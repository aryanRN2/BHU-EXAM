import fs from "fs";
import path from "path";
import crypto from "crypto";

// Load env variables manually from .env
function loadEnv() {
  const envPath = ".env";
  if (!fs.existsSync(envPath)) return {};
  const envContent = fs.readFileSync(envPath, "utf-8");
  const env = {};
  envContent.split("\n").forEach(line => {
    const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
    if (match) {
      const key = match[1];
      let value = match[2] || "";
      if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
      if (value.startsWith("'") && value.endsWith("'")) value = value.slice(1, -1);
      env[key] = value;
    }
  });
  return env;
}

const env = loadEnv();
const keyId = env.B2_APPLICATION_KEY_ID;
const applicationKey = env.B2_APPLICATION_KEY;
const bucketId = env.B2_BUCKET_ID;

export async function uploadFileToB2(localFilePath, b2DestPath) {
  if (!keyId || !applicationKey || !bucketId) {
    throw new Error("Missing Backblaze B2 credentials in .env file.");
  }

  if (!fs.existsSync(localFilePath)) {
    throw new Error(`Local file not found: ${localFilePath}`);
  }

  console.log(`[B2] Authorizing account...`);
  const authHeader = "Basic " + Buffer.from(`${keyId}:${applicationKey}`).toString("base64");
  const authRes = await fetch("https://api.backblazeb2.com/b2api/v2/b2_authorize_account", {
    method: "GET",
    headers: {
      "Authorization": authHeader
    }
  });

  if (!authRes.ok) {
    const text = await authRes.text();
    throw new Error(`B2 Authorization failed: ${authRes.status} - ${text}`);
  }

  const authData = await authRes.json();
  const apiUrl = authData.apiUrl;
  const accountAuthToken = authData.authorizationToken;

  console.log(`[B2] Getting upload URL for bucket ID: ${bucketId}...`);
  const uploadUrlRes = await fetch(`${apiUrl}/b2api/v2/b2_get_upload_url`, {
    method: "POST",
    headers: {
      "Authorization": accountAuthToken,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ bucketId: bucketId })
  });

  if (!uploadUrlRes.ok) {
    const text = await uploadUrlRes.text();
    throw new Error(`Failed to get B2 upload URL: ${uploadUrlRes.status} - ${text}`);
  }

  const uploadUrlData = await uploadUrlRes.json();
  const uploadUrl = uploadUrlData.uploadUrl;
  const uploadAuthToken = uploadUrlData.authorizationToken;

  // Read file and compute SHA-1
  const fileBuffer = fs.readFileSync(localFilePath);
  const sha1 = crypto.createHash("sha1").update(fileBuffer).digest("hex");
  const fileSize = fileBuffer.length;

  console.log(`[B2] Uploading file '${b2DestPath}' (${(fileSize / 1024).toFixed(1)} KB)...`);
  
  // RFC 3986 URL encode filename (excluding slashes / to preserve directories)
  const encodedFileName = b2DestPath
    .split("/")
    .map(segment => encodeURIComponent(segment))
    .join("/");

  const uploadRes = await fetch(uploadUrl, {
    method: "POST",
    headers: {
      "Authorization": uploadAuthToken,
      "X-Bz-File-Name": encodedFileName,
      "Content-Type": "application/pdf",
      "X-Bz-Content-Sha1": sha1,
      "Content-Length": String(fileSize)
    },
    body: fileBuffer
  });

  if (!uploadRes.ok) {
    const text = await uploadRes.text();
    throw new Error(`B2 upload failed: ${uploadRes.status} - ${text}`);
  }

  const uploadResult = await uploadRes.json();
  console.log(`[B2] Success! File uploaded. File ID: ${uploadResult.fileId}`);
  return uploadResult;
}

// Support executing directly as a script (e.g. node scratch/upload_to_b2.mjs local_path b2_path)
const args = process.argv.slice(2);
if (args.length >= 2) {
  const [localFile, destPath] = args;
  uploadFileToB2(localFile, destPath)
    .then(() => console.log("Done."))
    .catch(err => {
      console.error(err);
      process.exit(1);
    });
}
