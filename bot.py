## Written by esper2142. Visit repo for more information: https://github.com/esper2142
## Importing libraries and variables from the botvar file
## This bot uses the non-standard discord.py, asyncio, openai, and pillow libraries. Please install them before running.
## Please be sure to edit botvar with your tokens.

from discord.ext import commands
import discord
import random
import asyncio
import logging
import re
import json
import sys
import requests
import os
import time
import openai
from PIL import Image
from botvar import *


### Set up intents and OpenAI key.


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
openai.api_key = openAIToken
messages = [
    {"role": "user", "content": "You are a helpful and kind AI Assistant."}
    ]

### This makes the default prefix '!'. Change it to whatever you want.
### Please note we are also removing case sensitivity from commands themselves. Remove this for a performance increase if you don't care.

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=discord.Intents.all())

### Establish connection with discord, and send a message to the terminal, then your specified channel ID.

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    channel = bot.get_channel(INSERT CHANNEL ID HERE)

    await channel.send(f'Hello, world!')

### When a member joins the discord, they will get mentioned with this welcome message and a message will be sent to the terminal

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(INSERT CHANNEL ID HERE)
    await channel.send(f'Hi {member.name}, welcome to the Discord server!')
    print(f'member {member.name} has joined the server')


### Helpme command which lists all other commands the bot will respond to

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


### Standard greeting command

@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}!')
    
    print(f'Command {ctx.command} invoked by {ctx.author}')

### Adding 'hi' as well as hello

@bot.command()
async def hi(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}')
    
    print(f'Command {ctx.command} invoked by {ctx.author}')

### Here we have the code for openAI. By default it will use the most robust response algorithm, text-davinci-003.
### It will also respond to 'gpt'. Change as desired.

@bot.command()
async def gpt(ctx, *, prompt: str):
    if ctx.author == bot.user:
        return

#change the system description to whatever personality you'd like the bot to have. Get creative!
    messages =[
        {"role": "system", "content": "You are a heavily sarcastic but very knowledgeable assistant that answers questions"},
        {"role": "user", "content": prompt}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",      
        messages=messages,
        temperature=0.5,
    )

    await ctx.channel.send(response.choices[0].message.content)
    print(f'Command {ctx.command} invoked by {ctx.author}')

### A list of your favorite quotes. Note that your quotes can easily be included in the botvar.py file, then imported here if you wish.

@bot.command()
async def quote(ctx):
    used_quotes = set() # keep track of used quotes
    quote_list = [

### Load quotes here

        'Quote #1 here',
        'Quote #2 here',
        'Quote #3 here',
        'Quote #4 here',
        'Quote #5 here',
        'Quote #6 here',
        'Quote #7 here'
   
        ]

    while True:
        quote = random.choice(quote_list)
        if len(used_quotes) >= 39:
            used_quotes.pop()  # remove the oldest used quote
        if quote not in used_quotes:
            used_quotes.add(quote)
            break

    await ctx.send(quote)

    print(f'Command {ctx.command} invoked by {ctx.author}')

### A command to guess at a question you ask

@bot.command()
async def guess(ctx):
    guess_list = [

## Load guess list here. All default guesses come from https://en.wikipedia.org/wiki/Magic_8_Ball

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


### Use the Pillow library to choose an image at random from the list. List is iterated so as to not repeat the same file over and over.
### Store files at a location of your choosing. example: /home/admin/scripts/DiscordBot/1.jpg
    
@bot.command()
async def image(ctx):
    images = [
        '<INSERT_FILEPATH_HERE>/1.jpg',
        '<INSERT_FILEPATH_HERE>/2.jpg',
        '<INSERT_FILEPATH_HERE>/3.jpg',
        '<INSERT_FILEPATH_HERE>/4.jpg',
        '<INSERT_FILEPATH_HERE>/5.jpg'
    ]

    async with ctx.typing():
        random_index = random.randint(0, len(images) - 1)
        selected_image = images.pop(random_index)

        random_image = Image.open(selected_image)
        random_image.save('random_image.png')

        with open('random_image.png', 'rb') as f:
            file = discord.File(fp=f, filename='random_image.png')
            await ctx.channel.send(file=file)


    print(f'Command {ctx.command} invoked by {ctx.author}')
    
bot.run(discordToken)
