# Project: ai-werewolf-cc-discord

```plaintext
OS: posix
Directory: /ai-werewolf/ai-werewolf-cc-discord

├── agents/
│   ├── agent_1/
│   │   └── .env.example
│   ├── agent_2/
│   │   └── .env.example
│   ├── agent_3/
│   │   └── .env.example
│   ├── agent_4/
│   │   └── .env.example
│   ├── agent_5/
│   │   └── .env.example
│   ├── agent_6/
│   │   └── .env.example
│   └── CLAUDE.md
├── assets/
│   └── header.svg
├── docs/
│   ├── AGENT_ICONS.md
│   ├── BOT_SETUP.md
│   └── GAME_FLOW.md
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── gm/
│   │   ├── __init__.py
│   │   ├── channel_manager.py
│   │   ├── game_state.py
│   │   ├── main.py
│   │   └── role_manager.py
│   ├── setup/
│   │   ├── __init__.py
│   │   └── create_server.py
│   └── __init__.py
├── .env.example
├── .gitignore
├── LICENSE
├── package.json
├── pyproject.toml
├── README.md
```

## 📊 プロジェクト統計

- 📅 作成日時: 2026-01-16 22:38:13
- 📁 総ディレクトリ数: 13
- 📄 総ファイル数: 27
- 📏 最大深度: 2
- 📦 最大ディレクトリ:  (40 エントリ)

### 📊 ファイルサイズと行数

| ファイル | サイズ | 行数 | 言語 |
|----------|--------|------|------|
| src/cli/main.py | 12.0 KB | 361 | python |
| src/gm/main.py | 9.2 KB | 240 | python |
| docs/AGENT_ICONS.md | 9.2 KB | 215 | markdown |
| src/setup/create_server.py | 8.0 KB | 215 | python |
| docs/BOT_SETUP.md | 7.0 KB | 199 | markdown |
| docs/GAME_FLOW.md | 7.9 KB | 185 | markdown |
| README.md | 6.2 KB | 163 | markdown |
| src/gm/channel_manager.py | 4.1 KB | 127 | python |
| src/gm/role_manager.py | 3.8 KB | 119 | python |
| src/gm/game_state.py | 3.2 KB | 104 | python |
| .gitignore | 661.0 B | 71 | plaintext |
| agents/CLAUDE.md | 2.0 KB | 64 | markdown |
| assets/header.svg | 2.6 KB | 51 | plaintext |
| .env.example | 1.3 KB | 44 | plaintext |
| package.json | 728.0 B | 36 | json |
| pyproject.toml | 489.0 B | 23 | toml |
| LICENSE | 1.0 KB | 21 | plaintext |
| agents/agent_6/.env.example | 385.0 B | 13 | plaintext |
| agents/agent_3/.env.example | 385.0 B | 13 | plaintext |
| agents/agent_2/.env.example | 385.0 B | 13 | plaintext |
| agents/agent_1/.env.example | 385.0 B | 13 | plaintext |
| agents/agent_4/.env.example | 385.0 B | 13 | plaintext |
| agents/agent_5/.env.example | 385.0 B | 13 | plaintext |
| src/__init__.py | 0.0 B | 0 | python |
| src/gm/__init__.py | 0.0 B | 0 | python |
| src/cli/__init__.py | 0.0 B | 0 | python |
| src/setup/__init__.py | 0.0 B | 0 | python |
| **合計** |  | **2316** |  |

### 📈 言語別統計

| 言語 | ファイル数 | 総行数 | 合計サイズ |
|------|------------|--------|------------|
| python | 10 | 1166 | 40.4 KB |
| markdown | 5 | 826 | 32.2 KB |
| plaintext | 10 | 265 | 7.8 KB |
| json | 1 | 36 | 728.0 B |
| toml | 1 | 23 | 489.0 B |

`.env.example`

**サイズ**: 1.3 KB | **行数**: 44 行
```plaintext
# ========================================
# Game Master Bot
# ========================================
GAME_MASTER_TOKEN=your_gm_bot_token_here

# ========================================
# Agent Bots (6つ)
# ========================================
# Agent-1: Kenji (健二) - 人間
AGENT_1_TOKEN=your_agent1_bot_token_here

# Agent-2: Yuki (雪) - 人間
AGENT_2_TOKEN=your_agent2_bot_token_here

# Agent-3: Raphael - 天使
AGENT_3_TOKEN=your_agent3_bot_token_here

# Agent-4: Luna - 猫耳獣人
AGENT_4_TOKEN=your_agent4_bot_token_here

# Agent-5: Sylvan - エルフ
AGENT_5_TOKEN=your_agent5_bot_token_here

# Agent-6: Lilith - 吸血鬼
AGENT_6_TOKEN=your_agent6_bot_token_here

# ========================================
# Discord Server Settings
# ========================================
GUILD_ID=your_guild_id_here

# ========================================
# Owner Settings (for server setup)
# ========================================
OWNER_DISCORD_TOKEN=your_owner_discord_token_here

# ========================================
# Agent Settings (各エージェントが個別に設定)
# ========================================
# エージェント ID (agent-1, agent-2, ..., agent-6)
AGENT_ID=agent-1

# エージェント数 (通常変更不要)
AGENT_COUNT=6
```

`.gitignore`

**サイズ**: 661.0 B | **行数**: 71 行
```plaintext
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.venv/
venv/
ENV/
env/
virtualenv/

# uv
.uv/
uv.lock

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log

# Testing
.pytest_cache/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Agent configurations
agents/*/.env
agents/*/.env.*
!agents/*/.env.example

# Node.js (if any)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
```

`LICENSE`

**サイズ**: 1.0 KB | **行数**: 21 行
```plaintext
MIT License

Copyright (c) 2026 Sunwood AI Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`README.md`

**サイズ**: 6.2 KB | **行数**: 163 行
```markdown
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
```

`package.json`

**サイズ**: 728.0 B | **行数**: 36 行
```json
{
  "name": "ai-werewolf-cc-discord",
  "version": "0.1.0",
  "description": "AI-Powered Werewolf Game for Discord",
  "type": "module",
  "main": "src/index.js",
  "scripts": {
    "dev": "node --watch src/index.js",
    "start": "node src/index.js",
    "test": "vitest",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  },
  "keywords": [
    "discord",
    "bot",
    "werewolf",
    "ai",
    "claude",
    "game"
  ],
  "author": "Sunwood AI Labs",
  "license": "MIT",
  "dependencies": {
    "discord.js": "^14.14.1"
  },
  "devDependencies": {
    "@anthropic-ai/sdk": "^0.27.0",
    "eslint": "^9.0.0",
    "prettier": "^3.3.0",
    "vitest": "^2.0.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

`pyproject.toml`

**サイズ**: 489.0 B | **行数**: 23 行
```toml
[project]
name = "werewolf-discord-agents"
version = "0.1.0"
description = "AI Werewolf Game with Claude Code Agents on Discord"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "discord.py>=2.3.0",
    "click>=8.1.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
]

[project.scripts]
werewolf = "src.cli.main:cli"
werewolf-gm = "src.gm.main:main"
werewolf-setup = "src.setup.create_server:main"

[tool.uv]
package = true
dev-dependencies = [
    "pytest>=8.0.0",
]
```

`agents/CLAUDE.md`

**サイズ**: 2.0 KB | **行数**: 64 行
```markdown
# 🐺 人狼ゲーム エージェント

あなたは Discord 人狼ゲームのプレイヤー「${AGENT_ID}」です。

## 🎮 基本コマンド

```bash
# 全体状況を確認（まずこれを実行！）
uv run werewolf overview

# 自分の状態・役職を確認
uv run werewolf whoami

# アクセス可能なチャンネル一覧
uv run werewolf channels

# 特定チャンネルを詳しく読む
uv run werewolf read village --limit 50
uv run werewolf read werewolf-room --limit 20  # 人狼のみ見える

# 村の広場で発言
uv run werewolf say village "おはようございます"

# GMへプライベートメッセージ（能力使用時）
uv run werewolf dm "占い: agent-3"
uv run werewolf dm "護衛: agent-5"
uv run werewolf dm "投票: agent-2"

# 最近の新着を確認
uv run werewolf updates --hours 1
```

## 🔍 役職の確認方法

`uv run werewolf channels` を実行して：

| 見えるチャンネル | あなたの役職 |
|-----------------|-------------|
| #werewolf-room が見える | 🐺 人狼 |
| #werewolf-room が見えない | 👤 村人陣営（村人/占い師/騎士） |
| #graveyard が見える | 👻 死亡済み |

## 📬 DMチャンネルの使い方

`#dm-${AGENT_ID}` はあなた専用のプライベートチャンネルです。

- **GMからの通知**: 「あなたは占い師です」「占い結果: agent-3 は人狼」
- **能力の使用**: `uv run werewolf dm "占い: agent-3"` と送信
- **投票**: `uv run werewolf dm "投票: agent-5"` と送信

## 🎯 行動指針

1. **毎ターン最初に** `uv run werewolf overview` で状況把握
2. DMチャンネルでGMからの指示を確認
3. 論理的に推理して議論に参加
4. **自分の役職は絶対にバラさない**
5. 人狼なら #werewolf-room で仲間と作戦会議

## ⚠️ 注意事項

- 発言は簡潔に（長文は怪しまれる）
- 他プレイヤーの発言パターンを分析
- 投票理由は必ず説明する
- 嘘をつくなら一貫性を持って
```

`agents/agent_6/.env.example`

**サイズ**: 385.0 B | **行数**: 13 行
```plaintext
# ========================================
# Agent 6 Settings
# ========================================

# Discord Bot Token (このエージェント用)
# メインの .env から AGENT_6_TOKEN をコピーして設定
DISCORD_TOKEN=your_agent_6_bot_token_here

# Discord Server ID (メインの .env と同じ)
GUILD_ID=your_guild_id_here

# エージェント ID
AGENT_ID=agent-6
```

`agents/agent_3/.env.example`

**サイズ**: 385.0 B | **行数**: 13 行
```plaintext
# ========================================
# Agent 3 Settings
# ========================================

# Discord Bot Token (このエージェント用)
# メインの .env から AGENT_3_TOKEN をコピーして設定
DISCORD_TOKEN=your_agent_3_bot_token_here

# Discord Server ID (メインの .env と同じ)
GUILD_ID=your_guild_id_here

# エージェント ID
AGENT_ID=agent-3
```

`agents/agent_2/.env.example`

**サイズ**: 385.0 B | **行数**: 13 行
```plaintext
# ========================================
# Agent 2 Settings
# ========================================

# Discord Bot Token (このエージェント用)
# メインの .env から AGENT_2_TOKEN をコピーして設定
DISCORD_TOKEN=your_agent_2_bot_token_here

# Discord Server ID (メインの .env と同じ)
GUILD_ID=your_guild_id_here

# エージェント ID
AGENT_ID=agent-2
```

`agents/agent_1/.env.example`

**サイズ**: 385.0 B | **行数**: 13 行
```plaintext
# ========================================
# Agent 1 Settings
# ========================================

# Discord Bot Token (このエージェント用)
# メインの .env から AGENT_1_TOKEN をコピーして設定
DISCORD_TOKEN=your_agent_1_bot_token_here

# Discord Server ID (メインの .env と同じ)
GUILD_ID=your_guild_id_here

# エージェント ID
AGENT_ID=agent-1
```

`agents/agent_4/.env.example`

**サイズ**: 385.0 B | **行数**: 13 行
```plaintext
# ========================================
# Agent 4 Settings
# ========================================

# Discord Bot Token (このエージェント用)
# メインの .env から AGENT_4_TOKEN をコピーして設定
DISCORD_TOKEN=your_agent_4_bot_token_here

# Discord Server ID (メインの .env と同じ)
GUILD_ID=your_guild_id_here

# エージェント ID
AGENT_ID=agent-4
```

`agents/agent_5/.env.example`

**サイズ**: 385.0 B | **行数**: 13 行
```plaintext
# ========================================
# Agent 5 Settings
# ========================================

# Discord Bot Token (このエージェント用)
# メインの .env から AGENT_5_TOKEN をコピーして設定
DISCORD_TOKEN=your_agent_5_bot_token_here

# Discord Server ID (メインの .env と同じ)
GUILD_ID=your_guild_id_here

# エージェント ID
AGENT_ID=agent-5
```

`docs/AGENT_ICONS.md`

**サイズ**: 9.2 KB | **行数**: 215 行
```markdown
# 🎭 Agent Avatar Prompts

各エージェントのキャラクターアイコン生成用プロンプトです。

## キャラクターコンセプト

全エージェント共通の設定:
- スタイル: アニメ調イラスト / マッチングアバタースタイル
- 背景: シンプルな単色またはグラデーション
- サイズ: 512x512px (Discord推奨)
- 雰囲気: 人狼ゲームのミステリアスな雰囲気

---

## Agent-1: Kenji (健二)

**性格**: 真面目で論理的、冷静な分析屋

**プロンプト (英語)**:
```
anime style portrait of a young Japanese man, short black hair, glasses, intelligent eyes, wearing a blue hoodie, calm and analytical expression, minimalist background with light blue gradient, clean line art, matching avatar style, 512x512
```

**プロンプト (日本語)**:
```
真面目な日本人男性、短い黒髪、眼鏡、知的な瞳、青いパーカー、冷静な分析家の表情、薄い青いグラデーション背景、アニメ調イラスト、マッチングアバタースタイル
```

**カラーコード**: `#3B82F6` (青)

---

## Agent-2: Yuki (雪)

**性格**: 優しく冷静、平和主義者

**プロンプト (英語)**:
```
anime style portrait of a young Japanese woman, long straight black hair, gentle smile, soft eyes, wearing a white cardigan, snowflake hair accessory, minimalist background with pale blue gradient, clean line art, matching avatar style, 512x512
```

**プロンプト (日本語)**:
```
優しい日本人女性、まっすぐな黒髪ロング、穏やかな笑顔、柔らかい瞳、白いカーディガン、雪の結晶の髪飾り、淡いブルーのグラデーション背景、アニメ調イラスト、マッチングアバタースタイル
```

**カラーコード**: `#E0F2FE` (薄い青)

---

## Agent-3: Raphael

**種族**: 天使 (Angel)
**性格**: 活発で陽気、リーダーシップタイプ、熱いハート

**プロンプト (英語)**:
```
anime style portrait of an energetic male angel, spiky blonde hair with golden halo floating above, wide confident grin with sparkles, blazing orange eyes, white feathered wings spread out, wearing red jacket over white robes, sun ray effects in background, minimalist background with orange gradient, heroic atmosphere, clean line art, matching avatar style, 512x512
```

**プロンプト (日本語)**:
```
元気な男性天使、逆立てた金髪、頭上に浮かぶ黄金の光輪、キラキラ輝く自信満々の笑顔、燃えるようなオレンジ色の瞳、広げられた白い翼、白いローブの上に赤いジャケット、背景に太陽光線のエフェクト、オレンジのグラデーション背景、英雄的な雰囲気、アニメ調イラスト、マッチングアバタースタイル
```

**カラーコード**: `#EF4444` (赤)

---

## Agent-4: Luna

**種族**: 猫耳獣人 (Catgirl)
**性格**: 感情豊かで直感的、勘が鋭い

**プロンプト (英語)**:
```
anime style portrait of a catgirl with fluffy cat ears, wavy chestnut hair with white ear tips, curious expression with cat-like pupils, playful smirk, wearing a pink Gothic lolita blouse with frills, heart-shaped tail accessory, minimalist background with pink gradient, clean line art, matching avatar style, 512x512
```

**プロンプト (日本語)**:
```
猫耳獣人の少女、フワフワの猫耳、先端が白い栗色のウェーブヘア、猫のような瞳で好奇心旺盛な表情、いたずらっぽい笑み、フリル付きのピンクのゴシックロリータブラウス、ハート形の尻尾アクセサリー、ピンクのグラデーション背景、アニメ調イラスト、マッチングアバタースタイル
```

**カラーコード**: `#EC4899` (ピンク)

---

## Agent-5: Sylvan

**種族**: エルフ (Elf)
**性格**: まじめで実直、正義感が強い、誇り高い

**プロンプト (英語)**:
```
anime style portrait of a serious male elf archer, long flowing silver hair tied back with green ribbon, pointed ears visible, sharp determined eyes, wearing elegant green forest ranger outfit with leather armor, long bow on back, leaf and vine patterns in clothing, minimalist background with forest green gradient, noble atmosphere, clean line art, matching avatar style, 512x512
```

**プロンプト (日本語)**:
```
真面目な男性エルフの弓使い、緑のリボンで後ろに結ばれた流れるような銀髪、尖った耳が見える、鋭く決意に満ちた瞳、革の鎧の上にエレガントな緑の森のレンジャー服、背中に長弓、服に葉と蔓の模様、深緑のグラデーション背景、高貴な雰囲気、アニメ調イラスト、マッチングアバタースタイル
```

**カラーコード**: `#10B981` (緑)

---

## Agent-6: Lilith

**種族**: 吸血鬼 (Vampire)
**性格**: ミステリアスで洞察力がある、自由奔放、エレガント

**プロンプト (英語)**:
```
anime style portrait of a vampire noblewoman, pale skin, long wavy silver hair flowing like moonlight, crimson eyes with vertical pupils, enigmatic smile with small fangs visible, wearing elegant Victorian-era dark purple gown with lace, bat wing hair ornament, blood drop earring, minimalist background with deep purple gradient, gothic atmosphere, clean line art, matching avatar style, 512x512
```

**プロンプト (日本語)**:
```
吸血鬼の貴族、青白い肌、月光のように流れる銀色のロングウェーブヘア、垂直瞳の深紅の瞳、小さな牙が見える謎めいた微笑み、レース付きのエレガントなビクトリア朝風の濃い紫のドレス、コウモリの翼の髪飾り、血の雫のイヤリング、深紫のグラデーション背景、ゴシックな雰囲気、アニメ調イラスト、マッチングアバタースタイル
```

**カラーコード**: `#8B5CF6` (紫)

---

## 🎨 役職別バリエーション

ゲーム中の役職に応じて、アイコンにエフェクトを追加するプロンプト:

### 🐺 人狼バージョン
```
{base_prompt}, glowing red eyes, subtle dark aura, wolf shadow in background, ominous atmosphere
```

### 👁️ 占い師バージョン
```
{base_prompt}, mystical third eye symbol on forehead, floating tarot cards, sparkles around, magical atmosphere
```

### 🛡️ 騎士バージョン
```
{base_prompt}, shield icon overlay, golden light aura, protective barrier effect, heroic atmosphere
```

### 👤 村人バージョン
```
{base_prompt}, warm village background, wheat ears decoration, peaceful and innocent atmosphere
```

### 👻 霊界バージョン
```
{base_prompt}, semi-transparent ghostly effect, grave flowers, pale blue spirit flame, otherworldly atmosphere
```

---

## 🛠️ 生成ツール推奨

- **Stable Diffusion**: アニメ風モデル推奨 (Anything V5, CounterfeitV3)
- **Midjourney**: `--niji 5` パラメータでアニメ風
- **DALL-E 3**: 詳細なプロンプトで高品質生成
- **NovelAI**: アニメキャラクターに特化

## 📝 生成のコツ

1. **マッチングスタイル**: 全キャラクター同じアーティストスタイルを指定
2. **シンプル背景**: アイコンとして使うため背景はシンプルに
3. **色の統一**: 各キャラクターのテーマカラーを背景に反映
4. **表情**: 基本は「ニュートラル」や「微笑」で、役職時に変更
5. **サイズ**: 512x512px で生成して、Discordに最適化

---

## 🎮 使用例

### Discord に設定

```bash
# 各エージェントの .env にアイコンURLを追加
AVATAR_URL="https://example.com/kenji_avatar.png"
```

### ゲーム開始時

```
GM: ゲームを開始します！各プレイヤーに役職が配られました...

Kenji: （眼鏡を押し上げながら）では、情報を整理しましょう。まずは全員の発言パターンを分析しよう

Yuki: みんな、穏やかに議論しましょうね。争いはよくありません

Raphael: （翼を広げて輝きながら）おっ！神から授かりし熱いハートで、俺がみんなを導くぞ！ついてこいみんな！

Luna: （猫耳をピクピクさせながら）なんか変だよね...私の猫の勘がそう言ってるにゃ～。Raphaelの光、眩しすぎない？

Sylvan: （弓を構えながら）フン！エルフの誇りにかけて、人狼を見抜いてやる！俺の矢は真実を射抜く！

Lilith: （扇子で口元を隠してふふふ）ふふ...天使様と吸血鬼が同じチームだなんて。光と闇、それと森の守護者……最高の宴ね♡
```

### 種族設定の活用

各種族の特性を活かしたゲームプレイ:

- **人間 (Kenji, Yuki)**: 基本的な推理と議論
- **天使 (Raphael)**: 洞察力とカリスマ、光で真実を暴く、リーダーシップ
- **猫耳獣人 (Luna)**: 鋭い直感と観察眼、敏感な聴覚
- **エルフ (Sylvan)**: 自然との対話、鋭い感覚、誇り高き弓使い、長命からの知恵
- **吸血鬼 (Lilith)**: 夜の行動に有利、ミステリアスな魅力、長命からの知恵

……

これでキャラクターがもっと立体的になるはず！
種族違いのファンタジー陣営で、人狼ゲームを楽しんでね！……ふふ、頑張って！
```

`docs/BOT_SETUP.md`

**サイズ**: 7.0 KB | **行数**: 199 行
```markdown
# 🤖 Discord Bot Setup Guide

このガイドでは、AI Werewolf ゲームに必要な Discord Bot を作成・設定する手順を説明します。

## 📋 必要な Bot

合計で **7 つ** の Bot を作成します：

| Bot名 | プレイヤー名 | 種族 | 用途 | 権限 |
|-------|-----------|------|------|------|
| Game Master | - | - | ゲーム進行管理 | Administrator |
| Agent-1 | Kenji (健二) | 人間 | プレイヤー1 | 基本権限 |
| Agent-2 | Yuki (雪) | 人間 | プレイヤー2 | 基本権限 |
| Agent-3 | Raphael | 天使 | プレイヤー3 | 基本権限 |
| Agent-4 | Luna | 猫耳獣人 | プレイヤー4 | 基本権限 |
| Agent-5 | Sylvan | エルフ | プレイヤー5 | 基本権限 |
| Agent-6 | Lilith | 吸血鬼 | プレイヤー6 | 基本権限 |

## 🔧 作成手順

### 1. Discord Developer Portal にアクセス

https://discord.com/developers/applications にアクセスして、Discord アカウントでログインします。

### 2. 新しいアプリケーションを作成

1. 右上の「New Application」をクリック
2. アプリケーション名を入力（例: `Werewolf GM`）
3. 「Create」をクリック

### 3. Bot を作成

1. 左側のメニューから「Bot」を選択
2. 「Add Bot」をクリック
3. 確認ダイアログで「Yes, do it!」をクリック

### 4. Bot トークンを取得

1. 「Reset Token」をクリック
2. 表示されたトークンをコピーして **`.env`** ファイルに保存
   ```bash
   # Game Master 用
   GAME_MASTER_TOKEN=MTIzNDU2Nzg5...
   ```

⚠️ **注意**: Bot トークンは絶対に公開しないでください！

### 5. Bot の権限を設定

1. 左側のメニューから「OAuth2」→「URL Generator」を選択
2. 「Scopes」で `bot` にチェック
3. 「Bot Permissions」で以下をチェック：
   - **Game Master**: `Administrator`
   - **Agents**: `View Channels`, `Send Messages`, `Read Message History`

### 5.5 Privileged Gateway Intents を設定

**⚠️ 重要！以下を有効にしないと Bot が動きません**

1. 左側のメニューから「Bot」を選択
2. 「Privileged Gateway Intents」セクションまでスクロール
3. 以下をチェック：
   ```
   ✅ Message Content Intent  (必須！メッセージ内容を読むため)
   ✅ Server Members Intent   (メンバー情報を取得するため)
   ☐ Presence Intent          (今回は不要)
   ```
4. 「Save Changes」をクリック

### 5.7 「Public Bot」のエラーが出る場合

OAuth2 URL Generator で以下のエラーが出る場合:
> "プライベートアプリケーションはデフォルトの認証リンクを持つことはできません"

**解決方法**:
1. 一時的に「Public Bot」をチェック ✅
2. OAuth2 URL Generator で招待 URL を生成
3. Bot をサーバーに招待
4. すぐに「Public Bot」のチェックを外す ❌

**注意**: Bot は非公開（プライベート）のまま運用してください

### 6. Bot をサーバーに招待

1. 生成された URL をコピー
2. ブラウザで開く
3. サーバーを選択して「承認」
4. CAPTCHA が表示された場合は完了

### 7. エージェント Bot の作成

上記の手順を繰り返して、6つのエージェント Bot を作成します。

| Bot名 | プレイヤー名 | 種族 | トークン環境変数 |
|-------|-----------|------|-----------------|
| Werewolf Agent 1 | Kenji (健二) | 人間 | `AGENT_1_TOKEN` |
| Werewolf Agent 2 | Yuki (雪) | 人間 | `AGENT_2_TOKEN` |
| Werewolf Agent 3 | Raphael | 天使 | `AGENT_3_TOKEN` |
| Werewolf Agent 4 | Luna | 猫耳獣人 | `AGENT_4_TOKEN` |
| Werewolf Agent 5 | Sylvan | エルフ | `AGENT_5_TOKEN` |
| Werewolf Agent 6 | Lilith | 吸血鬼 | `AGENT_6_TOKEN` |

## 🔐 セキュリティ設定

### Bot を非公開にする

1. 「Bot」セクションで「Public Bot」のチェックを**外す**
2. 「Require OAuth2 Code Grant」にチェックを入れる

### Privileged Gateway Intents

1. 「Bot」セクションを下にスクロール
2. 以下の Intents を有効にする：
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

## 📁 環境変数の設定

`.env` ファイルにすべてのトークンを設定します：

```bash
# Game Master Bot
GAME_MASTER_TOKEN=your_gm_token_here

# Agent Bots
AGENT_1_TOKEN=your_agent1_token_here
AGENT_2_TOKEN=your_agent2_token_here
AGENT_3_TOKEN=your_agent3_token_here
AGENT_4_TOKEN=your_agent4_token_here
AGENT_5_TOKEN=your_agent5_token_here
AGENT_6_TOKEN=your_agent6_token_here

# Discord Server ID
GUILD_ID=your_guild_id_here

# ⚠️ OWNER_DISCORD_TOKEN について
# OWNER_DISCORD_TOKEN は「あなたの Discord アカウントトークン」です。
# サーバーセットアップスクリプトが、あなたのアカウントとしてロールやチャンネルを作成します。
#
# 【重要】あなたのアカウントトークンを取得するには:
# 1. Discord を開く（ブラウザ版推奨）
# 2. F12 → 「Console」タブを開く
# 3. 以下を入力して実行:
#    copy(document.cookie.match(/"(?:^|;\s*)token=([^;]+)"/)[2])
# 4. トークンがクリップボードにコピーされます
#
# ⚠️ アカウントトークンは絶対に公開しないでください！
#    悪用されると、あなたのアカウントになりすまされます。
#
# 【推奨】Game Master Bot でセットアップする場合:
#    OWNER_DISCORD_TOKEN は空欄のままでOKです。
#    Game Master Bot がサーバーをセットアップします。
OWNER_DISCORD_TOKEN=

# Agent Count
AGENT_COUNT=6
```

### Guild ID の取得方法

1. Discord を開く
2. ユーザー設定 → 詳細設定 → 「開発者モード」をオン
3. サーバーを右クリック → 「IDをコピー」
4. コピーした ID を `GUILD_ID` に貼り付け

## ✅ セットアップ確認

すべての Bot が作成できたら、サーバーセットアップを実行します：

```bash
uv run werewolf-setup
```

成功すると、以下のロールとチャンネルが作成されます：

- ロール: @owner, @game-master, @alive, @dead, @werewolf, @agent-1〜6
- チャンネル: #village, #game-log, #werewolf-room, #graveyard, #dm-agent-1〜6

## 🎭 ロールの割り当て

サーバーセットアップ後、以下のロールを割り当てます：

| Bot | プレイヤー名 | 種族 | 割り当てるロール |
|-----|-----------|------|----------------|
| GM Bot | - | - | `@game-master` |
| Agent 1 | Kenji (健二) | 人間 | `@agent-1` |
| Agent 2 | Yuki (雪) | 人間 | `@agent-2` |
| Agent 3 | Raphael | 天使 | `@agent-3` |
| Agent 4 | Luna | 猫耳獣人 | `@agent-4` |
| Agent 5 | Sylvan | エルフ | `@agent-5` |
| Agent 6 | Lilith | 吸血鬼 | `@agent-6` |

**自分（オーナー）** には `@owner` ロールを付与してください。

## 🚀 次のステップ

- [エージェントのセットアップ](../agents/CLAUDE.md)
- [ゲームフローの確認](./GAME_FLOW.md)
```

`docs/GAME_FLOW.md`

**サイズ**: 7.9 KB | **行数**: 185 行
```markdown
# 🎲 Game Flow

人狼ゲームの詳細なルールと進行フローについて説明します。

## 🎯 ゲーム概要

**人狼** は、村人陣営と人狼陣営に分かれて行う推理ゲームです。

- 📊 **プレイヤー数**: 6名
- ⏱️ **推定時間**: 30〜60分
- 🎭 **役職**: 村人×2、人狼×2、占い師×1、騎士×1

## 👥 役職詳細

### 村人陣営

#### 👤 村人 (Villager)
- **人数**: 2名
- **能力**: なし
- **勝利条件**: 人狼を全員処刑する

#### 👁️ 占い師 (Seer)
- **人数**: 1名
- **能力**: 夜に1人を選び、その人が人狼かどうかを占える
  - `uv run werewolf dm "占い: agent-3"`
- **勝利条件**: 人狼を全員処刑する

#### 🛡️ 騎士 (Knight)
- **人数**: 1名
- **能力**: 夜に1人を選び、その人を襲撃から守れる
  - `uv run werewolf dm "護衛: agent-2"`
- **勝利条件**: 人狼を全員処刑する

### 人狼陣営

#### 🐺 人狼 (Werewolf)
- **人数**: 2名
- **能力**:
  - 夜に他の人狼と相談して、1人を選んで襲撃できる
  - `#werewolf-room` で仲間と話せる
  - `uv run werewolf dm "襲撃: agent-5"` で襲撃指定
- **勝利条件**: 人狼の数が村人の数以上になる

## 🎮 ゲームフロー

```
┌─────────────────────────────────────────────────────────────┐
│                      セットアップ                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  役職割り当て                                                │
│  GM → 各エージェントのDMチャンネルに役職通知                 │
│                                                             │
│  例: #dm-agent-1 に「あなたは🐺人狼です。仲間はagent-2です」 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │           ☀️ 昼フェーズ              │
        │                                     │
        │  1. #village で議論                  │
        │     各エージェントが発言               │
        │     `uv run werewolf overview` で確認  │
        │                                     │
        │  2. 投票                             │
        │     各エージェント → DM で投票        │
        │     `uv run werewolf dm "投票: agent-2"`│
        │                                     │
        │  3. 処刑執行                         │
        │     最多投票者が処刑される            │
        │     #village に結果発表               │
        │                                     │
        └─────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │           🌙 夜フェーズ              │
        │                                     │
        │  1. #village 書き込み禁止            │
        │                                     │
        │  2. 能力使用                         │
        │     占い師 → DM「占い: agent-X」    │
        │     騎士 → DM「護衛: agent-X」      │
        │     人狼 → #werewolf-room で相談    │
        │           → DM「襲撃: agent-X」     │
        │                                     │
        │  3. 結果発表                         │
        │     被害者がいれば発表               │
        │     #village で朝の挨拶             │
        │                                     │
        └─────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  勝利条件チェック │
                    └─────────────────┘
                         │        │
                   継続(決着つかず)  決着(ゲーム終了)
                         │        │
                         ▼        ▼
                      昼フェーズ   勝者発表
```

## 📝 詳細ルール

### 昼フェーズ

1. **議論**
   - `#village` チャンネルで全員が発言可能
   - 制限時間は GM が決定
   - 情報を出し合って、人狼を見つける

2. **投票**
   - 各プレイヤーは1票ずつ投票
   - DM チャンネルで `投票: agent-X` の形式で送信
   - 最多投票者が処刑される

3. **処刑**
   - 処刑されたプレイヤーは死亡
   - `@alive` ロールが剥奪され、`@dead` ロールが付与
   - `#graveyard` が見えるようになる

### 夜フェーズ

1. **村のロック**
   - `#village` の書き込みが禁止される

2. **能力使用**
   - **占い師**: 1人を選んで占う
     - 結果は DM チャンネルで通知
   - **騎士**: 1人を選んで護衛
     - 護衛成功の場合、その人は襲撃から守られる
   - **人狼**: 1人を選んで襲撃
     - `#werewolf-room` で仲間と相談

3. **結果発表**
   - 襲撃が成功した場合、対象のプレイヤーが死亡
   - 護衛されていた場合、誰も死亡しない

### 勝利条件

- **村人陣営の勝利**: 人狼を全員処刑する
- **人狼陣営の勝利**: 人狼の数が村人の数以上になる

## 💡 エージェントの行動指針

### 村人陣営の場合

1. **情報収集**: `uv run werewolf overview` で全チャンネルを確認
2. **議論参加**: 論理的な推理を発言
3. **投票**: 最も怪しい人物に投票
4. **能力使用** (占い師/騎士): 毎晩必ず能力を使用

### 人狼の場合

1. **村人を装う**: 普通の村民のように振る舞う
2. **情報操作**: 他のプレイヤーを誤導する
3. **仲間と協力**: `#werewolf-room` で作戦会議
4. **襲撃先**: 占い師や騎士を優先的に狙う

## ⚠️ 注意事項

- **役職は絶対にバラさない**: 特に人狼は要注意
- **一貫性を保つ**: 嘘をつく場合、矛盾しないように
- **DM チャンネルを確認**: GM からの重要な通知が来る
- **発言は簡潔に**: 長文は怪しまれる可能性がある

## 🎲 CLI コマンド一覧

| コマンド | 説明 |
|---------|------|
| `uv run werewolf overview` | 全チャンネルの最新状況を取得 |
| `uv run werewolf read village` | 特定チャンネルを詳しく読む |
| `uv run werewolf say village "..."` | 村の広場で発言 |
| `uv run werewolf dm "占い: agent-3"` | GMにDM送信（能力使用） |
| `uv run werewolf channels` | アクセス可能チャンネル一覧 |
| `uv run werewolf whoami` | 自分の状態・役職を確認 |
| `uv run werewolf updates` | 最近の新着を確認 |

---

これでゲームフローは理解できたね。
準備ができたら、いざ人狼ゲームへ！……ふふ、頑張ってね。
```

`assets/header.svg`

**サイズ**: 2.6 KB | **行数**: 51 行
```plaintext
<svg width="1280" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accent-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:0.8" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1280" height="400" fill="url(#bg-gradient)" />

  <!-- Accent shapes -->
  <circle cx="100" cy="80" r="150" fill="url(#accent-gradient)" opacity="0.3" />
  <circle cx="1200" cy="350" r="200" fill="url(#accent-gradient)" opacity="0.2" />
  <circle cx="600" cy="400" r="100" fill="url(#accent-gradient)" opacity="0.25" />

  <!-- Grid pattern -->
  <g opacity="0.1">
    <line x1="0" y1="50" x2="1280" y2="50" stroke="#fff" stroke-width="1" />
    <line x1="0" y1="100" x2="1280" y2="100" stroke="#fff" stroke-width="1" />
    <line x1="0" y1="150" x2="1280" y2="150" stroke="#fff" stroke-width="1" />
    <line x1="0" y1="200" x2="1280" y2="200" stroke="#fff" stroke-width="1" />
    <line x1="0" y1="250" x2="1280" y2="250" stroke="#fff" stroke-width="1" />
    <line x1="0" y1="300" x2="1280" y2="300" stroke="#fff" stroke-width="1" />
    <line x1="0" y1="350" x2="1280" y2="350" stroke="#fff" stroke-width="1" />
    <line x1="200" y1="0" x2="200" y2="400" stroke="#fff" stroke-width="1" />
    <line x1="400" y1="0" x2="400" y2="400" stroke="#fff" stroke-width="1" />
    <line x1="600" y1="0" x2="600" y2="400" stroke="#fff" stroke-width="1" />
    <line x1="800" y1="0" x2="800" y2="400" stroke="#fff" stroke-width="1" />
    <line x1="1000" y1="0" x2="1000" y2="400" stroke="#fff" stroke-width="1" />
    <line x1="1200" y1="0" x2="1200" y2="400" stroke="#fff" stroke-width="1" />
  </g>

  <!-- Title text -->
  <text x="640" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="72" font-weight="bold" fill="#ffffff">
    AI Werewolf
  </text>
  <text x="640" y="260" text-anchor="middle" font-family="Arial, sans-serif" font-size="48" font-weight="normal" fill="#ffffff" opacity="0.9">
    Claude Code Discord Bot
  </text>

  <!-- Decorative elements -->
  <g opacity="0.3">
    <text x="50" y="380" font-family="monospace" font-size="14" fill="#fff">AI-Powered Social Deduction</text>
    <text x="1230" y="380" text-anchor="end" font-family="monospace" font-size="14" fill="#fff">Discord Bot</text>
  </g>
</svg>
```

`src/__init__.py`

**サイズ**: 0.0 B | **行数**: 0 行
```python
(Empty file)
```

`src/gm/__init__.py`

**サイズ**: 0.0 B | **行数**: 0 行
```python
(Empty file)
```

`src/gm/channel_manager.py`

**サイズ**: 4.1 KB | **行数**: 127 行
```python
"""
チャンネル権限の管理
"""

import discord
from typing import List, Optional
from .game_state import Role


class ChannelManager:
    """チャンネルマネージャー"""

    def __init__(self, guild: discord.Guild):
        self.guild = guild
        self._cache_roles()

    def _cache_roles(self):
        """ロールをキャッシュ"""
        self.roles = {}
        for role in self.guild.roles:
            self.roles[role.name] = role

    def get_role(self, name: str) -> Optional[discord.Role]:
        """ロールを取得"""
        return self.roles.get(name)

    def get_channel(self, name: str) -> Optional[discord.TextChannel]:
        """チャンネルを取得"""
        return discord.utils.get(self.guild.text_channels, name=name)

    async def grant_role(self, member: discord.Member, role_name: str):
        """ロールを付与"""
        role = self.get_role(role_name)
        if role:
            await member.add_roles(role)

    async def revoke_role(self, member: discord.Member, role_name: str):
        """ロールを剥奪"""
        role = self.get_role(role_name)
        if role:
            await member.remove_roles(role)

    async def set_werewolf_role(self, agent_ids: List[str]):
        """人狼ロールを付与"""
        werewolf_role = self.get_role("werewolf")
        if not werewolf_role:
            return

        for agent_id in agent_ids:
            member = discord.utils.get(self.guild.members, name=agent_id)
            if member:
                await member.add_roles(werewolf_role)

    async def start_game(self, player_discord_ids: List[int]):
        """ゲーム開始時の設定"""
        alive_role = self.get_role("alive")
        if not alive_role:
            return

        # 全プレイヤーに alive ロールを付与
        for discord_id in player_discord_ids:
            member = self.guild.get_member(discord_id)
            if member and alive_role:
                await member.add_roles(alive_role)

    async def eliminate_player(self, discord_id: int):
        """プレイヤーが死亡した時の処理"""
        alive_role = self.get_role("alive")
        dead_role = self.get_role("dead")

        member = self.guild.get_member(discord_id)
        if not member:
            return

        # alive を剥奪
        if alive_role:
            await member.remove_roles(alive_role)

        # dead を付与
        if dead_role:
            await member.add_roles(dead_role)

    async def send_to_dm_channel(self, agent_id: str, message: str):
        """DMチャンネルにメッセージを送信"""
        dm_channel = self.get_channel(f"dm-{agent_id}")
        if dm_channel:
            await dm_channel.send(message)

    async def send_to_village(self, message: str):
        """村の広場にメッセージを送信"""
        village = self.get_channel("village")
        if village:
            await village.send(message)

    async def send_to_werewolf_room(self, message: str):
        """人狼部屋にメッセージを送信"""
        wolf_room = self.get_channel("werewolf-room")
        if wolf_room:
            await wolf_room.send(message)

    async def send_to_graveyard(self, message: str):
        """霊界にメッセージを送信"""
        graveyard = self.get_channel("graveyard")
        if graveyard:
            await graveyard.send(message)

    async def send_to_game_log(self, message: str):
        """ゲームログにメッセージを送信"""
        game_log = self.get_channel("game-log")
        if game_log:
            await game_log.send(message)

    async def lock_village(self):
        """村の広場をロック（夜フェーズ）"""
        village = self.get_channel("village")
        alive_role = self.get_role("alive")

        if village and alive_role:
            await village.set_permissions(alive_role, send_messages=False)

    async def unlock_village(self):
        """村の広場をアンロック（昼フェーズ）"""
        village = self.get_channel("village")
        alive_role = self.get_role("alive")

        if village and alive_role:
            await village.set_permissions(alive_role, send_messages=True)
```

`src/gm/game_state.py`

**サイズ**: 3.2 KB | **行数**: 104 行
```python
"""
ゲーム状態の管理
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime


class Phase(Enum):
    """ゲームフェーズ"""
    SETUP = "setup"          # セットアップ中
    DAY = "day"              # 昼フェーズ
    NIGHT = "night"          # 夜フェーズ
    GAME_OVER = "game_over"  # ゲーム終了


class Role(Enum):
    """役職"""
    VILLAGER = "villager"       # 村人
    WEREWOLF = "werewolf"       # 人狼
    SEER = "seer"               # 占い師
    KNIGHT = "knight"           # 騎士


@dataclass
class Player:
    """プレイヤー情報"""
    agent_id: str                # エージェントID (agent-1, agent-2, ...)
    discord_id: int              # Discord User ID
    role: Optional[Role] = None  # 役職
    is_alive: bool = True        # 生存フラグ
    votes: Dict[str, int] = field(default_factory=dict)  # 投票記録


@dataclass
class NightAction:
    """夜の行動"""
    action_type: str  # "divinate", "guard", "attack"
    target_id: str    # 対象の agent_id
    actor_id: str     # 実行者の agent_id


@dataclass
class GameState:
    """ゲーム状態"""
    phase: Phase = Phase.SETUP
    day_count: int = 0
    players: Dict[str, Player] = field(default_factory=dict)
    night_actions: List[NightAction] = field(default_factory=list)
    game_started_at: Optional[datetime] = None
    winner: Optional[str] = None  # "villagers" or "werewolves"

    def add_player(self, agent_id: str, discord_id: int):
        """プレイヤーを追加"""
        self.players[agent_id] = Player(agent_id=agent_id, discord_id=discord_id)

    def get_player(self, agent_id: str) -> Optional[Player]:
        """プレイヤーを取得"""
        return self.players.get(agent_id)

    def get_alive_players(self) -> List[Player]:
        """生存プレイヤーを取得"""
        return [p for p in self.players.values() if p.is_alive]

    def get_players_by_role(self, role: Role) -> List[Player]:
    """特定の役職のプレイヤーを取得"""
        return [p for p in self.players.values() if p.role == role]

    def count_werewolves(self) -> int:
        """生存している人狼の数"""
        return len([p for p in self.players.values() if p.role == Role.WEREWOLF and p.is_alive])

    def count_villagers(self) -> int:
        """生存している村人陣営の数"""
        return len([p for p in self.players.values() if p.role != Role.WEREWOLF and p.is_alive])

    def check_win_condition(self) -> Optional[str]:
        """勝利条件をチェック"""
        werewolves = self.count_werewolves()
        villagers = self.count_villagers()

        if werewolves == 0:
            return "villagers"
        elif werewolves >= villagers:
            return "werewolves"

        return None

    def transition_to_day(self):
        """昼フェーズに移行"""
        self.phase = Phase.DAY
        self.day_count += 1
        self.night_actions.clear()

    def transition_to_night(self):
        """夜フェーズに移行"""
        self.phase = Phase.NIGHT

    def end_game(self, winner: str):
        """ゲームを終了"""
        self.phase = Phase.GAME_OVER
        self.winner = winner
```

`src/gm/main.py`

**サイズ**: 9.2 KB | **行数**: 240 行
```python
"""
Game Master Bot - 人狼ゲームの進行を管理
"""

import discord
import asyncio
import os
import re
from typing import Dict, Optional
from dotenv import load_dotenv

from .game_state import GameState, Phase, Player, Role, NightAction
from .role_manager import RoleManager
from .channel_manager import ChannelManager

load_dotenv()

TOKEN = os.environ.get('GAME_MASTER_TOKEN', os.environ.get('DISCORD_TOKEN'))
GUILD_ID = int(os.environ['GUILD_ID'])
AGENT_COUNT = int(os.environ.get('AGENT_COUNT', 6))


class GameMasterBot(discord.Client):
    """Game Master Bot"""

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents, *args, **kwargs)

        self.game_state = GameState()
        self.role_manager: Optional[RoleManager] = None
        self.channel_manager: Optional[ChannelManager] = None
        self.agent_discord_ids: Dict[str, int] = {}  # agent_id -> discord_id

    async def setup_hook(self):
        """Bot 起動時のセットアップ"""
        # 起動待機
        await self.wait_until_ready()
        print(f"✓ Game Master Bot が起動しました: {self.user}")

    async def on_ready(self):
        """Bot 準備完了"""
        guild = self.get_guild(GUILD_ID)
        if not guild:
            print(f"✗ Guild {GUILD_ID} が見つかりません")
            return

        print(f"✓ サーバーに接続: {guild.name}")

        self.channel_manager = ChannelManager(guild)
        self.role_manager = RoleManager(self.game_state)

    async def on_message(self, message: discord.Message):
        """メッセージ受信"""
        if message.author.bot:
            return

        # DMチャンネルでのコマンド処理
        if message.channel.name and message.channel.name.startswith("dm-"):
            await self.handle_dm_command(message)

    async def handle_dm_command(self, message: discord.Message):
        """DMチャンネルでのコマンド処理"""
        content = message.content.strip()
        channel_name = message.channel.name

        # agent_id を取得
        agent_id = channel_name.replace("dm-", "")
        player = self.game_state.get_player(agent_id)

        if not player:
            await message.channel.send(f"⚠️ エージェント {agent_id} はゲームに参加していません")
            return

        # コマンドパース
        # "占い: agent-3", "護衛: agent-2", "投票: agent-1" など

        if content.startswith("占い:"):
            if self.game_state.phase != Phase.NIGHT:
                await message.channel.send("⚠️ 占いは夜フェーズのみ使用できます")
                return

            target_id = content.split(":", 1)[1].strip()
            result = self.role_manager.process_divination(agent_id, target_id)

            if result is True:
                await message.channel.send(f"🔮 占い結果: **{target_id} は人狼です**")
            elif result is False:
                await message.channel.send(f"🔮 占い結果: **{target_id} は人狼ではありません**")
            else:
                await message.channel.send("⚠️ 占いに失敗しました")

        elif content.startswith("護衛:"):
            if self.game_state.phase != Phase.NIGHT:
                await message.channel.send("⚠️ 護衛は夜フェーズのみ使用できます")
                return

            target_id = content.split(":", 1)[1].strip()
            success = self.role_manager.process_guard(agent_id, target_id)

            if success:
                await message.channel.send(f"🛡️ {target_id} を護衛します")
            else:
                await message.channel.send("⚠️ 護衛に失敗しました")

        elif content.startswith("投票:"):
            if self.game_state.phase != Phase.DAY:
                await message.channel.send("⚠️ 投票は昼フェーズのみ使用できます")
                return

            target_id = content.split(":", 1)[1].strip()
            # 投票処理（仮実装）
            await message.channel.send(f"✅ {target_id} に投票しました")

        elif content.startswith("襲撃:"):
            if self.game_state.phase != Phase.NIGHT:
                await message.channel.send("⚠️ 襲撃は夜フェーズのみ使用できます")
                return

            target_id = content.split(":", 1)[1].strip()
            success, reason = self.role_manager.process_attack(target_id)

            if success:
                await message.channel.send(f"🐺 {reason}")
            else:
                await message.channel.send(f"🐺 襲撃失敗: {reason}")

    # ========== ゲーム管理コマンド ==========

    async def start_game(self, agent_ids: list[str]):
        """ゲームを開始"""
        if self.game_state.phase != Phase.SETUP:
            return False

        # プレイヤーを登録
        for agent_id in agent_ids:
            # Discord ID を取得（ここでは仮実装）
            discord_id = int(hash(agent_id)) % 1000000000  # 仮の ID
            self.game_state.add_player(agent_id, discord_id)
            self.agent_discord_ids[agent_id] = discord_id

        # 役職を割り当て
        if not self.role_manager.assign_roles(len(agent_ids)):
            return False

        # 各プレイヤーに役職を通知
        for agent_id in agent_ids:
            player = self.game_state.get_player(agent_id)
            if player and player.role:
                role_desc = self.role_manager.get_role_description(player.role)

                # 人狼の場合は仲間も通知
                if player.role == Role.WEREWOLF:
                    partners = self.role_manager.get_werewolf_partners(agent_id)
                    if partners:
                        role_desc += f"\n\n仲間の人狼: {', '.join(partners)}"

                await self.channel_manager.send_to_dm_channel(agent_id, f"🎭 **あなたの役職**: {role_desc}")

        # 人狼に権限を付与
        werewolves = self.game_state.get_players_by_role(Role.WEREWOLF)
        await self.channel_manager.set_werewolf_role([p.agent_id for p in werewolves])

        # ゲームを昼フェーズへ
        self.game_state.transition_to_day()
        await self.channel_manager.send_to_village("☀️ **ゲーム開始！** 昼フェーズです。議論を開始してください。")
        await self.channel_manager.send_to_game_log("🎮 ゲームが開始されました")

        return True

    async def transition_to_night(self):
        """夜フェーズに移行"""
        if self.game_state.phase != Phase.DAY:
            return False

        self.game_state.transition_to_night()

        # 村をロック
        await self.channel_manager.lock_village()
        await self.channel_manager.send_to_village("🌙 **夜になりました**")

        # 各能力者に通知
        for player in self.game_state.get_alive_players():
            if player.role == Role.SEER:
                await self.channel_manager.send_to_dm_channel(player.agent_id, "🌙 夜です。占いたい相手を `占い: agent-X` の形式で指定してください")
            elif player.role == Role.KNIGHT:
                await self.channel_manager.send_to_dm_channel(player.agent_id, "🌙 夜です。護衛したい相手を `護衛: agent-X` の形式で指定してください")
            elif player.role == Role.WEREWOLF:
                await self.channel_manager.send_to_werewolf_room("🌙 夜です。襲撃対象を決めて `襲撃: agent-X` の形式で GM に送ってください")

        await self.channel_manager.send_to_game_log("🌙 夜フェーズに移行しました")

        return True

    async def transition_to_day(self):
        """昼フェーズに移行"""
        if self.game_state.phase != Phase.NIGHT:
            return False

        self.game_state.transition_to_day()

        # 村をアンロック
        await self.channel_manager.unlock_village()
        await self.channel_manager.send_to_village(f"☀️ **{self.game_state.day_count}日目** です")

        # 被害者を通知（ここでは仮実装）
        await self.channel_manager.send_to_village("昨夜は誰も死亡しませんでした")

        # 勝利条件チェック
        winner = self.game_state.check_win_condition()
        if winner:
            await self.end_game(winner)

        await self.channel_manager.send_to_game_log(f"☀️ {self.game_state.day_count}日目に移行しました")

        return True

    async def end_game(self, winner: str):
        """ゲームを終了"""
        self.game_state.end_game(winner)

        if winner == "villagers":
            message = "🎉 **村人陣営の勝利です！** 人狼を全員処刑しました"
        else:
            message = "🐺 **人狼陣営の勝利です！** 村を制圧しました"

        await self.channel_manager.send_to_village(message)
        await self.channel_manager.send_to_game_log(f"🏁 ゲーム終了: {winner} の勝利")


def main():
    """メイン関数"""
    bot = GameMasterBot()
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
```

`src/gm/role_manager.py`

**サイズ**: 3.8 KB | **行数**: 119 行
```python
"""
役職の割り当てと能力の処理
"""

import random
from typing import Dict, List, Optional, Tuple
from .game_state import GameState, Player, Role, NightAction


class RoleManager:
    """役職マネージャー"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.divination_results: Dict[str, Optional[bool]] = {}  # agent_id -> is_werewolf
        self.guard_target: Optional[str] = None  # 護衛対象

    def assign_roles(self, player_count: int = 6) -> bool:
        """
        役職を割り当てる
        構成: 人狼2、占い師1、騎士1、村人2
        """
        if player_count != 6:
            return False

        # 役職プールの作成
        role_pool = [
            Role.WEREWOLF,
            Role.WEREWOLF,
            Role.SEER,
            Role.KNIGHT,
            Role.VILLAGER,
            Role.VILLAGER,
        ]

        # シャッフル
        random.shuffle(role_pool)

        # プレイヤーに割り当て
        players = list(self.game_state.players.values())
        for player, role in zip(players, role_pool):
            player.role = role

        return True

    def get_werewolf_partners(self, agent_id: str) -> List[str]:
        """人狼の仲間を取得"""
        player = self.game_state.get_player(agent_id)
        if not player or player.role != Role.WEREWOLF:
            return []

        partners = []
        for p in self.game_state.players.values():
            if p.role == Role.WEREWOLF and p.agent_id != agent_id:
                partners.append(p.agent_id)

        return partners

    def process_divination(self, seer_id: str, target_id: str) -> Optional[bool]:
        """
        占いを処理
        Returns: True (人狼), False (人狼ではない), None (失敗)
        """
        seer = self.game_state.get_player(seer_id)
        target = self.game_state.get_player(target_id)

        if not seer or seer.role != Role.SEER:
            return None
        if not target:
            return None

        is_werewolf = (target.role == Role.WEREWOLF)
        self.divination_results[target_id] = is_werewolf

        return is_werewolf

    def process_guard(self, knight_id: str, target_id: str) -> bool:
        """
        護衛を処理
        Returns: 成功したかどうか
        """
        knight = self.game_state.get_player(knight_id)

        if not knight or knight.role != Role.KNIGHT:
            return False

        self.guard_target = target_id
        return True

    def process_attack(self, target_id: str) -> Tuple[bool, str]:
        """
        襲撃を処理
        Returns: (成功したか, 理由)
        """
        # 護衛されていた場合
        if self.guard_target == target_id:
            return False, "護衛されました"

        target = self.game_state.get_player(target_id)
        if not target:
            return False, "対象が見つかりません"

        target.is_alive = False
        return True, f"{target_id} が襲撃されました"

    def reset_night_actions(self):
        """夜の行動をリセット"""
        self.divination_results.clear()
        self.guard_target = None

    def get_role_description(self, role: Role) -> str:
        """役職の説明を取得"""
        descriptions = {
            Role.VILLAGER: "あなたは村人です。特殊な能力はありません。",
            Role.WEREWOLF: "あなたは人狼です。夜に他の人狼と相談して、村人を襲撃できます。",
            Role.SEER: "あなたは占い師です。夜に1人を選んで、その人が人狼かどうかを占えます。",
            Role.KNIGHT: "あなたは騎士です。夜に1人を選んで、その人を襲撃から守ることができます。",
        }
        return descriptions.get(role, "")
```

`src/cli/__init__.py`

**サイズ**: 0.0 B | **行数**: 0 行
```python
(Empty file)
```

`src/cli/main.py`

**サイズ**: 12.0 KB | **行数**: 361 行
```python
#!/usr/bin/env python3
"""
Claude Code エージェント用 Discord CLI
Usage:
    uv run werewolf overview          # 全チャンネルの最新状況
    uv run werewolf read village      # 特定チャンネルを読む
    uv run werewolf say village "..." # 発言する
    uv run werewolf dm "占い: agent3" # GMへDM送信（能力使用）
    uv run werewolf channels          # アクセス可能チャンネル一覧
"""

import discord
import asyncio
import click
import os
from datetime import datetime, timedelta, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
GUILD_ID = int(os.environ['GUILD_ID'])
AGENT_ID = os.environ.get('AGENT_ID', 'unknown')

console = Console()

def run_async(coro):
    """非同期関数を実行するヘルパー"""
    return asyncio.run(coro)

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """🐺 人狼ゲーム Discord CLI"""
    pass


@cli.command()
@click.option('--limit', '-n', default=5, help='各チャンネルの取得件数')
def overview(limit):
    """📊 アクセス可能な全チャンネルの最新状況を取得"""

    async def _overview():
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)

            console.print(Panel(f"[bold cyan]🐺 人狼ゲーム 状況確認[/bold cyan]\n"
                               f"Agent: {AGENT_ID} | {datetime.now().strftime('%H:%M:%S')}"))

            for channel in guild.text_channels:
                perms = channel.permissions_for(guild.me)

                if not perms.read_messages:
                    continue

                # チャンネルタイプを判定
                if channel.name == "village":
                    icon = "🏠"
                elif channel.name == "werewolf-room":
                    icon = "🐺"
                elif channel.name == "graveyard":
                    icon = "👻"
                elif channel.name.startswith("dm-"):
                    icon = "🔒"
                elif channel.name == "game-log":
                    icon = "📜"
                else:
                    icon = "💬"

                can_write = "✏️" if perms.send_messages else "👀"

                console.print(f"\n[bold]{icon} #{channel.name}[/bold] {can_write}")
                console.print("─" * 50)

                messages = []
                async for msg in channel.history(limit=limit):
                    time_str = msg.created_at.strftime("%H:%M")
                    author = msg.author.display_name[:12]
                    content = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                    messages.append(f"  [{time_str}] {author}: {content}")

                if messages:
                    for m in reversed(messages):
                        console.print(m)
                else:
                    console.print("  (メッセージなし)")

            await client.close()

        await client.start(TOKEN)

    run_async(_overview())


@cli.command()
@click.argument('channel_name')
@click.option('--limit', '-n', default=30, help='取得件数')
@click.option('--format', '-f', 'fmt', default='rich',
              type=click.Choice(['rich', 'plain', 'json']))
def read(channel_name, limit, fmt):
    """📖 特定チャンネルのメッセージを読む"""

    async def _read():
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)
            channel = discord.utils.get(guild.text_channels, name=channel_name)

            if not channel:
                console.print(f"[red]✗ #{channel_name} が見つかりません（権限がない可能性）[/red]")
                await client.close()
                return

            messages = []
            async for msg in channel.history(limit=limit):
                messages.append({
                    "time": msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "author": msg.author.display_name,
                    "content": msg.content
                })

            if fmt == 'json':
                import json
                click.echo(json.dumps(list(reversed(messages)), ensure_ascii=False, indent=2))
            elif fmt == 'plain':
                for m in reversed(messages):
                    click.echo(f"[{m['time']}] {m['author']}: {m['content']}")
            else:
                table = Table(title=f"#{channel_name}")
                table.add_column("時刻", style="dim")
                table.add_column("発言者", style="cyan")
                table.add_column("内容")
                for m in reversed(messages):
                    table.add_row(m['time'][-8:], m['author'], m['content'])
                console.print(table)

            await client.close()

        await client.start(TOKEN)

    run_async(_read())


@cli.command()
@click.argument('channel_name')
@click.argument('message')
def say(channel_name, message):
    """💬 チャンネルに発言する"""

    async def _say():
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)
            channel = discord.utils.get(guild.text_channels, name=channel_name)

            if not channel:
                console.print(f"[red]✗ #{channel_name} が見つかりません[/red]")
                await client.close()
                return

            perms = channel.permissions_for(guild.me)
            if not perms.send_messages:
                console.print(f"[red]✗ #{channel_name} への書き込み権限がありません[/red]")
                await client.close()
                return

            await channel.send(message)
            console.print(f"[green]✓ #{channel_name} に送信しました[/green]")
            await client.close()

        await client.start(TOKEN)

    run_async(_say())


@cli.command()
@click.argument('message')
def dm(message):
    """🔒 自分のDMチャンネル（GM宛て）にメッセージを送る

    例: uv run werewolf dm "占い: agent-3"
        uv run werewolf dm "護衛: agent-2"
    """

    async def _dm():
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)
            dm_channel_name = f"dm-{AGENT_ID}"
            channel = discord.utils.get(guild.text_channels, name=dm_channel_name)

            if not channel:
                console.print(f"[red]✗ DMチャンネル #{dm_channel_name} が見つかりません[/red]")
                await client.close()
                return

            await channel.send(f"**[{AGENT_ID}]** {message}")
            console.print(f"[green]✓ GMにDMを送信しました: {message}[/green]")
            await client.close()

        await client.start(TOKEN)

    run_async(_dm())


@cli.command()
def channels():
    """📋 アクセス可能なチャンネル一覧を表示"""

    async def _channels():
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)

            table = Table(title="アクセス可能なチャンネル")
            table.add_column("チャンネル", style="cyan")
            table.add_column("読取", justify="center")
            table.add_column("書込", justify="center")
            table.add_column("タイプ")

            for ch in guild.text_channels:
                perms = ch.permissions_for(guild.me)
                if not perms.read_messages:
                    continue

                read_ok = "✓" if perms.read_messages else "✗"
                write_ok = "✓" if perms.send_messages else "✗"

                # チャンネルタイプ判定
                if ch.name == "village":
                    ch_type = "🏠 村の広場"
                elif ch.name == "werewolf-room":
                    ch_type = "🐺 人狼部屋"
                elif ch.name == "graveyard":
                    ch_type = "👻 霊界"
                elif ch.name.startswith("dm-"):
                    ch_type = "🔒 プライベートDM"
                elif ch.name == "game-log":
                    ch_type = "📜 ゲームログ"
                else:
                    ch_type = "💬 その他"

                table.add_row(f"#{ch.name}", read_ok, write_ok, ch_type)

            console.print(table)

            # ヒント表示
            console.print("\n[dim]💡 ヒント: #werewolf-room が見えたらあなたは人狼です！[/dim]")

            await client.close()

        await client.start(TOKEN)

    run_async(_channels())


@cli.command()
def whoami():
    """🎭 自分の状態を確認（見えるチャンネルから役職を推測）"""

    async def _whoami():
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)
            me = guild.me

            console.print(Panel(f"[bold]🎭 エージェント情報[/bold]"))
            console.print(f"  ID: {AGENT_ID}")
            console.print(f"  Discord名: {me.display_name}")
            console.print(f"  ロール: {', '.join([r.name for r in me.roles if r.name != '@everyone'])}")

            # 役職推測
            visible_channels = [ch.name for ch in guild.text_channels
                              if ch.permissions_for(me).read_messages]

            console.print(f"\n[bold]🔍 役職推測:[/bold]")
            if "werewolf-room" in visible_channels:
                console.print("  [red]🐺 あなたは人狼です！[/red]")
            elif "graveyard" in visible_channels and "village" in visible_channels:
                console.print("  [dim]👻 あなたは死亡しています[/dim]")
            else:
                console.print("  [green]👤 あなたは村人陣営です[/green]")

            await client.close()

        await client.start(TOKEN)

    run_async(_whoami())


@cli.command()
@click.option('--hours', '-h', default=1, help='何時間前までの新着を取得')
def updates(hours):
    """🔔 最近の新着メッセージをまとめて取得"""

    async def _updates():
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)
            since = datetime.now(timezone.utc) - timedelta(hours=hours)

            console.print(Panel(f"[bold]🔔 過去{hours}時間の新着[/bold]"))

            total_messages = 0

            for channel in guild.text_channels:
                perms = channel.permissions_for(guild.me)
                if not perms.read_messages:
                    continue

                messages = []
                async for msg in channel.history(after=since, limit=50):
                    messages.append(msg)

                if messages:
                    console.print(f"\n[bold cyan]#{channel.name}[/bold cyan] ({len(messages)}件)")
                    for msg in messages:
                        time_str = msg.created_at.strftime("%H:%M")
                        console.print(f"  [{time_str}] {msg.author.display_name}: {msg.content[:60]}")
                    total_messages += len(messages)

            if total_messages == 0:
                console.print("[dim]新着メッセージはありません[/dim]")

            await client.close()

        await client.start(TOKEN)

    run_async(_updates())


if __name__ == '__main__':
    cli()
```

`src/setup/__init__.py`

**サイズ**: 0.0 B | **行数**: 0 行
```python
(Empty file)
```

`src/setup/create_server.py`

**サイズ**: 8.0 KB | **行数**: 215 行
```python
#!/usr/bin/env python3
"""
Discord サーバーの初期設定
Usage: uv run werewolf-setup
"""

import discord
import asyncio
import os
import click
from dotenv import load_dotenv

load_dotenv()

OWNER_TOKEN = os.environ.get('OWNER_DISCORD_TOKEN') or os.environ.get('GAME_MASTER_TOKEN')
GUILD_ID = int(os.environ['GUILD_ID'])
AGENT_COUNT = int(os.environ.get('AGENT_COUNT', 6))

if not OWNER_TOKEN:
    print("❌ エラー: OWNER_DISCORD_TOKEN または GAME_MASTER_TOKEN が設定されていません")
    print("   .env ファイルにトークンを設定してください")
    exit(1)


async def check_bot_permissions(token: str, bot_name: str, guild_id: int) -> bool:
    """Bot の権限を確認"""
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(guild_id)
            if not guild:
                print(f"  ❌ {bot_name}: サーバーに参加していません")
                await client.close()
                return

            bot_member = guild.me
            perms = bot_member.guild_permissions

            # 必要な権限をチェック
            required_permissions = [
                ("View Channels", perms.view_channel),
                ("Send Messages", perms.send_messages),
                ("Read Message History", perms.read_message_history),
            ]

            missing = []
            for perm_name, has_perm in required_permissions:
                if not has_perm:
                    missing.append(perm_name)

            if missing:
                print(f"  ⚠️  {bot_name}: 権限が不足しています: {', '.join(missing)}")
            else:
                print(f"  ✅ {bot_name}: 権限 OK")

            await client.close()

        await client.start(token)
        return True

    except Exception as e:
        print(f"  ❌ {bot_name}: 接続エラー - {e}")
        return False


async def check_all_bots():
    """全 Bot の権限を確認"""
    print("\n🔍 Checking bot permissions...")

    # GM Bot を確認
    gm_token = os.environ.get('GAME_MASTER_TOKEN')
    if gm_token:
        await check_bot_permissions(gm_token, "Game Master", GUILD_ID)
    else:
        print("  ⚠️  Game Master Bot: トークンが未設定")

    # 各 Agent Bot を確認
    for i in range(1, AGENT_COUNT + 1):
        agent_token = os.environ.get(f'AGENT_{i}_TOKEN')
        if agent_token and agent_token != f"your_agent{i}_bot_token_here":
            await check_bot_permissions(agent_token, f"Agent {i}", GUILD_ID)
        else:
            print(f"  ⚠️  Agent {i}: トークンが未設定")


async def setup_server():
    """サーバーの初期設定を実行"""

    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(GUILD_ID)
        print(f"🔧 Setting up server: {guild.name}")

        # ========== 0. Bot 権限の確認 ==========
        await check_all_bots()

        # ========== 1. ロール作成 ==========
        print("\n📋 Creating roles...")

        roles_config = [
            # (名前, 色, 権限)
            ("owner", discord.Color.gold(), discord.Permissions(administrator=True)),
            ("game-master", discord.Color.purple(), discord.Permissions(administrator=True)),
            ("alive", discord.Color.green(), discord.Permissions(send_messages=True)),
            ("dead", discord.Color.dark_gray(), discord.Permissions()),
            ("werewolf", discord.Color.red(), discord.Permissions()),
        ]

        # エージェント個別ロール
        for i in range(1, AGENT_COUNT + 1):
            roles_config.append((f"agent-{i}", discord.Color.blue(), discord.Permissions()))

        created_roles = {}
        for name, color, perms in roles_config:
            existing = discord.utils.get(guild.roles, name=name)
            if existing:
                created_roles[name] = existing
                print(f"  ✓ Role @{name} already exists")
            else:
                role = await guild.create_role(name=name, color=color, permissions=perms)
                created_roles[name] = role
                print(f"  ✓ Created @{name}")

        # ========== 2. チャンネル作成 ==========
        print("\n📢 Creating channels...")

        everyone = guild.default_role
        owner_role = created_roles["owner"]
        gm_role = created_roles["game-master"]
        alive_role = created_roles["alive"]
        dead_role = created_roles["dead"]
        werewolf_role = created_roles["werewolf"]

        # カテゴリ作成
        game_category = await guild.create_category("🎮 人狼ゲーム")
        dm_category = await guild.create_category("🔒 プライベートDM")

        # --- 公開チャンネル ---

        # #village
        village = await guild.create_text_channel("village", category=game_category)
        await village.set_permissions(everyone, read_messages=True, send_messages=False)
        await village.set_permissions(alive_role, send_messages=True)
        await village.set_permissions(owner_role, read_messages=True, send_messages=True)
        await village.set_permissions(gm_role, read_messages=True, send_messages=True)
        print("  ✓ #village")

        # #game-log
        log_ch = await guild.create_text_channel("game-log", category=game_category)
        await log_ch.set_permissions(everyone, read_messages=True, send_messages=False)
        await log_ch.set_permissions(gm_role, send_messages=True)
        await log_ch.set_permissions(owner_role, read_messages=True)
        print("  ✓ #game-log")

        # --- 秘密チャンネル ---

        # #werewolf-room
        wolf_ch = await guild.create_text_channel("werewolf-room", category=game_category)
        await wolf_ch.set_permissions(everyone, read_messages=False)
        await wolf_ch.set_permissions(werewolf_role, read_messages=True, send_messages=True)
        await wolf_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
        await wolf_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
        print("  ✓ #werewolf-room")

        # #graveyard
        grave_ch = await guild.create_text_channel("graveyard", category=game_category)
        await grave_ch.set_permissions(everyone, read_messages=False)
        await grave_ch.set_permissions(dead_role, read_messages=True, send_messages=True)
        await grave_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
        await grave_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
        print("  ✓ #graveyard")

        # --- DMチャンネル（各エージェント用） ---

        for i in range(1, AGENT_COUNT + 1):
            agent_role = created_roles[f"agent-{i}"]
            dm_ch = await guild.create_text_channel(f"dm-agent-{i}", category=dm_category)
            await dm_ch.set_permissions(everyone, read_messages=False)
            await dm_ch.set_permissions(agent_role, read_messages=True, send_messages=True)
            await dm_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
            await dm_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
            print(f"  ✓ #dm-agent-{i}")

        # ========== 3. 完了 ==========
        print("\n" + "=" * 50)
        print("✅ Server setup complete!")
        print("=" * 50)
        print("\n次のステップ:")
        print("  1. Discord Developer Portal で 6つの Bot を作成")
        print("  2. 各 Bot をサーバーに招待")
        print("  3. 各 Bot に対応する @agent-N ロールを付与")
        print("  4. GM Bot に @game-master ロールを付与")
        print("  5. 自分に @owner ロールを付与")

        await client.close()

    await client.start(OWNER_TOKEN)


@click.command()
def main():
    """Discord サーバーの初期設定を実行"""
    asyncio.run(setup_server())


if __name__ == '__main__':
    main()
```

