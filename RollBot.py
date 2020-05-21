import random
import string
import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='/')

global NAMES

NAMES = []


@client.event
async def on_ready():
    print('RollBot is ready!')
    global roll_channel


@client.command()
async def roll(ctx, max: int):
    # Get the server channel to send the "user rolled # out of #" message to
    roll_channel = client.get_channel(700426150329057340)

    # Get the random roll number from 1 to the number that was inputed
    rolled = random.randint(1, max)

    # If the user that is rolling does not have their name in the list
    if ctx.message.author.name not in NAMES:

        # Send the "User rolled # out of #" message to the admin channel
        await roll_channel.send(f"{ctx.message.author.mention} has rolled a " + str(rolled) + " out of " + str(max))

        # Add the user's name to the list so they can not reroll
        NAMES.append(ctx.message.author.name)

        # This is for debugging purposes
        print(NAMES)

        # This is for the fun of it
        counter = open("counter.txt", "r")

        iC = counter.readline()
        iC = int(iC)
        iC += 1
        counter = open("counter.txt", "w")
        counter.write(str(iC))
        counter.close()

    else:

        # If the name already exists in the list, send this message to the user
        await ctx.message.author.send(
            "Sorry, but you've already rolled in the Togethearn raffle. If there has been a mistake, please contact the Togethearn staff.")


@client.command()
async def rem(ctx, name: str):
    # This will give us the User ID without "<", ">", and "@"
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace("@", "")

    # This gets the role from the server
    role = discord.utils.get(ctx.guild.roles, name="RBAs")

    # This returns the user's name
    user = client.get_user(int(name))
    username = user.name

    # If the role of the user matches the required role
    if role in ctx.author.roles:

        # If the username exists in the list
        if username in NAMES:

            # Remove the name from the list
            NAMES.remove(username)

            # For debugging purposes
            print(NAMES)

        else:

            # If the user does not exist on the list, send this message
            await ctx.author.send("The user " + username + " has not yet rolled.")


@client.command()
async def list(ctx):
    role = discord.utils.get(ctx.guild.roles, name="RBAs")

    if role in ctx.author.roles:
        await ctx.send(NAMES)


@client.command()
async def clear(ctx):
    role = discord.utils.get(ctx.guild.roles, name="RBAs")

    if role in ctx.author.roles:
        NAMES.clear()
        await ctx.author.send("The list has been cleared.")


client.run(os.environ['TOKEN'])
