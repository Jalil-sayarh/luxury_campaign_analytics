const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the dashboard directory
app.use(express.static(path.join(__dirname, 'dashboard')));

// Route for the homepage
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Luxury Marketing Dashboard server running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} in your browser to view the dashboard`);
}); 