from discord import Intents  # Import the Intents class
import openai
from discord.ext import commands
import utils

MESSAGE_HISTORIES = {}
MAX_TOKENS = 500

bot = commands.Bot(intents=Intents.all(), command_prefix='!')
openai.api_key = ""

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.event
async def on_message(message):
    try:
        if message.content.split()[0] != "!reply":
            if message.channel.id not in MESSAGE_HISTORIES:
                MESSAGE_HISTORIES[message.channel.id] = []
            MESSAGE_HISTORIES[message.channel.id].append(message.content)
    except:
        print("Message error. Message:", reply)
    await bot.process_commands(message)

@bot.command()
async def reply(ctx: commands.Context):
    channel_id = ctx.channel.id
    if channel_id not in MESSAGE_HISTORIES:
        MESSAGE_HISTORIES[channel_id] = []
        messages = [msg async for msg in ctx.channel.history(limit=10)]
        for msg in messages:
            # if msg.author == ctx.author and msg.content != "!reply":
            MESSAGE_HISTORIES[channel_id].append(f"{msg.author}: {msg.content}")
    user_messages = "\n".join(MESSAGE_HISTORIES[channel_id])

    instructions = utils.read_prompt_file('instructions.txt')
    who_is = f"The person replying to the following conversation is {ctx.author.global_name}."

    user_content = f"{instructions} \n {who_is} \n {user_messages}" 

    # TODO: Are the messages being addded to the history backwards
    response = openai.ChatCompletion.create(  # Use the chat model endpoint
        model="gpt-4",
        messages=[
            {"role": "system", "content": utils.read_prompt_file('system.txt')},
            {"role": "user", "content": user_content},
        ],
        max_tokens = MAX_TOKENS,
    )

    reply = response.choices[0].message["content"].strip()
    MESSAGE_HISTORIES[channel_id].append(reply)
    await ctx.message.delete() # make sure to give bot manage messages permission
    try:
        await bot.user.edit(username=ctx.author.global_name, avatar=(await ctx.author.avatar.read()))
    except:
        print("Avatar error. Message:", reply)
    await ctx.send(f"{reply}")

bot.run("")
