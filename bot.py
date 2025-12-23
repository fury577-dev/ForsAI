import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"ForsAI is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("I’m here. Unfortunately for procrastination.")

@bot.command()
async def help(ctx):
    message = (
        "📖 **ForsAI — Available Commands**\n"
        "`!ping` — Check if I’m awake\n"
        "`!help` — Display this message\n\n"
        "More functions will be added when necessary."
    )
    await ctx.send(message)

if __name__ == "__main__":
    bot.run(TOKEN)
