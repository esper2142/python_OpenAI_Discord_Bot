### written from scratch by Joshua King, 2023
### refer to github repo for more information https://github.com/esper2142/DiscordBot/

### import libraries needed for bot

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


### setup token, intents, and other global commands such as bot
### Replace INSERT_BOT_TOKEN_HERE with your discord bots generated token
### make sure your both is set up with the proper intents and permissions via discords developer interface

TOKEN = 'INSERT_BOT_TOKEN_HERE'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

### follow an instagram user so your bot can post their content into a discord channel via webhook
### find and change all instances of INSERT_IGRAM_USERNAME_HERE with the instagram username you wish to follow
### find and change all instances of INSERT_WEBHOOK_URL_HERE with the webhook URL you've created for your respective discord channel server
### find and change all instances of INSERT_CHANNEL_ID_HERE with the channel ID of the bot


INSTAGRAM_USERNAME = os.environ.get('INSERT_IGRAM_USERNAME_HERE')

### change the prefix to whatever you desire. Here we use the standard !
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

### establish webhook and channel for posting instagram messages

def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def webhook(webhook_url, html):
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "New pic of @"+INSTAGRAM_USERNAME+""
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    # embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    embed["thumbnail"] = {"url": get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def main():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        if(os.environ.get("LAST_IMAGE_ID") == get_last_publication_url(html)):
            print("Not new image to post in discord.")
        else:
            os.environ["LAST_IMAGE_ID"] = get_last_publication_url(html)
            print("New image to post in discord.")
            webhook(os.environ.get("INSERT_WEBHOOK_URL_HERE"),
                    get_instagram_html(INSTAGRAM_USERNAME))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if os.environ.get('INSERT_IGRAM_USERNAME_HERE') != None and os.environ.get('INSERT_WEBHOOK_URL_HERE') != None:
        while True:
            main()
            time.sleep(float(os.environ.get('TIME_INTERVAL') or 600)) # 600 = 10 minutes
    else:
        print('Please configure environment variables properly!')

### establish connection with discord, and send a message to the channel specified and to the terminal

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready to spread the literary gospel!')
    channel = bot.get_channel(INSERT_CHANNEL_ID_HERE)

    await channel.send(f'Hi! I\'m your friendly neighborhood Discord bot, and I\'m ready to go!')

### when a member joins the discord, they will get mentioned with this welcome message and a message will be sent to the terminal

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(INSERT_CHANNEL_ID_HERE)
    await channel.send(f'Hi {member.name}, welcome to theserver! Please type \'! helpme\' to see how I can serve you!')
    print(f'member {member.name} has joined the server')


### commands for the bot to respond to

@bot.command()
async def helpme(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'''


        *************************************
### change ! here if you used another prefix
        ! <command>

        hello - I will greet you
        helpme - You're seeing that right now, aren't you? 
        quote - I will present you with a random quote
        guess - I will guess something for you

        *************************************


        ''')

    print(f'Command {ctx.command} invoked by {ctx.author}')


@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}!')
    
    print(f'Command {ctx.command} invoked by {ctx.author}')

@bot.command()
async def hi(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}')
    
    print(f'Command {ctx.command} invoked by {ctx.author}')

@bot.command()
async def quote(ctx):

    quote_list = [

### load quotes here

        'Dogs can\'t look up.',
        'I like turtles.',
        
        ]

    await ctx.send(random.choice(quote_list))

    print(f'Command {ctx.command} invoked by {ctx.author}')

@bot.command()
async def guess(ctx):
    party_list = [

### load party list here

        'First guest response here!',
        'Second guest response here!',
    ]
    await ctx.send(random.choice(party_list))

    print(f'Command {ctx.command} invoked by {ctx.author}')

bot.run(TOKEN)
