const fs = require('fs');
const path = require('path');

const rateLimitStore = {};

module.exports = async (req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    // Hotlink / Referer check
    const referer = req.headers.referer || '';
    const host = req.headers.host || '';
    if (!referer || !referer.includes(host)) {
        res.status(403).json({ error: 'Access Forbidden: Direct API requests are blocked' });
        return;
    }

    // Rate limiter check
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown';
    const now = Date.now();
    if (!rateLimitStore[ip]) rateLimitStore[ip] = [];
    rateLimitStore[ip] = rateLimitStore[ip].filter(time => now - time < 60000);

    if (rateLimitStore[ip].length >= 15) {
        res.status(429).json({ error: 'Too Many Requests: Please slow down' });
        return;
    }
    rateLimitStore[ip].push(now);

    const fileQuery = req.query.file;
    if (!fileQuery) {
        res.status(400).json({ error: 'Missing file parameter' });
        return;
    }

    // Resolve path and prevent directory traversal
    let decodedFile = '';
    try {
        decodedFile = decodeURIComponent(fileQuery);
    } catch (e) {
        decodedFile = fileQuery;
    }

    const rootDir = path.resolve(__dirname, '..');
    const targetPath = path.resolve(rootDir, decodedFile);

    // Safety check: ensure target path is within rootDir
    if (!targetPath.startsWith(rootDir)) {
        res.status(403).json({ error: 'Access Forbidden' });
        return;
    }

    // Ensure it ends with .tex
    if (!targetPath.endsWith('.tex')) {
        res.status(403).json({ error: 'Access Forbidden: Only .tex files can be loaded' });
        return;
    }

    if (!fs.existsSync(targetPath)) {
        res.status(404).json({ error: 'File Not Found' });
        return;
    }

    try {
        const rawText = fs.readFileSync(targetPath, 'utf8');
        
        // Simple XOR encryption + Base64
        const key = 'BHU_EXAM_PREP_KEY_2026';
        let xored = '';
        for (let i = 0; i < rawText.length; i++) {
            xored += String.fromCharCode(rawText.charCodeAt(i) ^ key.charCodeAt(i % key.length));
        }
        
        const encrypted = Buffer.from(xored, 'binary').toString('base64');
        res.status(200).json({ data: encrypted });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
