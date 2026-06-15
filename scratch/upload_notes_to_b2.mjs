import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

// Load env variables manually from .env
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

if (!keyId || !applicationKey || !bucketId) {
  console.error("Error: Missing Backblaze B2 credentials in .env");
  process.exit(1);
}

// Recursively traverse directory to find files
function getFilesRecursive(dir) {
  const results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results.push(...getFilesRecursive(fullPath));
    } else {
      results.push(fullPath);
    }
  });
  return results;
}

async function uploadToB2() {
  console.log("Authorizing B2...");
  const authHeader = "Basic " + Buffer.from(`${keyId}:${applicationKey}`).toString("base64");
  const authRes = await fetch("https://api.backblazeb2.com/b2api/v2/b2_authorize_account", {
    method: "GET",
    headers: { "Authorization": authHeader }
  });
  
  if (!authRes.ok) {
    throw new Error(`B2 Auth Failed: ${authRes.status} ${await authRes.text()}`);
  }
  
  const authData = await authRes.json();
  const { apiUrl, authorizationToken } = authData;
  console.log("Authorized successfully!");

  console.log("Getting upload URL...");
  const uploadUrlRes = await fetch(`${apiUrl}/b2api/v2/b2_get_upload_url`, {
    method: "POST",
    headers: {
      "Authorization": authorizationToken,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ bucketId })
  });

  if (!uploadUrlRes.ok) {
    throw new Error(`B2 Get Upload URL Failed: ${uploadUrlRes.status} ${await uploadUrlRes.text()}`);
  }

  const uploadUrlData = await uploadUrlRes.json();
  const { uploadUrl, authorizationToken: uploadAuthToken } = uploadUrlData;
  console.log("Got upload URL!");

  // Find files inside the local NOTES directory
  const notesDir = path.join(process.cwd(), 'NOTES');
  if (!fs.existsSync(notesDir)) {
    console.error("No NOTES directory found in the workspace.");
    return;
  }

  const localFiles = getFilesRecursive(notesDir);
  console.log(`Found ${localFiles.length} files to upload:`);
  console.log(localFiles);

  for (const filePath of localFiles) {
    // Determine the key inside the bucket: NOTES/MATHS/...
    const relativePath = path.relative(process.cwd(), filePath);
    // Replace backslashes for Windows path safety
    const b2Key = relativePath.replace(/\\/g, '/');

    console.log(`\nUploading "${filePath}" to B2 as key: "${b2Key}"...`);

    const fileContent = fs.readFileSync(filePath);
    
    // Calculate SHA1
    const sha1 = crypto.createHash('sha1').update(fileContent).digest('hex');

    // Headers must be URL encoded for non-ASCII characters
    // X-Bz-File-Name requires RFC 5987 / custom encoding or simple encodeURIComponent/escape for B2
    const safeB2Key = encodeURIComponent(b2Key)
      .replace(/%2F/g, '/'); // Leave slashes intact for directory structure in B2 panel

    const response = await fetch(uploadUrl, {
      method: "POST",
      headers: {
        "Authorization": uploadAuthToken,
        "X-Bz-File-Name": safeB2Key,
        "Content-Type": "application/pdf",
        "Content-Length": fileContent.length.toString(),
        "X-Bz-Content-Sha1": sha1
      },
      body: fileContent
    });

    if (response.ok) {
      console.log(`Successfully uploaded: ${b2Key}`);
    } else {
      const errorText = await response.text();
      console.error(`Failed to upload ${b2Key}: Status ${response.status} - ${errorText}`);
    }
  }
}

uploadToB2().catch(err => {
  console.error("Upload process crashed:", err);
});
