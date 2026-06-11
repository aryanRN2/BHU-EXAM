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

        // If the file param is a remote HTTP URL (e.g. Supabase), skip local path resolution
        // and go straight to the local tex fallback search using just the filename.
        const isRemoteUrl = decodedFile.startsWith('http://') || decodedFile.startsWith('https://');

        let targetPath = isRemoteUrl ? null : path.resolve(__dirname, decodedFile);

        if (!isRemoteUrl && !targetPath.startsWith(__dirname)) {
            res.writeHead(403, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Access Forbidden' }));
            return;
        }

        let fileExists = false;
        if (!isRemoteUrl && targetPath) {
            try {
                fileExists = fs.existsSync(targetPath) && fs.statSync(targetPath).isFile();
            } catch (e) {
                fileExists = false;
            }
        }

        if (!fileExists) {
            const filename = path.basename(decodedFile).replace('.pdf', '').replace('.tex', '');
            const localTexFallbacks = [
                path.join(__dirname, 'aaa', 'chemistry', 'tex_files', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'cs', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'geology', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'geography', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'STATISTIC', 'tex_files', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'PHYSICS OUT', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'latest corrected maths pdf', 'final maths export latex', `${filename}.tex`),
                path.join(__dirname, 'aaa', 'all science pyq', `${filename}.tex`)
            ];

            let found = false;
            for (const fallbackPath of localTexFallbacks) {
                if (fs.existsSync(fallbackPath) && fs.statSync(fallbackPath).isFile()) {
                    targetPath = fallbackPath;
                    found = true;
                    break;
                }
            }

            if (!found) {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'File Not Found' }));
                return;
            }
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
    console.log(`BHU Exam Prep Server running at http://localhost:${PORT}`);
});
