# 🤖 ForsAI

ForsAI is a **personal Discord AI assistant** inspired by *Fors Wall* from **Lord of the Mysteries**.
She is designed to be calm, slightly sarcastic, efficient, and actually useful — not a noisy gimmick bot.

Built as a learning + portfolio project, ForsAI combines:

* Persistent user memory
* Short-term conversational context
* External AI reasoning (Zukijourney)
* Clean GitHub-safe architecture

---

## ✨ Features

### 🧠 AI Chat (`!ask`)

* Ask questions in **DMs or servers**
* Uses Zukijourney AI for intelligent responses
* Maintains **short-term conversation memory** per user
* Persona-driven replies (Fors Wall–inspired)

Example:

```
!ask explain recursion
!ask give a python example
```

---

### 🗂️ Short-Term Context Memory

* Remembers last few AI messages per user
* Improves follow-up answers
* Automatically trimmed (FIFO)
* Stored in RAM only (privacy-safe)

Clear context anytime:

```
!clearcontext
```

---

### 📝 Personal Notes System

* Notes are **per-user** and persistent
* Stored locally in `memory.json`

Commands:

```
!note buy milk
!notes
!delnote 1
```

---

### 🔐 Secure by Design

* Secrets stored in `.env` (never committed)
* `.gitignore` protects API keys
* `.env.example` included for setup

---

## 🛠️ Tech Stack

* **Python 3.11+**
* **discord.py**
* **Zukijourney API**
* **python-dotenv**
* **requests**

---

## 📂 Project Structure

```
ForsAI/
├── bot.py
├── memory.json
├── personality/
│   └── persona.txt
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/ForsAI.git
cd ForsAI
```

### 2️⃣ Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

Create a `.env` file:

```env
DISCORD_TOKEN=your_discord_bot_token
ZUKI_API_KEY=your_zukijourney_api_key
```

### 4️⃣ Run the bot

```bash
python bot.py
```

---

## 📌 Commands Overview

| Command           | Description                  |
| ----------------- | ---------------------------- |
| `!ping`           | Check if ForsAI is online    |
| `!ask <question>` | Ask ForsAI anything          |
| `!clearcontext`   | Clear AI conversation memory |
| `!note <text>`    | Save a personal note         |
| `!notes`          | View your notes              |
| `!delnote <n>`    | Delete a note                |

---

## ⚠️ Notes

* AI context resets when the bot restarts
* Notes persist across restarts
* Designed primarily for **personal assistant use**

---

## 📜 Disclaimer

This project is for **educational and personal use**.
ForsAI is not affiliated with *Lord of the Mysteries* or its creators.

---

## 🌱 Future Plans

* Rate limiting
* Reminder system
* 24/7 cloud hosting
* Expanded memory controls

---

> *“Efficiency is mercy.”* — Fors Wall (probably)
