import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./components/App.js";

// // renders React Component "Root" into the DOM element with ID "root"
// const container = document.getElementById("root");
// const root = createRoot(container);
// root.render(
//   <BrowserRouter>
//     <App />
//   </BrowserRouter>
// );

// // allows for live updating
// module.hot.accept();

const OpenAIAPI = require('openai');
const openai = new OpenAIAPI({key: "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"});

const Discord = require("discord.js");
const client = new Discord.Client();

let chatHistory = {};

client.once("ready", () => {
  console.log("Ready!");
});

client.on("message", async (message) => {
  if (!chatHistory[message.channel.id]) {
    chatHistory[message.channel.id] = [];
  }
  chatHistory[message.channel.id].push(message.content);

  // Limit chat history to the last 100 messages for simplicity
  if (chatHistory[message.channel.id].length > 100) {
    chatHistory[message.channel.id].shift();
  }

  if (message.content === ".reply") {
    const conversation = chatHistory[message.channel.id].join("\n");
    
    // Generate reply using OpenAI API
    const prompt = `${conversation}\nHow would [Your Name] reply: `;
    const maxTokens = 300; // Limit the reply length
    
    const apiResponse = await openai.createCompletion({
      prompt: prompt,
      max_tokens: maxTokens
    });
    
    const reply = apiResponse.choices[0].text.trim();
    message.channel.send(`[Mimicking ${message.author.username}]: ${reply}`);
  }
  
  });
