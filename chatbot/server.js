import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import fetch from "node-fetch"; // Use import instead of require


const app = express();
const PORT = 3000;
const API_URL = "https://api.deepseek.com/chat"; // Replace with correct Deepseek API URL
const API_KEY = "sk-999bec56ddf14b3890c7f9e7d94a3182"; // Replace with your API key

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Chatbot route
app.post("/chat", async (req, res) => {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${API_KEY}`,
            },
            body: JSON.stringify(req.body),
        });

        if (!response.ok) {
            throw new Error(`Deepseek API error: ${response.statusText}`);
        }

        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Chatbot server running at http://localhost:${PORT}`);
});
