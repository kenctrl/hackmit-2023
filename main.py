import discord
from discord import Intents, Message  # Import the Intents class
import openai

client = discord.Client(intents=Intents.all())  # Specify the intents
openai.api_key = "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"

chatHistory = {}

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message: Message):

    channel = message.channel

    channel_id = channel.id

    if channel_id not in chatHistory:
        chatHistory[channel_id] = []

    chatHistory[channel_id].append(f"{message.author.name}: {message.content}")

    if len(chatHistory[channel_id]) > 100:
        chatHistory[channel_id].pop(0)

    if message.content == ".reply":

        conversation = "\n".join(chatHistory[channel_id])
        prompt = f"{conversation}\nHow would {message.author} reply? Please respond with the exact response."
        max_tokens = 50

        response = openai.ChatCompletion.create(  # Use the chat model endpoint
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens = max_tokens,
        )
        reply = response.choices[0].message["content"].strip()
        await client.user.edit(username=message.author.name)
        await message.channel.send(f"[Mimicking {message.author.name}]: {reply}")

client.run("MTE1MjczMzMxMzE1MzM4MDQ4Mg.GmtPEq.pue9VY1UYqLa9DRW8RZvQVYx2T0-qfYP6rL4Fs")
