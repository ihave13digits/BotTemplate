import random

from discord.ext import commands
from discord import Color, Embed

###############
###############
###         ###
### Globals ###
###         ###
###############
###############

TOKEN = "" # Your Discord Application Token
OWNER = 0 # Your User ID
INTRO = "welcome" # Desired Welcome Channel Name
SECRET = "secret" # Desired Moderation Channel Name (Make Private)
PREFIX = "!" # Desired Prefix For Commands

bot = commands.Bot(command_prefix=PREFIX)

image = {
        'bot' : "",
        }

help_dict = {
        # Help
        'help' : "This is a command!",
        'shutdown' : "Ends the current session."
        }

react_dict = {
        # Very Welcomed Speech
        'open source' : {
            'offense' : -2,
            'trigger' : 'open source',
            'warning' : ["The best source!"],
            },

        # Welcomed Speech
        'freeware' : {
            'offense' : -1,
            'trigger' : 'freeware',
            'warning' : ["Sharing is caring!"],
            },

        # Reaction Words
        'git' : {
            'offense' : 0,
            'trigger' : 'git',
            'warning' : ["I'm on Github too!"],
            },

        # Slightly Offensive
        'php' : {
            'offense' : 1,
            'trigger' : 'php',
            'warning' : ["I'm sorry to hear that!"],
            },

        # Really Offensive
        'closed source' : {
            'offense' : 2,
            'trigger' : 'closed source',
            'warning' : ["Your message has been deleted, {}!"],
            },
        }

welcome = {
        'sm' : [
            # server, member
            'Welcome to {}, {}!',
            ],
        'ms' : [
            # server, member
            "{} just joined {}!",
            ],
        'm' : [
            # member
            'Welcome, {}!',
            ]
        }

welcome_types = ['sm', 'ms', 'm']



########################
########################
###                  ###
### Helper Functions ###
###                  ###
########################
########################

### Gets Help Info ###
def helper(a):
    color_choice = random.randint(0, 16777215)
    embed=Embed(title="Help", color=color_choice)
    if not a:
        for f in help_dict:
            embed.add_field(name=f, value=help_dict[f], inline=False)
    else:
        embed.add_field(name=f, value=help_dict[a[0]], inline=False)
    embed.set_footer(text="End")
    return embed



#####################
#####################
###               ###
###  Start Async  ###
###               ###
#####################
#####################

### Connect ###
@bot.event
async def on_ready():
    print("Bot Ready!")


### Welcome Message ###
@bot.event
async def on_member_join(member):
    response = ""
    srvr = member.guild
    for chnl in srvr.channels:
        if chnl.name == INTRO:
            channel = bot.get_channel(chnl.id)
            wt = random.choice(welcome_types)
            if wt == "ms":
                response = random.choice(welcome[wt]).format(member.mention, srvr.name)
            if wt == "sm":
                response = random.choice(welcome[wt]).format(srvr.name, member.mention)
            if wt == "m":
                response = random.choice(welcome[wt]).format(member.mention)
            await channel.send(response)
        text = "\x1b[{};2;{};{};{}m".format(38, 255, 0, 255) + response + '\x1b[0m'
        print("{}: {}".format(member.id, text))


### Moderation ###
@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    offense = 0
    r, g, b = 0, 255, 0
    
    if message.author == bot.user:
        return
    else:
        # Check For Command
        if not message.content.startswith(PREFIX):
            for word in react_dict:
                if word in message.content.lower():
                    offense = react_dict[word]['offense']
                    response = random.choice(react_dict[word]['warning']).format(message.author.mention)
                    await ctx.send(response)
                
                    # Set Offense Color
                    if react_dict[word]['offense'] == -2:
                        r, g, b = 0, 0, 255
                    if react_dict[word]['offense'] == -1:
                        r, g, b = 0, 255, 255
                    if react_dict[word]['offense'] == 0:
                        r, g, b = 0, 255, 0
                    if react_dict[word]['offense'] == 1:
                        r, g, b = 255, 255, 0
                    if react_dict[word]['offense'] == 2:
                        r, g, b, = 255, 0, 0
                        await message.delete()
        else:
            r, g, b = 255, 255, 255

    # Private Channel Messages
    color_tag = Color.from_rgb(r, g, b)
    private_message = Embed(title=message.author.name, color=color_tag)
    try:
        private_message.add_field(name=message.channel.name, value=message.content, inline=False)
        for chnl in message.author.guild.channels:
            if chnl.name == SECRET:
                private_channel = bot.get_channel(chnl.id)
                await private_channel.send(embed=private_message)
    except:
        # Protect Against Crash From Bot DMs
        pass

    # Allow Commands
    await bot.process_commands(message)


### Shutdown ###
@bot.command(name='shutdown')
async def shutdown(ctx):
    can_do = False
    response = "You're not my owner!  Only an owner can use that command!"
    if ctx.author.id == OWNER:
        response = "Okay, {}!  See you soon!".format(ctx.author.name)
        can_do = True
    await ctx.send(response)
    if can_do:        
        print("Shutting down...")
        await bot.close()


### Help ###
bot.remove_command('help')
@bot.command(name='help')
async def send_help(ctx, *a):
    response=helper(a)
    await ctx.send(embed=response)

bot.run(TOKEN)
