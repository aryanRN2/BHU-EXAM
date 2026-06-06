module.exports = async (req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization'
    );

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    if (req.method !== 'POST') {
        res.status(405).json({ error: 'Method Not Allowed' });
        return;
    }

    try {
        // Vercel parses the body automatically if it is JSON
        const payload = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
        const targetUrl = payload.url;
        let apiKey = payload.apiKey;
        const requestBody = payload.body;

        if (!targetUrl) {
            res.status(400).json({ error: 'Missing target url' });
            return;
        }

        // If apiKey is empty, retrieve from environment
        if (!apiKey) {
            if (targetUrl.includes('nvidia.com')) {
                apiKey = process.env.NVIDIA_API_KEY;
            } else if (targetUrl.includes('huggingface.co')) {
                apiKey = process.env.HF_API_KEY;
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

        res.setHeader('Content-Type', contentType);
        res.status(apiResponse.status).send(responseData);
    } catch (err) {
        console.error('Proxy error:', err);
        res.status(500).json({ error: err.message });
    }
};
