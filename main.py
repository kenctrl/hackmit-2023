from discord import Intents  # Import the Intents class
import openai
from discord.ext import commands
import utils

MAX_TOKENS = 500

bot = commands.Bot(intents=Intents.all(), command_prefix='!')
openai.api_key = ""

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.event
async def on_message(message):
    print(message.content)
    await bot.process_commands(message)

@bot.command()
async def reply(ctx):
    user_messages_list = []
    messages = [msg async for msg in ctx.channel.history(limit=10)]
    for msg in messages:
        # if msg.author == ctx.author and msg.content != "!reply":
        user_messages_list.append(f"{msg.author}: {msg.content}")
    user_messages = "\n".join(user_messages_list)
    print("user messages:", user_messages)

    instructions = utils.read_prompt_file('instructions.txt')
    who_is = f"The person replying to the following conversation is {ctx.author.name}."

    user_content = f"{instructions} \n {who_is} \n {user_messages}" 

    response = openai.ChatCompletion.create(  # Use the chat model endpoint
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": utils.read_prompt_file('system.txt')},
            {"role": "user", "content": user_content},
        ],
        max_tokens = MAX_TOKENS,
    )

    reply = response.choices[0].message["content"].strip()
    print("reply:", reply)
    await bot.user.edit(username=ctx.author.name)
    await ctx.send(f"[Mimicking {ctx.author.name}]: {reply}")

bot.run("")
