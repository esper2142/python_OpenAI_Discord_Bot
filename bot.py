# Written by esper2142. Visit repo for more information: https://github.com/esper2142
# Please be sure to edit .env with your tokens.

import os
import discord
import random
import openai
from dotenv import load_dotenv
from pathlib import Path
from discord.ext import commands

# Load in the .env file if it's found. Otherwise, fallback to the runtime env variables
load_dotenv()

### Set up intents and OpenAI key.
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
openai.api_key = os.environ.get("OPENAI_TOKEN")

# This makes the default prefix '!'. Change it to whatever you want.
# Please note we are also removing case sensitivity from commands themselves. Remove this for a performance increase if you don't care.
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=discord.Intents.all())
quotes = []


# Establish connection with discord, and send a message to the terminal, then your specified channel ID.
@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    channel = bot.get_channel(int(os.environ.get("DISCORD_CHANNEL_ID")))

    await channel.send(f'Hello, world!')


# When a member joins the discord, they will get mentioned with this welcome message and a message will be sent to the terminal
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(os.environ.get("DISCORD_CHANNEL_ID")))
    await channel.send(f'Hi {member.name}, welcome to the Discord server!')
    print(f'member {member.name} has joined the server')


# Helpme command which lists all other commands the bot will respond to
@bot.command()
async def helpme(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'''


        *************************************

        ! <command>

        hi or hello - I will greet you.
        helpme - You're seeing that right now, aren't you?
        quote - I will present you with a random quote.
        guess <yes or no question> - I will make a guess at a question you ask me.
        gpt <question> - I will pass your question to ChatGPT for a response.
        image - I will post a random image from my databanks.
        
        *************************************


        ''')

    print(f'Command {ctx.command} invoked by {ctx.author}')


# Standard greeting command
@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}!')

    print(f'Command {ctx.command} invoked by {ctx.author}')


# Adding 'hi' as well as hello
@bot.command()
async def hi(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}')

    print(f'Command {ctx.command} invoked by {ctx.author}')


# Here we have the code for openAI. By default it will use the most robust response algorithm, text-davinci-003.
# It will also respond to 'gpt'. Change as desired.
@bot.command()
async def gpt(ctx):
    if ctx.author == bot.user:
        return

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{ctx.message.content}",
        max_tokens=2048,
        temperature=0.5,
    )

    await ctx.channel.send(response.choices[0].text)
    print(f'Command {ctx.command} invoked by {ctx.author}')


# A list of your favorite quotes. Load the quotes file into a random order. Reloads the list once empty

@bot.command()
async def quote(ctx):
    global quotes

    if (len(quotes) == 0):
        f = open(os.environ.get("DISCORD_QUOTE_FILE"))
        quotes = f.read().splitlines()
        random.shuffle(quotes)

    await ctx.send(quotes.pop())
    print(f'Command {ctx.command} invoked by {ctx.author}')


# A command to guess at a question you ask
@bot.command()
async def guess(ctx):
    guess_list = [

        # Load guess list here. All default guesses come from https://en.wikipedia.org/wiki/Magic_8_Ball

        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes, definitely.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don\'t count on it.',
        'My reply is no.',
        'My sources sy no.',
        'Outlook not so good.',
        'Very doubtful.'

    ]
    await ctx.send(random.choice(guess_list))

    print(f'Command {ctx.command} invoked by {ctx.author}')


# Grab a random image from the defined folder and send it
# Store files at a location of your choosing (defined in the .env file). example: /home/admin/scripts/DiscordBot/1.jpg
@bot.command()
async def image(ctx):
    async with ctx.typing():
        available_images = list(Path(os.environ.get("DISCORD_IMAGE_PATH")).rglob("*.jpg"))

        file = discord.File(fp=random.choice(available_images), filename='random_image.png')
        await ctx.channel.send(file=file)

    print(f'Command {ctx.command} invoked by {ctx.author}')


if __name__ == '__main__':
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
