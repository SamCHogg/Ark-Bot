import logging
import os
import platform
import subprocess
import sys
import typing

import discord
from discord.ext.commands import Bot, CommandError, has_permissions

from blueprint_spins import do_multiple_spins
from reset_mindwipe import reset_user_mindwipes

# Config.py setup
##################################################################################
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")

else:
    import config  # config.py is required to run; found in the same directory.
##################################################################################

# This code logs all events including chat to discord.log. This file will be overwritten when the bot is restarted - rename the file if you want to keep it.

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=config.logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# IMPORTANT - DO NOT TOUCH! Setup bot as "bot", with description and prefix from config.py
bot = Bot(description=config.des, command_prefix=config.pref)

screen_session = "Ark-Server-Manager"

check_screen = subprocess.run(['screen', '-S', screen_session, '-Q', 'select', '.'])
if check_screen.returncode == 0:
    print("Found existing screen")
else:
    subprocess.run(['screen', '-dmS', screen_session])

# This message lets us know that the script is running correctly
print("Connecting...")


def async_subprocess_call(cmd):
    # Do the janky screen magic to stop server being killed when bot is killed
    subprocess.Popen(['screen', '-S', screen_session, '-p', '0', '-X', 'stuff', '{}\n'.format(cmd)])


@bot.event
async def on_ready():
    print("Bot online!")
    print("Discord.py API version:", discord.__version__)
    print("Python version:", platform.python_version())
    print("Running on:", platform.system(),
          platform.release(), "(" + os.name + ")")
    print("Name : {}".format(bot.user.name))
    print("ID : {}".format(bot.user.id))
    print("Currently active on " + str(len(bot.guilds)) + " servers.")
    print("")
    logger.info("Bot started successfully.")


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(config.err_mesg)


@bot.command(pass_context=True)
async def ping(ctx):
    """
    Ping the bot to make sure he's awake
    """
    latency = bot.latency
    await ctx.send(latency)


@bot.command()
@has_permissions(administrator=True)
async def update(ctx, instance: typing.Optional[str] = "@all"):
    """
    Forcefully updates the ARK Server
    """
    await ctx.send("Players currently on the server will be warned before the server is stopped.")
    async_subprocess_call('arkmanager update {} --warn --update-mods --force'.format(instance))


@bot.command()
@has_permissions(administrator=True)
async def restart(ctx, instance: typing.Optional[str] = ""):
    """
    Restarts the ARK Server
    """
    if instance != "":
        instance = "@" + instance
    await ctx.send("Restarting server...")
    await ctx.send("Players currently on the server will be warned before the server is stopped.")
    async_subprocess_call('arkmanager restart {} --warn'.format(instance))


@bot.command()
@has_permissions(administrator=True)
async def stop(ctx, instance: typing.Optional[str] = ""):
    """
    Stops the ARK Server
    """
    if instance != "":
        instance = "@" + instance
    await ctx.send("Stopping server...")
    await ctx.send("Players currently on the server will be warned before the server is stopped.")
    async_subprocess_call('arkmanager stop {} --warn'.format(instance))


@bot.command()
@has_permissions(administrator=True)
async def start(ctx,  instance: typing.Optional[str] = ""):
    """
    Starts the ARK Server
    """
    if instance != "":
        instance = "@" + instance
    await ctx.send("Starting server...")
    async_subprocess_call('arkmanager start {}'.format(instance))


@bot.command()
async def list_mods(ctx):
    """
    Lists mods installed on the server
    """
    mods_dir = "{}/ShooterGame/Content/Mods/".format(config.ark_install_dir)
    command = subprocess.check_output(
        ["find", mods_dir, '-name', '*.mod']
    )
    command_output = command.decode('UTF-8')

    mods = ""
    for line in command_output.splitlines():
        if mods != "":
            mods += ", "
        mods += line.replace(mods_dir, '').replace('.mod', '')

    output = "Current Mods: \n"+mods
    await ctx.send(output)


@bot.command()
@has_permissions(administrator=True)
async def listplayers(ctx):
    """
    List players on the ARK Server
    """
    try:
        command = subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'listplayers']
        )
    except subprocess.CalledProcessError as e:
        command = e.output
    command_output = command.decode('UTF-8')
    await ctx.send('```' + command_output + '```')


@bot.command()
@has_permissions(administrator=True)
async def whitelist(ctx, steam_id):
    """
    Add player to ARK server whitelist
    """
    try:
        command = subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'AllowPlayerToJoinNoCheck {}'.format(steam_id)]
        )
    except subprocess.CalledProcessError as e:
        command = e.output
    command_output = command.decode('UTF-8')
    await ctx.send('```' + command_output + '```')


@bot.command()
@has_permissions(administrator=True)
async def unwhitelist(ctx, steam_id):
    """
    Remove player from ARK server whitelist
    """
    try:
        command = subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'DisallowPlayerToJoinNoCheck {}'.format(steam_id)]
        )
    except subprocess.CalledProcessError as e:
        command = e.output
    command_output = command.decode('UTF-8')
    await ctx.send('```' + command_output + '```')


@bot.command()
@has_permissions(administrator=True)
async def ban(ctx, steam_id):
    """
    Bans player from the ARK server
    """
    try:
        subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'DisallowPlayerToJoinNoCheck {}'.format(steam_id)]
        )
    except subprocess.CalledProcessError as e:
        pass
    try:
        command = subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'BanPlayer {}'.format(steam_id)]
        )
    except subprocess.CalledProcessError as e:
        command = e.output
    try:
        subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'KickPlayer {}'.format(steam_id)]
        )
    except subprocess.CalledProcessError as e:
        pass
    command_output = command.decode('UTF-8')
    await ctx.send('```' + command_output + '```')


@bot.command()
@has_permissions(administrator=True)
async def unban(ctx, steam_id):
    """
    Un-bans player from the ARK server
    """
    try:
        command = subprocess.check_output(
            ['arkmanager', 'rconcmd', '@all', 'UnbanPlayer {}'.format(steam_id)]
        )
    except subprocess.CalledProcessError as e:
        command = e.output
    command_output = command.decode('UTF-8')
    await ctx.send('```' + command_output + '```')


@bot.command()
@has_permissions(administrator=True)
async def spins(ctx, number_of_rolls: int):
    """
    Do a blueprint spin
    """
    output = do_multiple_spins(number_of_rolls)
    await ctx.send('```' + output + '```')


@bot.command()
@has_permissions(administrator=True)
async def reset_mindwipes(ctx, steam_id):
    """
    Resets the mindwipe allowance of a given player
    """
    await ctx.send("Make sure that the user is logged out of the server!")
    await ctx.send("Backing up server first...")
    async_subprocess_call('arkmanager backup')
    await ctx.send("Now resetting mindwipe allowance for {}...".format(steam_id))
    reset_user_mindwipes(steam_id, "{}/ShooterGame/Saved/SavedArks/".format(config.ark_install_dir))
    await ctx.send("Mindwipe allowance reset for {}".format(steam_id))

# Read bot token from "config.py" (which should be in the same directory as this file)
bot.run(config.bbtoken)
