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
    const filename = path.basename(decodedFile).replace('.pdf', '').replace('.tex', '');
    let targetPath = null;

    // 1. Direct check of the decoded path if it's local
    const isRemoteUrl = decodedFile.startsWith('http://') || decodedFile.startsWith('https://');
    if (!isRemoteUrl) {
        const directPath = path.resolve(rootDir, decodedFile);
        if (directPath.startsWith(rootDir) && fs.existsSync(directPath) && fs.statSync(directPath).isFile()) {
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
            const aliasPath = path.resolve(rootDir, ALIAS_MAP[filename]);
            if (fs.existsSync(aliasPath)) {
                targetPath = aliasPath;
            }
        }
    }

    // 3. Scan the aaa/ directory inside rootDir for matching filename
    if (!targetPath) {
        const targetDirs = [path.join(rootDir, 'aaa'), path.join(rootDir, 'COMMERCE_LATEX')];
        const allFiles = [];
        function walk(dir) {
            if (!fs.existsSync(dir)) return;
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
        targetDirs.forEach(walk);

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

    if (!targetPath) {
        res.status(404).json({ error: 'File Not Found' });
        return;
    }

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
