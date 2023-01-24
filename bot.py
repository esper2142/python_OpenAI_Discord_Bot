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


### Set up token, intents, and other global commands such as bot

TOKEN = 'INSERT TOKEN HERE'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

### follow an instagram user so your bot can post their content into a discord channel via webhook

INSTAGRAM_USERNAME = os.environ.get('GuyQuintero')

bot = commands.Bot(command_prefix='nelson ', intents=discord.Intents.all())

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
            webhook(os.environ.get("https://discord.com/api/webhooks/1067155503089725440/HQENXyEIB5D5_75XFGrnWbwe90Ma_XpS9pg2zLkG-FS57BdBgRhA9ZutgSd_z-XSwX44"),
                    get_instagram_html(INSTAGRAM_USERNAME))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if os.environ.get('IG_USERNAME') != None and os.environ.get('https://discord.com/api/webhooks/1067155503089725440/HQENXyEIB5D5_75XFGrnWbwe90Ma_XpS9pg2zLkG-FS57BdBgRhA9ZutgSd_z-XSwX44') != None:
        while True:
            main()
            time.sleep(float(os.environ.get('TIME_INTERVAL') or 600)) # 600 = 10 minutes
    else:
        print('Please configure environment variables properly!')

### establish connection with discord, and send a message to the channel specified and to the terminal

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready to spread the literary gospel!')
    channel = bot.get_channel(1022313760976806030)

    await channel.send(f'Hi, I am NelsonBot - and I predict there will be Solipsism in Syria caused by Globalists when America loses it\'s hedgemony. Please type \'nelson helpme\' to see how I can serve you, master!')

### when a member joins the discord, they will get mentioned with this welcome message and a message will be sent to the terminal

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1022313760976806030)
    await channel.send(f'Hi {member.name}, welcome to the Ditch Gang Discord server! I am your host, NelsonBot - and I predict there will be Solipsism in Syria caused by Globalists when America loses it\'s hedgemony. Please type \'nelson helpme\' to see how I can serve you, master!')
    print(f'member {member.name} has joined the server')


### commands for the bot to respond to

@bot.command()
async def helpme(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'''


        *************************************

        nelson <command>

        hello - I will greet you in the manner in which you are accustomed, you Obama loving Big pharma sponsor.
        helpme - You're seeing that right now, aren't you? Jesus...the liberals have no platform do they?
        quote - I will present you with a random bit of prose from the tortured asylum that is my mind. Can you handle it?
        guess - I will guess whether or not you are a libtard, or GOP scum.

        *************************************


        ''')

    print(f'Command {ctx.command} invoked by {ctx.author}')


@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}, you fuckin\' globalist donkey! \n (__)(__)====LLLL==D - - - - - - {ctx.author.name} \n \(that\'s a penis\)')
    
    print(f'Command {ctx.command} invoked by {ctx.author}')

@bot.command()
async def hi(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send(f'Salutations {ctx.author.name}, you fuckin\' globalist donkey! \n (__)(__)====LLLL==D - - - - - - {ctx.author.name} \n \(that\'s a penis\)')
    
    print(f'Command {ctx.command} invoked by {ctx.author}')

@bot.command()
async def quote(ctx):

    quote_list = [

### load quotes here

        'I fucked a turtle once.',
        'Dogs can\'t look up.',
        'Which one of you libtards farted on my grandma!?',
        'Crispr will replace all pharmaceutical drugs and therapies',
        'I will dominate our discourse with long-winded diatribes to impress upon you all my ability to use a thesaurus',
        'America will lose its hegemony as Russia cripples our economy with the ruble backed by the petrol dollar',
        'Trump 2024!',
        'Disney\'s stock will crumble due to woke ideology.',
        'I had a successful personal training business until Obama ruined the economy.',
        'Most Christians ignore the true books of the Bible, like the Book of Enoch.',
        'I don\'t respect Donald Trump, I just agree with a lot of his policies.',
        'If the Asian community gives into fear, they\'ll become susceptible like the black community, just like the real white supremacists want.',
        'Your cognitive dissonance hamster is on overdrive.',
        'Putin\'s next move will be humanitarian efforts, backed by a media blitz, absorbing the economic assets, and reinforcing the border with the help of Belarus. The humanitarian efforts taking priority until the population is docile and life returns to normal. Then his next move will be friendly acts to the rest of Eastern Europe, under the pretenses of assisting with their energy crisis.',
        'I\'m expecting Biden to completely tank the economy with spending (by passing congress to shell out student debt forgiveness) and market neglect or jump into WW3 by the end of the year, or both.',
        'If Putin wants to win this, he needs to level Kiev.',
        'I already told you to do research yourself. I\'ve given you a few. My sources aren\'t what\'s under scrutiny here. It\'s your inane accusations. There you go moving the goal posts again.',

        ]

    await ctx.send(random.choice(quote_list))

    print(f'Command {ctx.command} invoked by {ctx.author}')

@bot.command()
async def guess(ctx):
    party_list = [

### load party list here

        'You are a libtard, and deserve your mediocre existance wallowing in the mire and muck of mediocrity.',
        'You are a divine member of the MAGA political party. Infowars.com thanks you for your patronage, patriot!',
    ]
    await ctx.send(random.choice(party_list))

    print(f'Command {ctx.command} invoked by {ctx.author}')

bot.run(TOKEN)
