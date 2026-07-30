const rateLimitStore = {};

module.exports = async (req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // Rate limiter check
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown';
    const now = Date.now();
    if (!rateLimitStore[ip]) rateLimitStore[ip] = [];
    rateLimitStore[ip] = rateLimitStore[ip].filter(time => now - time < 60000);

    if (rateLimitStore[ip].length >= 15) {
        res.writeHead(429, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Too Many Requests: Please slow down' }));
        return;
    }
    rateLimitStore[ip].push(now);

    const fileQuery = req.query.file;
    if (!fileQuery) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Missing file parameter' }));
        return;
    }

    let decodedFile = '';
    try {
        decodedFile = decodeURIComponent(fileQuery);
    } catch (e) {
        decodedFile = fileQuery;
    }

    // If it's a Supabase URL, redirect directly (it's public)
    if (decodedFile.includes('supabase.co')) {
        res.writeHead(302, { 'Location': decodedFile });
        res.end();
        return;
    }

    // If it's a B2 URL or path, generate a signed download URL
    try {
        const bucketName = process.env.B2_BUCKET_NAME;
        // Extract relative path from URL if a full URL was passed
        let relativePath = decodedFile;
        if (decodedFile.startsWith('http')) {
            try {
                const urlObj = new URL(decodedFile);
                const pathParts = decodeURIComponent(urlObj.pathname).split('/');
                const bucketIndex = pathParts.indexOf(bucketName);
                if (bucketIndex !== -1) {
                    relativePath = pathParts.slice(bucketIndex + 1).join('/');
                } else if (urlObj.hostname.startsWith(bucketName)) {
                    // S3 format
                    relativePath = pathParts.slice(1).join('/');
                } else {
                    relativePath = pathParts.slice(1).join('/');
                }
            } catch (e) {
                relativePath = decodedFile;
            }
        }

        // Clean up leading slashes
        relativePath = relativePath.replace(/^\/+/, '');

        // Call B2 API to get signed URL
        const keyId = process.env.B2_APPLICATION_KEY_ID;
        const applicationKey = process.env.B2_APPLICATION_KEY;
        const bucketId = process.env.B2_BUCKET_ID;

        if (!keyId || !applicationKey || !bucketId) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'B2 storage is not configured on the server' }));
            return;
        }

        // 1. Authorize B2
        const authHeader = "Basic " + Buffer.from(`${keyId}:${applicationKey}`).toString("base64");
        const authRes = await fetch("https://api.backblazeb2.com/b2api/v2/b2_authorize_account", {
            method: "GET",
            headers: { "Authorization": authHeader }
        });
        if (!authRes.ok) throw new Error(`B2 Auth Failed: ${authRes.status}`);
        const authData = await authRes.json();
        
        // 2. Get download auth
        const docRes = await fetch(`${authData.apiUrl}/b2api/v2/b2_get_download_authorization`, {
            method: "POST",
            headers: {
                "Authorization": authData.authorizationToken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                bucketId: bucketId,
                fileNamePrefix: relativePath,
                validDurationInSeconds: 600 // 10 minutes
            })
        });
        if (!docRes.ok) throw new Error(`B2 Download Auth Failed: ${docRes.status}`);
        const docData = await docRes.json();

        // 3. Construct signed URL (route through Cloudflare Worker CDN if configured)
        const encodedPath = relativePath.split('/').map(encodeURIComponent).join('/');
        const cdnBase = (process.env.B2_WORKER_URL || `${authData.downloadUrl}/file/${bucketName}`).replace(/\/$/, '');
        const signedUrl = `${cdnBase}/${encodedPath}?Authorization=${docData.authorizationToken}`;

        // Redirect user to the secure temporary signed URL
        res.writeHead(302, { 'Location': signedUrl });
        res.end();
    } catch (err) {
        console.error("B2 Signing Error:", err);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
    }
};
