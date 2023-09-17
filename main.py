from discord import Intents  # Import the Intents class
import openai
from discord.ext import commands
import utils

MESSAGE_HISTORY = []
MAX_TOKENS = 500

bot = commands.Bot(intents=Intents.all(), command_prefix='!')
openai.api_key = ""

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.event
async def on_message(message):
    if message.content.split()[0] != "!reply":
        print("Adding message to history:", message.content)
        MESSAGE_HISTORY.append(message.content)
    await bot.process_commands(message)

@bot.command()
async def reply(ctx: commands.Context):
    if not MESSAGE_HISTORY:
        messages = [msg async for msg in ctx.channel.history(limit=10)]
        for msg in messages:
            # if msg.author == ctx.author and msg.content != "!reply":
            print("Adding message to history, first call:", msg.content)
            MESSAGE_HISTORY.append(f"{msg.author}: {msg.content}")
    user_messages = "\n".join(MESSAGE_HISTORY)
    print("user messages:", user_messages)

    instructions = utils.read_prompt_file('instructions.txt')
    who_is = f"The person replying to the following conversation is {ctx.author.global_name}."

    user_content = f"{instructions} \n {who_is} \n {user_messages}" 

    # TODO: Are the messages being addded to the history backwards
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
    MESSAGE_HISTORY.append(reply)
    await ctx.message.delete() # make sure to give bot manage messages permission
    await bot.user.edit(username=ctx.author.global_name, avatar=(await ctx.author.avatar.read()))
    await ctx.send(f"[Mimicking {ctx.author.global_name}]: {reply}")

bot.run("")
