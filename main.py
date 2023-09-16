import discord
from discord import Intents  # Import the Intents class
import openai

client = discord.Client(intents=Intents.all())  # Specify the intents
openai.api_key = ""

chatHistory = {}

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_id = message.channel.id

    if channel_id not in chatHistory:
        chatHistory[channel_id] = []

    chatHistory[channel_id].append(message.content)

    if len(chatHistory[channel_id]) > 100:
        chatHistory[channel_id].pop(0)

    if message.content == ".reply":
        conversation = "\n".join(chatHistory[channel_id])
        prompt = f"{conversation}\nHow would [Your Name] reply: "
        max_tokens = 50

        response = openai.Completion.create(
          model="gpt-3.5-turbo-16k",
          prompt=prompt,
          max_tokens=max_tokens
        )
        
        reply = response.choices[0].text.strip()
        await message.channel.send(f"[Mimicking {message.author.name}]: {reply}")

client.run("MTE1MjczMzMxMzE1MzM4MDQ4Mg.G9V-nZ.7hls6a2VQNVdMefgplyhqhhjrZvdDKIjf26BNw")
