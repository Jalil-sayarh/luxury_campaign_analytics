const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the dashboard build directory in production
// or from the dashboard directory in development
if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, 'dashboard/build')));
} else {
    app.use(express.static(path.join(__dirname, 'dashboard')));
}

// Route for the homepage
app.get('/', (req, res) => {
    if (process.env.NODE_ENV === 'production') {
        res.sendFile(path.join(__dirname, 'dashboard', 'build', 'index.html'));
    } else {
        res.sendFile(path.join(__dirname, 'dashboard', 'index.html'));
    }
});

// API routes can be added here
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok' });
});

// Catch-all route to handle SPA routing
app.get('*', (req, res) => {
    if (process.env.NODE_ENV === 'production') {
        res.sendFile(path.join(__dirname, 'dashboard', 'build', 'index.html'));
    } else {
        res.sendFile(path.join(__dirname, 'dashboard', 'index.html'));
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Luxury Marketing Dashboard server running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} in your browser to view the dashboard`);
});

// Export the express app for Vercel
module.exports = app; 