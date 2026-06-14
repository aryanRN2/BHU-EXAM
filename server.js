const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 8000;

// Read .env file
function loadEnv() {
    const envPath = path.join(__dirname, '.env');
    if (!fs.existsSync(envPath)) return {};
    const text = fs.readFileSync(envPath, 'utf8');
    const env = {};
    text.split('\n').forEach(line => {
        const parts = line.split('=');
        if (parts.length >= 2) {
            const key = parts[0].trim();
            const val = parts.slice(1).join('=').trim();
            env[key] = val.replace(/(^["']|["']$)/g, ''); // remove quotes
        }
    });
    return env;
}

const env = loadEnv();

const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.json': 'application/json',
    '.ico': 'image/x-icon',
    '.pdf': 'application/pdf',
    '.tex': 'text/plain'
};

const rateLimitStore = {};

const server = http.createServer(async (req, res) => {
    // Enable CORS for development
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    const parsedUrl = url.parse(req.url, true);
    
    // 1. API Config endpoint
    if (parsedUrl.pathname === '/api/config' && req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            HF_API_KEY: env.HF_API_KEY ? "configured" : "",
            NVIDIA_API_KEY: env.NVIDIA_API_KEY ? "configured" : ""
        }));
        return;
    }
    
    // 2. API proxy endpoint
    if (parsedUrl.pathname === '/api/ai' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', async () => {
            try {
                const payload = JSON.parse(body);
                const targetUrl = payload.url;
                let apiKey = payload.apiKey;
                const requestBody = payload.body;

                if (!targetUrl) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'Missing target url' }));
                    return;
                }

                // If apiKey is empty, retrieve from environment
                if (!apiKey) {
                    if (targetUrl.includes('nvidia.com')) {
                        apiKey = env.NVIDIA_API_KEY;
                    } else if (targetUrl.includes('huggingface.co')) {
                        apiKey = env.HF_API_KEY;
                    }
                }

                const headers = {
                    'Content-Type': 'application/json'
                };
                if (apiKey) {
                    headers['Authorization'] = `Bearer ${apiKey}`;
                }

                console.log(`[PROXY] Forwarding request to: ${targetUrl}`);
                const apiResponse = await fetch(targetUrl, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(requestBody)
                });

                const contentType = apiResponse.headers.get('content-type') || 'application/json';
                const responseData = await apiResponse.text();

                res.writeHead(apiResponse.status, { 'Content-Type': contentType });
                res.end(responseData);
            } catch (err) {
                console.error('Proxy error:', err);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }

    // 2.3. API Download PDF (Secure proxy for private Backblaze B2 files)
    if (parsedUrl.pathname === '/api/download-pdf' && req.method === 'GET') {
        // Hotlink / Referer check
        const referer = req.headers.referer || '';
        const host = req.headers.host || '';
        if (!referer || !referer.includes(host)) {
            res.writeHead(403, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Access Forbidden: Direct downloads are blocked' }));
            return;
        }

        const fileQuery = parsedUrl.query.file;
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
            const bucketName = env.B2_BUCKET_NAME;
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
                        // S3 format: bucket.s3.endpoint.com/path
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
            const keyId = env.B2_APPLICATION_KEY_ID;
            const applicationKey = env.B2_APPLICATION_KEY;
            const bucketId = env.B2_BUCKET_ID;

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
            const cdnBase = (env.B2_WORKER_URL || `${authData.downloadUrl}/file/${bucketName}`).replace(/\/$/, '');
            const signedUrl = `${cdnBase}/${encodedPath}?Authorization=${docData.authorizationToken}`;

            // Redirect user to the secure temporary signed URL
            res.writeHead(302, { 'Location': signedUrl });
            res.end();
        } catch (err) {
            console.error("B2 Signing Error:", err);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: err.message }));
        }
        return;
    }

    // 2.5. API PYQ encryption endpoint
    if (parsedUrl.pathname === '/api/pyq' && req.method === 'GET') {
        // Hotlink / Referer check
        const referer = req.headers.referer || '';
        const host = req.headers.host || '';
        if (!referer || !referer.includes(host)) {
            res.writeHead(403, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Access Forbidden: Direct API requests are blocked' }));
            return;
        }

        // Rate limiter check
        const ip = req.socket.remoteAddress || 'unknown';
        const now = Date.now();
        if (!rateLimitStore[ip]) rateLimitStore[ip] = [];
        rateLimitStore[ip] = rateLimitStore[ip].filter(time => now - time < 60000);

        if (rateLimitStore[ip].length >= 100) {
            res.writeHead(429, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Too Many Requests: Please slow down' }));
            return;
        }
        rateLimitStore[ip].push(now);

        const fileQuery = parsedUrl.query.file;
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

        const filename = path.basename(decodedFile).replace('.pdf', '').replace('.tex', '');
        let targetPath = null;

        // 1. Direct check of the decoded path if it's local
        const isRemoteUrl = decodedFile.startsWith('http://') || decodedFile.startsWith('https://');
        if (!isRemoteUrl) {
            const directPath = path.resolve(__dirname, decodedFile);
            if (directPath.startsWith(__dirname) && fs.existsSync(directPath) && fs.statSync(directPath).isFile()) {
                targetPath = directPath;
            }
        }

        // 2. Explicit Alias Map
        if (!targetPath) {
            const ALIAS_MAP = {
                'ode_2023-24': 'aaa/latest corrected maths pdf/final maths export latex/MTB-302_DiffEq_BSc-SemIII_2023-24.tex',
                'ode_2024-25': 'aaa/latest corrected maths pdf/final maths export latex/MTB-302_DiffEq_BSc-SemIII_2023-24.tex',
                'STB_501__Applied_Statistics_2024_25': 'aaa/STATISTIC/tex_files/STA_STB-501_AppliedStatistics_SemV_2022-23_BSc.tex',
                'STB_502__Statistical_Inference_and_Decision_Theory_2024_25': 'aaa/STATISTIC/tex_files/STA_STB-502_StatisticalInferenceandDecisionTheory_SemV_2022-23_BSc.tex'
            };

            if (ALIAS_MAP[filename]) {
                const aliasPath = path.resolve(__dirname, ALIAS_MAP[filename]);
                if (fs.existsSync(aliasPath)) {
                    targetPath = aliasPath;
                }
            }
        }

        // 3. Scan the aaa/ directory for matching filename
        if (!targetPath) {
            const aaaDir = path.join(__dirname, 'aaa');
            if (fs.existsSync(aaaDir)) {
                const allFiles = [];
                function walk(dir) {
                    const list = fs.readdirSync(dir);
                    list.forEach(file => {
                        const fullPath = path.join(dir, file);
                        if (fs.statSync(fullPath).isDirectory()) {
                            walk(fullPath);
                        } else if (file.endsWith('.tex')) {
                            allFiles.push({
                                name: file.replace('.tex', ''),
                                path: fullPath
                            });
                        }
                    });
                }
                walk(aaaDir);

                // Exact match
                let matched = allFiles.find(f => f.name === filename);
                
                // Normalized match
                if (!matched) {
                    const normTarget = filename.toLowerCase().replace(/[^a-z0-9]/g, '');
                    matched = allFiles.find(f => f.name.toLowerCase().replace(/[^a-z0-9]/g, '') === normTarget);
                }

                // Code-year regex match
                if (!matched) {
                    const codeMatch = filename.match(/([A-Z]{3})[-_](\d{3})/i);
                    const yearMatch = filename.match(/(\d{4}[-_]\d{2})/);
                    if (codeMatch && yearMatch) {
                        const code = codeMatch[1].toUpperCase() + '-' + codeMatch[2];
                        const year = yearMatch[1].replace('_', '-');
                        matched = allFiles.find(f => {
                            const nameUpper = f.name.toUpperCase();
                            return (nameUpper.includes(code) || nameUpper.includes(code.replace('-', '_'))) && 
                                   nameUpper.includes(year);
                        });
                    }
                }

                // Fuzzy match
                if (!matched) {
                    const normTarget = filename.toLowerCase().replace(/[^a-z0-9]/g, '');
                    matched = allFiles.find(f => {
                        const normFile = f.name.toLowerCase().replace(/[^a-z0-9]/g, '');
                        return normFile.includes(normTarget) || normTarget.includes(normFile);
                    });
                }

                if (matched) {
                    targetPath = matched.path;
                }
            }
        }

        if (!targetPath) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'File Not Found' }));
            return;
        }

        if (!targetPath.endsWith('.tex')) {
            res.writeHead(403, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Access Forbidden: Only .tex files can be loaded' }));
            return;
        }

        try {
            const rawText = fs.readFileSync(targetPath, 'utf8');
            const key = 'BHU_EXAM_PREP_KEY_2026';
            let xored = '';
            for (let i = 0; i < rawText.length; i++) {
                xored += String.fromCharCode(rawText.charCodeAt(i) ^ key.charCodeAt(i % key.length));
            }
            const encrypted = Buffer.from(xored, 'binary').toString('base64');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ data: encrypted }));
        } catch (err) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: err.message }));
        }
        return;
    }

    // 3. Security Filters: Block access to dotfiles, configuration, and backend files
    let decodedPathname = '';
    try {
        decodedPathname = decodeURIComponent(parsedUrl.pathname);
    } catch (e) {
        decodedPathname = parsedUrl.pathname;
    }

    const pathParts = decodedPathname.split('/');
    const isDotfile = pathParts.some(part => part.startsWith('.'));
    const forbiddenFiles = ['package.json', 'package-lock.json', 'server.js', 'vercel.json', '.env', '.tex'];
    const isForbiddenFile = forbiddenFiles.some(file => decodedPathname.endsWith(file));
    const isBlockedDir = decodedPathname.includes('/scratch/') || decodedPathname.includes('/api/') || decodedPathname.includes('/node_modules/');
    const isRootScript = pathParts.length === 2 && decodedPathname.endsWith('.js');
    const isMjs = decodedPathname.endsWith('.mjs');

    if (isDotfile || isForbiddenFile || isBlockedDir || isRootScript || isMjs) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Access Forbidden');
        return;
    }

    // 4. Serve static files
    let filePath = path.join(__dirname, decodedPathname === '/' ? 'index.html' : decodedPathname);
    
    // Safety check to prevent directory traversal
    if (!filePath.startsWith(__dirname)) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Access Forbidden');
        return;
    }

    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            const htmlPath = filePath + '.html';
            fs.stat(htmlPath, (errHtml, statsHtml) => {
                if (!errHtml && statsHtml.isFile()) {
                    serveFile(htmlPath, res);
                } else {
                    res.writeHead(404, { 'Content-Type': 'text/plain' });
                    res.end('404 Not Found');
                }
            });
        } else {
            serveFile(filePath, res);
        }
    });
});

function serveFile(filePath, res) {
    const ext = path.extname(filePath);
    const contentType = mimeTypes[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType });
    
    const stream = fs.createReadStream(filePath);
    stream.on('error', (err) => {
        res.writeHead(500);
        res.end('Server Error');
    });
    stream.pipe(res);
}

server.listen(PORT, () => {
    console.log(`SCIQB Server running at http://localhost:${PORT}`);
});
