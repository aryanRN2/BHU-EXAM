import fetch from 'node-fetch';

const files = [
    "NOTES/MATHS/SEMESTER 4/KM Sir class notes.pdf",
    "NOTES/MATHS/SEMESTER 4/Vector and Tensor Analysis notes.pdf",
    "NOTES/MATHS/SEMESTER 4/Differential equation notes.pdf",
    "NOTES/MATHS/SEMESTER 4/MECHANICS class notes .pdf",
    "NOTES/MATHS/SEMESTER 4/Differential equation notes.pdf"
];

async function checkFiles() {
    for (const file of files) {
        const url = `http://localhost:8000/api/download-pdf?file=${encodeURIComponent(file)}`;
        console.log(`Checking: ${file}`);
        try {
            const res = await fetch(url, {
                headers: {
                    'Referer': 'http://localhost:8000/notes.html'
                }
            });
            console.log(`  Response Status: ${res.status}`);
            if (res.status === 200 || res.status === 302) {
                console.log(`  Redirect/Target URL: ${res.url}`);
                const finalRes = await fetch(res.url);
                console.log(`  Final Fetch Status: ${finalRes.status}`);
            } else {
                console.log(`  Error body: ${await res.text()}`);
            }
        } catch (e) {
            console.log(`  Error: ${e.message}`);
        }
        console.log('---');
    }
}

checkFiles();
