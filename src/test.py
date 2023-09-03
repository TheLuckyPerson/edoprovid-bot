from collections import deque
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from PIL import Image
import pyautogui
import subprocess
import time

load_dotenv()

prefix = '!'  # Can change this later
vid_path = '/tmp/output.mp4'
edopro_path = os.path.expanduser('~/ProjectIgnis')
FPS = 10  # Can change this later, but this is probably the max for remote desktop'
w, h = 1440, 816  # equivalent to full screen on mac

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')


@bot.command(name='load')
async def load(ctx, *args):
    message = ctx.message
    if len(message.attachments) == 0:
        await ctx.channel.send('No attachment found. Type `!load` in the message box and attach a replay file.')
    elif len(message.attachments) > 1:
        await ctx.channel.send('More than one attachment found. `!load` accepts only one replay file at a time.')
    else:
        await ctx.channel.send('Loading replay')
        
        # Clear replays, then download replay file from discord to ~/edoprovid/ProjectIgnis/replay/
        os.system('rm ' + os.path.join(edopro_path, 'replay/*'))
        replay_name = message.attachments[0].filename
        replay = await message.attachments[0].save(os.path.join(edopro_path, f'replay/{replay_name}'))
        
        # Maximize EDOPro window 
        os.system("wmctrl -r 'Project Ignis: EDOPro' -b add,fullscreen")
        os.system("wmctrl -a 'Project Ignis: EDOPro'")


@bot.command(name='click')
async def click(ctx, *args):
    # Click at position defined by args
    os.system('rm /tmp/screen.png')
    pyautogui.click(int(args[0]), int(args[1]))
    time.sleep(0.5)
    img = pyautogui.screenshot('/tmp/screen.png')
    await ctx.channel.send(file=discord.File('/tmp/screen.png'))



if __name__ == "__main__":
    bot.run(os.environ['TOKEN'])
