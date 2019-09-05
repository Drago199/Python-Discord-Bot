import discord
from discord.ext import commands, tasks
from discord.utils import get
import youtube_dl
import os
import random
import asyncio

TOKEN = "NTkwMjEwNzcwOTY5NTU5MDY4.XQe9eA.ZRZXP63ed8BC-KXtboFMb87isSY"
BOT_PREFIX = ['!', '?', '.', '/']

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Epic Gamer Moments'))
    print('Bot is ready')
    print(f"Logged is as {bot.user.name}")
    print(f'Id: {bot.user.id}')
    print('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command')


@bot.command(brief='Get the latency of the bot')
async def ping(ctx):
    await ctx.send(f'Ping! {round(bot.latency * 1000)}ms')


@bot.command(brief='Delete a specified amound of messages')
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the amount of messages to delete.')


@bot.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    await ctx.send('Joining voice channel')

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(brief='Kick a member')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


@bot.command(brief='Ban a member')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@bot.command(brief='Unban a member')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return


@bot.command(brief='Bot says hello to you')
async def hello(message):
    await message.channel.send('Hello {0.author.mention}'.format(message))


@bot.command(brief='Dank')
async def ham(message):
    await message.channel.send('H A M B U R G E R')


@bot.command(brief='Play a guessing game')
async def guess(message):
    await message.channel.send('Guess a number between 1 and 10.')

    def is_correct(m):
        return m.author == message.author and m.content.isdigit()

    answer = random.randint(1, 10)

    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await message.channel.send('You took too long. The answer was {}.'.format(answer))

    if int(guess.content) == answer:
        await message.channel.send('Lucky guess!')
    if int(guess.content) > 10:
        await message.channel.send('That is not a number between 1 and 10, the answer was {}'.format(answer))
    else:
        await message.channel.send('Nope. It was {}.'.format(answer))


@bot.command(aliases=['8ball', 'eighball'], brief='Play 8ball')
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidely so.',
                 'Without a doubt.',
                 'Yes, Definitely.',
                 'You may rely on it.',
                 'As i see it, Yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again layer.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtfull',
                 'No.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@bot.event
async def on_message_delete(message):
    fmt = '**{0.author}** has YEETED the message: {0.content}'
    # fmt = '**{0.author.mention}** has YEETED the message: {0.content}'
    await message.channel.send(fmt.format(message))


@bot.event
async def on_message_edit(before, after):
    fmt = '**{0.author}** did an oopsie and edited their message:\n{0.content} -> {1.content}'
    # fmt = '**{0.author.mention}** did an oopsie and edited their message:\n{0.content} -> {1.content}'
    await before.channel.send(fmt.format(before, after))


bot.run(TOKEN)
