import fs from "fs";
import path from "path";
import crypto from "crypto";

// 1. Load env variables manually from .env
const envContent = fs.readFileSync(".env", "utf-8");
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

const keyId = env.B2_APPLICATION_KEY_ID;
const applicationKey = env.B2_APPLICATION_KEY;
const bucketId = env.B2_BUCKET_ID;
const bucketName = env.B2_BUCKET_NAME;

if (!keyId || !applicationKey || !bucketId) {
  console.error("Error: Missing Backblaze B2 credentials in .env");
  process.exit(1);
}

// 2. Authorize Account
async function authorizeB2() {
  console.log("Authorizing with Backblaze B2...");
  const credentials = Buffer.from(`${keyId}:${applicationKey}`).toString("base64");
  const response = await fetch("https://api.backblazeb2.com/b2api/v2/b2_authorize_account", {
    headers: {
      "Authorization": `Basic ${credentials}`
    }
  });

  if (!response.ok) {
    throw new Error(`B2 Authorization failed: ${response.status} ${await response.text()}`);
  }

  const data = await response.json();
  console.log("Authorized successfully!");
  return data;
}

// 3. Get Upload URL
async function getUploadUrl(apiUrl, authToken) {
  const response = await fetch(`${apiUrl}/b2api/v2/b2_get_upload_url`, {
    method: "POST",
    headers: {
      "Authorization": authToken,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ bucketId })
  });

  if (!response.ok) {
    throw new Error(`Failed to get upload URL: ${response.status} ${await response.text()}`);
  }

  return response.json();
}

// 4. Upload File
async function uploadFile(authData, relativeFilePath) {
  if (!fs.existsSync(relativeFilePath)) {
    console.error(`File not found: ${relativeFilePath}`);
    return;
  }

  const fileBuffer = fs.readFileSync(relativeFilePath);
  const sha1 = crypto.createHash("sha1").update(fileBuffer).digest("hex");
  const b2FileName = relativeFilePath.replace(/\\/g, "/");

  console.log(`Getting upload URL for: ${b2FileName}...`);
  const { uploadUrl, authorizationToken } = await getUploadUrl(authData.apiUrl, authData.authorizationToken);

  console.log(`Uploading ${b2FileName} (${(fileBuffer.length / (1024 * 1024)).toFixed(2)} MB)...`);
  const uploadRes = await fetch(uploadUrl, {
    method: "POST",
    headers: {
      "Authorization": authorizationToken,
      "X-Bz-File-Name": encodeURIComponent(b2FileName),
      "Content-Type": "application/pdf",
      "Content-Length": fileBuffer.length.toString(),
      "X-Bz-Content-Sha1": sha1
    },
    body: fileBuffer
  });

  if (uploadRes.ok) {
    const resData = await uploadRes.json();
    console.log(`Successfully uploaded ${b2FileName}! File ID: ${resData.fileId}`);
  } else {
    const errText = await uploadRes.text();
    console.error(`Failed to upload ${b2FileName}: ${uploadRes.status} - ${errText}`);
  }
}

async function run() {
  const authData = await authorizeB2();

  const fileToUpload = process.argv[2] || "NOTES/PHY/sem 4/sem 4 relativity notes.pdf";
  await uploadFile(authData, fileToUpload);
}

run().catch(console.error);
