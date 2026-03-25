const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

const server = http.createServer((req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    // Serve index.html for root path
    if (req.url === '/' || req.url === '/index.html') {
        const filePath = path.join(PUBLIC_DIR, 'index.html');
        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(500);
                return res.end('Error loading index.html');
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
        });
    } 
    // Proxy API requests to our Python API running on port 8000
    else if (req.url.startsWith('/api/')) {
        // For simplicity in this example, we'll just show a message
        // In a real setup, you'd proxy to your actual API
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
            message: 'This is a proxy to your Python API. Make sure python api/hello.py is running on port 8000.',
            note: 'For full local development, run: python api/hello.py in one terminal, and node server.js in another.'
        }));
    }
    // Serve static files from public directory
    else {
        const filePath = path.join(PUBLIC_DIR, req.url);
        fs.access(filePath, fs.constants.F_OK, (err) => {
            if (err) {
                res.writeHead(404);
                res.end('Not found');
                return;
            }
            
            fs.readFile(filePath, (err, data) => {
                if (err) {
                    res.writeHead(500);
                    res.end('Error loading file');
                    return;
                }
                
                // Set content type based on file extension
                const ext = path.extname(filePath).toLowerCase();
                let contentType = 'text/plain';
                
                switch (ext) {
                    case '.html':
                        contentType = 'text/html';
                        break;
                    case '.css':
                        contentType = 'text/css';
                        break;
                    case '.js':
                        contentType = 'application/javascript';
                        break;
                    case '.json':
                        contentType = 'application/json';
                        break;
                    case '.png':
                        contentType = 'image/png';
                        break;
                    case '.jpg':
                    case '.jpeg':
                        contentType = 'image/jpeg';
                        break;
                }
                
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(data);
            });
        });
    }
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log('Make sure to run your Python API in another terminal:');
    console.log('  cd api && python hello.py');
    console.log('Then visit http://localhost:3000 to test your frontend!');
});