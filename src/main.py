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


@bot.command(name='convert')
async def convert(ctx, *args):
    message = ctx.message
    if len(message.attachments) == 0:
        await ctx.channel.send('No attachment found. Type `!convert` in the message box and attach a replay file.')
    elif len(message.attachments) > 1:
        await ctx.channel.send('More than one attachment found. `!convert` accepts only one replay file at a time.')
    else:
        await ctx.channel.send('Converting replay')
        
        # Clear replays, then download replay file from discord to ~/edoprovid/ProjectIgnis/replay/
        os.system('rm ' + os.path.join(edopro_path, 'replay/*'))
        replay_name = message.attachments[0].filename
        replay = await message.attachments[0].save(os.path.join(edopro_path, f'replay/{replay_name}'))
        
        # Maximize EDOPro window and enter replay
        os.system("wmctrl -r 'Project Ignis: EDOPro' -e 0,0,0,1000,600")
        os.system("wmctrl -a 'Project Ignis: EDOPro'")
        time.sleep(0.5)
        pyautogui.click(573, 393)  # Click replays button
        time.sleep(0.5)
        pyautogui.click(340, 181)  # Select first replay
        time.sleep(0.5)
        pyautogui.click(802, 501)  # Enter replay
        pyautogui.moveTo(10, 10)   # Move mouse away from screen

        # Start subprocess for ffmpeg screen recording
        rec = subprocess.Popen(f'ffmpeg -y -video_size 690x580 -framerate 24 -f x11grab -i :1.0+374,67 -pix_fmt yuv420p -c:v libx264 -crf 35 -preset ultrafast -an {vid_path}', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)  # change codec to work on mobile
	    
	    # Detect when replay is finished (the "replay ended" box appears)
        x, y, w, h = 644, 274, 244, 61
        total, div = 1, 4  # (total) seconds of solid white, checking every (total/div) seconds
        white = Image.new('RGB', (w, h), (255, 255, 255))
        count = 0
        while count < div:
            time.sleep(total / div)
            section = pyautogui.screenshot(region=(x, y, w, h))
            count = (count + 1) * (section == white)  # chat, is this faster than an if-statement?
	    
        # End ffmpeg screen recording and upload video to discord
        rec.communicate(b'q\n')
        await ctx.channel.send(f'{message.author.mention}, your replay is ready.', file=discord.File(vid_path))
	        
        # Back to EDOPro main menu
        pyautogui.click(723, 361)  # Exit replay
        time.sleep(0.5)
        pyautogui.click(800, 541)  # Exit replay menu
        


if __name__ == "__main__":
    bot.run(os.environ['TOKEN'])
