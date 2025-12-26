import json
import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# =========================
# ENV SETUP
# =========================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
ZUKI_API_KEY = os.getenv("ZUKI_API_KEY")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not found. Check your .env file.")

if not ZUKI_API_KEY:
    raise RuntimeError("ZUKI_API_KEY not found. Check your .env file.")

# =========================
# SHORT-TERM CONVERSATION MEMORY
# =========================
MAX_CONTEXT_MESSAGES = 6  # 3 user + 3 assistant
conversation_memory = {}

# =========================
# MEMORY SETUP (PERMANENT)
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
# PERSONA SETUP
# =========================
def load_persona():
    with open("personality/persona.txt", "r", encoding="utf-8") as f:
        return f.read()

# =========================
# ZUKIJOURNEY API (WITH CONTEXT)
# =========================
def zukijourney_chat(user_id, user_prompt):
    persona = load_persona()
    user_id = str(user_id)

    # Init memory for user
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []

    # Add user message
    conversation_memory[user_id].append({
        "role": "user",
        "content": user_prompt
    })

    # Trim old context
    conversation_memory[user_id] = conversation_memory[user_id][-MAX_CONTEXT_MESSAGES:]

    messages = [
        {"role": "system", "content": persona},
        *conversation_memory[user_id]
    ]

    headers = {
        "Authorization": f"Bearer {ZUKI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "zukigm-1",
        "messages": messages
    }

    response = requests.post(
        "https://api.zukijourney.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    reply = data["choices"][0]["message"]["content"]

    # Store assistant reply
    conversation_memory[user_id].append({
        "role": "assistant",
        "content": reply
    })

    # Trim again
    conversation_memory[user_id] = conversation_memory[user_id][-MAX_CONTEXT_MESSAGES:]

    return reply

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

@bot.command()
async def ask(ctx, *, question: str):
    await ctx.send("Thinking…")

    try:
        reply = zukijourney_chat(ctx.author.id, question)
        await ctx.send(reply)

    except Exception as e:
        await ctx.send("That was… troublesome. Try again later.")
        print("Zuki error:", e)

# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    bot.run(TOKEN)

