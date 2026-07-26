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

  const notesDir = path.join(process.cwd(), 'NOTES');
  if (!fs.existsSync(notesDir)) {
    console.error("No NOTES directory found in the workspace.");
    return;
  }

  const localFiles = getFilesRecursive(notesDir);
  console.log(`Found ${localFiles.length} files to upload.`);

  // Upload concurrently with limit
  const CONCURRENCY = 5;
  let activeCount = 0;
  let index = 0;

  await new Promise((resolve, reject) => {
    function next() {
      if (index >= localFiles.length && activeCount === 0) {
        resolve();
        return;
      }
      
      while (activeCount < CONCURRENCY && index < localFiles.length) {
        const filePath = localFiles[index++];
        const relativePath = path.relative(process.cwd(), filePath);
        const b2Key = relativePath.replace(/\\/g, '/');

        activeCount++;
        console.log(`Uploading "${b2Key}"...`);

        const fileContent = fs.readFileSync(filePath);
        const sha1 = crypto.createHash('sha1').update(fileContent).digest('hex');
        const safeB2Key = encodeURIComponent(b2Key).replace(/%2F/g, '/');

        fetch(uploadUrl, {
          method: "POST",
          headers: {
            "Authorization": uploadAuthToken,
            "X-Bz-File-Name": safeB2Key,
            "Content-Type": "application/pdf",
            "Content-Length": fileContent.length.toString(),
            "X-Bz-Content-Sha1": sha1
          },
          body: fileContent
        }).then(res => {
          if (res.ok) {
            console.log(`Successfully uploaded: ${b2Key}`);
          } else {
            res.text().then(errText => {
              console.error(`Failed to upload ${b2Key}: ${res.status} - ${errText}`);
            });
          }
          activeCount--;
          next();
        }).catch(err => {
          console.error(`Error uploading ${b2Key}:`, err);
          activeCount--;
          next();
        });
      }
    }
    next();
  });

  console.log("All uploads finished!");
}

uploadToB2().catch(err => {
  console.error("Upload process crashed:", err);
  process.exit(1);
});
