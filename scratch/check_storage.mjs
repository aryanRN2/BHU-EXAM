import fs from "fs";

// Load env variables manually from .env
const envContent = fs.readFileSync(".env", "utf-8");
const env = {};
envContent.split("\n").forEach(line => {
  const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
  if (match) {
    const key = match[1];
    let value = match[2] || "";
    // remove quotes if present
    if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
    if (value.startsWith("'") && value.endsWith("'")) value = value.slice(1, -1);
    env[key] = value;
  }
});

const projectRef = env.SUPABASE_PROJECT_REF;
const apiKey = env.SUPABASE_SERVICE_ROLE_KEY;

if (!projectRef || !apiKey) {
  console.error("Error: Missing Supabase credentials in .env");
  process.exit(1);
}

async function checkStorage() {
  const listBucketsUrl = `https://${projectRef}.supabase.co/storage/v1/bucket`;
  
  console.log("Fetching buckets...");
  const response = await fetch(listBucketsUrl, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "apikey": apiKey
    }
  });

  if (!response.ok) {
    const text = await response.text();
    console.error(`Failed to list buckets: Status ${response.status} - ${text}`);
    return;
  }

  const buckets = await response.json();
  console.log("Buckets found:", buckets);

  for (const bucket of buckets) {
    console.log(`\nAnalyzing bucket: ${bucket.id}`);
    
    const listObjectsUrl = `https://${projectRef}.supabase.co/storage/v1/object/list/${bucket.id}`;
    
    let totalSize = 0;
    let fileCount = 0;
    let limit = 100;
    let offset = 0;
    let hasMore = true;

    while (hasMore) {
      const objectsResponse = await fetch(listObjectsUrl, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "apikey": apiKey,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prefix: "",
          limit: limit,
          offset: offset,
          sortBy: { column: "name", order: "asc" }
        })
      });

      if (!objectsResponse.ok) {
        const text = await objectsResponse.text();
        console.error(`Failed to list objects for ${bucket.id} at offset ${offset}: Status ${objectsResponse.status} - ${text}`);
        hasMore = false;
        continue;
      }

      const objects = await objectsResponse.json();
      if (!objects || objects.length === 0) {
        hasMore = false;
        break;
      }

      for (const obj of objects) {
        if (obj.metadata) {
          totalSize += obj.metadata.size || 0;
          fileCount++;
        }
      }

      console.log(`Retrieved ${objects.length} items from offset ${offset}...`);
      offset += limit;
      if (objects.length < limit) {
        hasMore = false;
      }
    }
    
    console.log(`\nBucket summary for '${bucket.id}':`);
    console.log(`- Total Files: ${fileCount}`);
    console.log(`- Total Size: ${(totalSize / (1024 * 1024)).toFixed(2)} MB (${totalSize} bytes)`);
  }
}

checkStorage().catch(console.error);
