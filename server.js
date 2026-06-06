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
    '.ico': 'image/x-icon'
};

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

    // 3. Block access to .env file for security
    if (parsedUrl.pathname.includes('.env')) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Access Forbidden');
        return;
    }

    // 4. Serve static files
    let filePath = path.join(__dirname, parsedUrl.pathname === '/' ? 'index.html' : parsedUrl.pathname);
    
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
