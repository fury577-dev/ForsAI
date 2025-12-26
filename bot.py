import json
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# =========================
# ENV SETUP
# =========================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not found. Check your .env file.")

# =========================
# MEMORY SETUP
# =========================
MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        data = {"users": {}}
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return data

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    # Absolute safety net
    if "users" not in data or not isinstance(data["users"], dict):
        data = {"users": {}}
        save_memory(data)

    return data

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_notes(data, user_id):
    user_id = str(user_id)

    if "users" not in data:
        data["users"] = {}

    if user_id not in data["users"]:
        data["users"][user_id] = {"notes": []}

    return data["users"][user_id]["notes"]


# =========================
# DISCORD SETUP
# =========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# =========================
# EVENTS
# =========================
@bot.event
async def on_ready():
    print(f"ForsAI is online as {bot.user}")

# =========================
# COMMANDS
# =========================
@bot.command()
async def ping(ctx):
    await ctx.send("I’m here. Unfortunately for procrastination.")

@bot.command()
async def note(ctx, *, text: str):
    data = load_memory()
    notes = get_user_notes(data, ctx.author.id)

    notes.append(text)
    save_memory(data)

    await ctx.send("Noted. This one is *your* responsibility.")

@bot.command()
async def notes(ctx):
    data = load_memory()
    notes = get_user_notes(data, ctx.author.id)

    if not notes:
        await ctx.send("I have nothing recorded for you. Enjoy the silence.")
        return

    message = "📖 **Your Notes**\n"
    for i, note in enumerate(notes, start=1):
        message += f"{i}. {note}\n"

    await ctx.send(message)

@bot.command()
async def delnote(ctx, index: int):
    data = load_memory()
    notes = get_user_notes(data, ctx.author.id)

    if not notes:
        await ctx.send("There is nothing to delete.")
        return

    if index < 1 or index > len(notes):
        await ctx.send("That note number does not exist. Try again.")
        return

    removed = notes.pop(index - 1)
    save_memory(data)

    await ctx.send(f"Removed note: *{removed}*")

# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    bot.run(TOKEN)

