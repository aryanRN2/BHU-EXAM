import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import https from 'https';

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

function uploadFileWithHttps(uploadUrl, headers, fileContent) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(uploadUrl);
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'POST',
      headers: headers,
      timeout: 300000 // 5 minutes timeout
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ ok: true, status: res.statusCode, body });
        } else {
          resolve({ ok: false, status: res.statusCode, body });
        }
      });
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timed out'));
    });

    req.write(fileContent);
    req.end();
  });
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

  // Only target the Chemistry notes folder
  const chemistryNotesDir = path.join(process.cwd(), 'NOTES', 'CHEMISTRY');
  if (!fs.existsSync(chemistryNotesDir)) {
    console.error("No NOTES/CHEMISTRY directory found.");
    return;
  }

  const localFiles = getFilesRecursive(chemistryNotesDir);
  console.log(`Found ${localFiles.length} Chemistry files to upload:`);
  console.log(localFiles);

  for (const filePath of localFiles) {
    const relativePath = path.relative(process.cwd(), filePath);
    const b2Key = relativePath.replace(/\\/g, '/');

    console.log(`\nUploading "${filePath}" to B2 as key: "${b2Key}"...`);

    const fileContent = fs.readFileSync(filePath);
    const sha1 = crypto.createHash('sha1').update(fileContent).digest('hex');
    const safeB2Key = encodeURIComponent(b2Key).replace(/%2F/g, '/');

    try {
      const result = await uploadFileWithHttps(uploadUrl, {
        "Authorization": uploadAuthToken,
        "X-Bz-File-Name": safeB2Key,
        "Content-Type": "application/pdf",
        "Content-Length": fileContent.length.toString(),
        "X-Bz-Content-Sha1": sha1
      }, fileContent);

      if (result.ok) {
        console.log(`Successfully uploaded: ${b2Key}`);
      } else {
        console.error(`Failed to upload ${b2Key}: Status ${result.status} - ${result.body}`);
      }
    } catch (err) {
      console.error(`Error uploading ${b2Key}:`, err.message);
    }
  }
}

uploadToB2().catch(err => {
  console.error("Upload process crashed:", err);
});
