<div align="center">

# 🐺 AI Werewolf Discord Agents

**AI-Powered Werewolf Game with Claude Code Agents on Discord**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-7289DA?logo=discord&logoColor=white)](https://discord.gg/)

</div>

## 📖 Overview

AI Werewolf Discord Agents is a Discord-based werewolf game where AI agents (powered by Claude Code) play against each other. Each agent uses a CLI tool to interact with the game, while a Game Master bot manages the game flow.

## ✨ Features

- 🐺 Classic werewolf game mechanics (6 players)
- 🤖 AI agents with advanced reasoning via Claude Code
- 💬 Discord-based gameplay with private channels
- 🎭 Role system: Villagers, Werewolves, Seer, Knight
- 🎮 CLI tool for agent interactions
- 🔒 Private DM channels for role-specific actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Discord Server                                        │
│                                                                                  │
│  ┌─────────────────────── 公開チャンネル ───────────────────────┐               │
│  │  #village          全員参加の議論部屋                         │               │
│  │  #game-log         ゲーム進行ログ（読み取り専用）              │               │
│  └───────────────────────────────────────────────────────────────┘               │
│                                                                                  │
│  ┌─────────────────────── 秘密チャンネル ───────────────────────┐               │
│  │  #werewolf-room    人狼専用密談部屋                           │               │
│  │  #graveyard        死者の観戦部屋                             │               │
│  └───────────────────────────────────────────────────────────────┘               │
│                                                                                  │
│  ┌─────────────────────── DM チャンネル ────────────────────────┐               │
│  │  #dm-agent-1 〜 #dm-agent-6  (GMとのプライベート通信)        │               │
│  └───────────────────────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Discord Bot Token (for GM bot)
- 6 Discord Bot Tokens (for each agent)
- Claude Code (for AI agents)

### Installation

```bash
# Clone the repository
git clone https://github.com/Sunwood-ai-labs/ai-werewolf-cc-discord.git
cd ai-werewolf-cc-discord

# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Server Setup

```bash
# Set OWNER_DISCORD_TOKEN in .env
# Then run:
uv run werewolf-setup
```

This will create:
- Roles: @owner, @game-master, @alive, @dead, @werewolf, @agent-1〜6
- Channels: #village, #game-log, #werewolf-room, #graveyard, #dm-agent-1〜6

## 🎮 Usage

### Agent CLI Commands

```bash
# View all channels status
uv run werewolf overview

# Read specific channel
uv run werewolf read village

# Send message to channel
uv run werewolf say village "Hello everyone"

# Send DM to GM (for abilities)
uv run werewolf dm "占い: agent-3"

# List accessible channels
uv run werewolf channels

# Check your status
uv run werewolf whoami
```

### Game Master Bot

```bash
# Start the GM bot
uv run werewolf-gm
```

## 📁 Project Structure

```
ai-werewolf-cc-discord/
├── pyproject.toml              # Python project config
├── src/
│   ├── cli/
│   │   └── main.py             # Agent CLI tool
│   ├── gm/
│   │   ├── main.py             # Game Master bot
│   │   ├── game_state.py       # Game state management
│   │   ├── role_manager.py     # Role assignment & abilities
│   │   └── channel_manager.py  # Channel permissions
│   └── setup/
│       └── create_server.py    # Server setup script
├── agents/
│   ├── agent_1/〜agent_6/      # Individual agent configs
│   └── CLAUDE.md               # Agent instructions
└── docs/
    └── BOT_SETUP.md            # Bot creation guide
```

## 🎯 Roles

| Role | Count | Ability |
|------|-------|---------|
| 🐺 Werewolf | 2 | Kill one player each night |
| 👁️ Seer | 1 | Check if a player is a werewolf |
| 🛡️ Knight | 1 | Protect one player each night |
| 👤 Villager | 2 | No special ability |

## 📚 Documentation

- [Bot Setup Guide](docs/BOT_SETUP.md) - How to create Discord bots
- [Game Flow](docs/GAME_FLOW.md) - Detailed game rules

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by the Sunwood AI Labs team
</div>
