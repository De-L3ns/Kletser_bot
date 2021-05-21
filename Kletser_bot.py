import discord
import random
import praw
import requests
import lists  # Stores large lists of data for certain commands.
from discord.ext import commands, tasks
from datetime import datetime

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category='Commands')
client = commands.Bot(command_prefix='!', intents=intents, help_command=help_command)
token = 'YOUR TOKEN HERE'
reddit = praw.Reddit(client_id='YOUR ID HERE',
                     client_secret='YOUR SECRET HERE',
                     username='YOUR USER HERE',
                     password='YOUR PASS HERE',
                     user_agent='YOUR AGENT HERE')
@client.event
async def on_ready():
    birthday_alert.start()
    print('KletserBot tot uw dienst.')

@tasks.loop(minutes=59)
async def birthday_alert():
    birthdays = lists.birthdays
    now = datetime.now()
    current_date = now.strftime("%d/%m")
    current_year = now.strftime("%Y")
    current_hour = now.strftime("%H")
    channel = client.get_channel(755014244247928924)
    message_30 = ['Tis voorbij voor u, de 30 is bereikt.']
    message_under_30 = ['Zo oud worden, aleh proficiat er mee hé.',
                        'Jahwadde ze, da begint al te tellen.',
                        ]
    message_over_30 = ['Dienen, voorbij de 30... Misschien stillekes aan inschrijven op de wachtlijst van het rusthuis?',
                       'In de ogen van de nieuwe generatie zijt gij echt wel al nen ouden ze.',
                       ]
    if int(current_hour) == 12:
        for name, date in birthdays.items():
            if current_date == date[:-5]:
                age = int(current_year) - int(date[-4:])
                if age == 30:
                    await channel.send(
                        f'@everyone {name} is vandaag geboren.\nGelukkige verjaardag, {name}! {random.choice(message_30)}')
                elif age >= 30:
                    await channel.send(
                        f'@everyone {name} is vandaag geboren.\nGelukkige verjaardag, {name}! {age}!? {random.choice(message_over_30)}')
                else:
                    await channel.send(
                        f'@everyone {name} is vandaag geboren.\nGelukkige verjaardag, {name}! {age}!? {random.choice(message_under_30)}')

# Reaction roles by Emoji


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 805483795288948767:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('done')
            else:
                print('Member not found')
        else:
            print('Role not found')

    # De mol minigame - 5 euro bets
    candidate_names = {'Annelotte': 830439131083046952,
                       'Jasmien': 830439147843485697,
                       'Katrien': 830439164654125066,
                       'Lennart': 830439182647558214,
                       'Philip': 830439211034607638,
                       'Samina': 830439233826324532,
                       'Sven': 830439244144967710,
                       'Dami': 830439260850094080,
                       'Jens': 830439376080207873,
                       'Kevin': 830439397329207347,
                       'Noah': 830439403909939250,
    }

    bets = {'Laurens' : 'Annelotte',
            'Joachim': 'Samina',
            'Kobe': 'Jasmien',
            'Max': 'Philip',
            'Leander': 'Lennart',
            'Matthieu': 'Samina',
    }


    channel_id = 830438815595364372
    channel = await client.fetch_channel(channel_id)

    for candidate, id in candidate_names.items():

        if payload.message_id == id and str(payload.emoji) == "❌":
            await channel.send(f'{candidate} ligt uit De Mol.')
            print('works')
            for name, bet in bets.items():
                if bet == candidate:
                    await channel.send(f'{name} dacht dat dit de mol was, bye bye 5 flappen.')

        if payload.message_id == id and str(payload.emoji) == "✅":
            await channel.send(f'{candidate} IS DE MOL!')
            for name, bet in bets.items():
                if bet == candidate:
                    await channel.send(f'{name} dacht dat dit de mol was en wint de gigantische prijzenpot!.')



@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 805483795288948767:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('done')
            else:
                print('Member not found')
        else:
            print('Role not found')

# Citaat command
@client.command()
async def citaat(context):
    citaten = lists.citaten
    await context.send(f'*{random.choice(citaten)}*')

# Question command
@client.command()
async def vraag(context, *, question):
    answers = lists.answers
    username = context.message.author
    special_user = username.name
    special_message = "18mm."
    message = 'lens'

    if message in question.lower():
        await context.send(f'Vraag: {question}\nAntwoord: {context.message.author.mention} L3ns is gewoon nen zotten baas.')

    elif special_user == 'Fabn':

        await context.send(f'Vraag: {question}\nAntwoord: {context.message.author.mention}{special_message} {random.choice(answers)}')

    else:
        await context.send(f'Vraag: {question}\nAntwoord: {context.message.author.mention} {random.choice(answers)}')

# Commands that use Imgur API
# Commands that use Reddit API

@client.command()
async def nostalgie(context):
    client_id = "YOUR CLIENT ID"
    album_key = "YOUR ALBUM ID"
    r = requests.get(f"https://api.imgur.com/3/album/{album_key}/images?client_id={client_id}").json()
    pictures = []

    for picture in r['data']:
        pictures.append(picture['link'])

    selected_picture = random.choice(pictures)
    em = discord.Embed(title="Eentje uit de oude doos")
    em.set_image(url = selected_picture)
    await context.send(embed = em)

@client.command()
async def meme(context):
    subreddit = reddit.subreddit("memes")
    all_posts = []
    hot = subreddit.hot(limit = 25)
    for post in hot:
        all_posts.append(post)
    random_post = random.choice(all_posts)
    name = random_post.title
    url = random_post.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await context.send(embed = em)

@client.command()
async def karen(context):
    subreddit = reddit.subreddit('fuckyoukaren')
    all_posts = []
    hot = subreddit.hot(limit = 25)
    for post in hot:
        all_posts.append(post)
    random_post = random.choice(all_posts)
    name = random_post.title
    url = random_post.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await context.send(embed = em)

@client.command()
async def office(context):
    subreddit = reddit.subreddit('DunderMifflin')
    all_posts = []
    hot = subreddit.hot(limit = 25)
    for post in hot:
        all_posts.append(post)
    random_post = random.choice(all_posts)
    name = random_post.title
    url = random_post.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await context.send(embed = em)

# Help commands

@client.command(hidden=True)
async def rollenhulp(context):
    text = lists.rollenhulp
    await context.send(f"**{text}**")

@client.command(hidden=True)
async def introductie(context):
    title = "@everyone\n--> KletserBOT tot uw dienst!"
    purpose = "What is my purpose?"
    text = lists.introductietekst
    exit = "--> KletserBOT OUT"

    await context.send(f"*{title}*\n**{purpose}**\n{text}\n*{exit}*")

@client.command()
async def uitleg(context):
    title = "Hoe werkt KletserBOT?"
    text = lists.uitlegtekst
    await context.send(f"**{title}**\n{text}")

client.run(token)

