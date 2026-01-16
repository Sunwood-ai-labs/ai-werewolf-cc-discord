#!/usr/bin/env python3
"""
Discord サーバーの初期設定
Usage: uv run werewolf-setup
"""

import discord
import asyncio
import os
import click
import shutil
from pathlib import Path
from dotenv import load_dotenv


async def get_bot_user_id(token: str):
    """BotトークンからユーザーIDを取得 (HTTP API経由)"""
    import aiohttp
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": f"Bot {token}"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return int(data['id'])
                else:
                    print(f"  ⚠️ Bot ID の取得に失敗: Status {response.status}")
                    return None
    except Exception as e:
        print(f"  ⚠️ Bot ID の取得中にHTTPエラーが発生: {e}")
        return None


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


def setup_agent_configs(skip_missing_claude=True):
    """各エージェントの設定ファイルを作成

    Args:
        skip_missing_claude: .claude ディレクトリがない場合にスキップするか（デフォルト: True）
    """
    print("\n📝 Setting up agent configurations...")

    # プロジェクトルートディレクトリ
    project_root = Path(__file__).parent.parent.parent

    for i in range(1, AGENT_COUNT + 1):
        agent_dir = project_root / f"agents/agent_{i}"
        agent_id = f"agent-{i}"

        # ========== .env ファイルを作成 ==========
        env_file = agent_dir / ".env"

        # メインの .env から値を取得
        guild_id = os.environ.get('GUILD_ID', 'your_guild_id_here')
        agent_token = os.environ.get(f'AGENT_{i}_TOKEN', f'your_agent{i}_bot_token_here')

        env_content = f"""# ========================================
# Agent {i} Settings
# ========================================

# Discord Bot Token (このエージェント用)
DISCORD_TOKEN={agent_token}

# Discord Server ID
GUILD_ID={guild_id}

# エージェント ID
AGENT_ID={agent_id}
"""

        env_file.write_text(env_content)
        print(f"  ✓ Created agents/agent_{i}/.env")

        # ========== CLAUDE.md（ルールブック）を複製 ==========
        source_claude_md = project_root / "agents/CLAUDE.md"
        target_claude_md = agent_dir / "CLAUDE.md"

        if source_claude_md.exists():
            content = source_claude_md.read_text()
            # エージェントIDを置換
            content = content.replace("${AGENT_ID}", agent_id)
            target_claude_md.write_text(content)
            print(f"  ✓ Created agents/agent_{i}/CLAUDE.md")
        else:
            print(f"  ⚠️  CLAUDE.md not found at {source_claude_md}")

        # ========== .claude ディレクトリを複製 ==========
        # 既存のエージェント固有のペルソナ設定を保持するため、
        # 各エージェントの .claude ディレクトリから複製します

        claude_dir = agent_dir / ".claude"
        source_claude_dir = project_root / f"agents/agent_{i}/.claude"

        if claude_dir.exists():
            # 既存の場合はスキップ（各エージェントの固有設定を保持）
            print(f"  ⏭️  Skipping agents/agent_{i}/.claude/ (already exists, preserving persona)")
        elif source_claude_dir.exists():
            # ソースが存在する場合は複製
            shutil.copytree(source_claude_dir, claude_dir)

            # CLAUDE.md の中身をエージェントIDに合わせて更新
            claude_md = claude_dir / "CLAUDE.md"
            if claude_md.exists():
                content = claude_md.read_text()
                # エージェントIDを置換
                content = content.replace("${AGENT_ID}", agent_id)
                claude_md.write_text(content)

            print(f"  ✓ Created agents/agent_{i}/.claude/")
        else:
            if skip_missing_claude:
                print(f"  ⏭️  Skipping .claude directory (not found at {source_claude_dir})")
            else:
                print(f"  ⚠️  Source .claude directory not found at {source_claude_dir}")


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
            ("seer", discord.Color.blue(), discord.Permissions()),
            ("knight", discord.Color.from_rgb(0, 255, 0), discord.Permissions()),  # 緑
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

        # カテゴリ作成（既存チェック）
        game_category = discord.utils.get(guild.categories, name="🎮 人狼ゲーム")
        if game_category:
            print("  ✓ Category 🎮 人狼ゲーム already exists")
        else:
            game_category = await guild.create_category("🎮 人狼ゲーム")
            print("  ✓ Created 🎮 人狼ゲーム")

        dm_category = discord.utils.get(guild.categories, name="🔒 プライベートDM")
        if dm_category:
            print("  ✓ Category 🔒 プライベートDM already exists")
        else:
            dm_category = await guild.create_category("🔒 プライベートDM")
            print("  ✓ Created 🔒 プライベートDM")

        # --- 公開チャンネル ---

        # #village
        village = discord.utils.get(guild.text_channels, name="village")
        if village:
            print("  ✓ #village already exists")
        else:
            village = await guild.create_text_channel("village", category=game_category)
            await village.set_permissions(everyone, read_messages=True, send_messages=False)
            await village.set_permissions(alive_role, send_messages=True)
            await village.set_permissions(owner_role, read_messages=True, send_messages=True)
            await village.set_permissions(gm_role, read_messages=True, send_messages=True)
            print("  ✓ Created #village")

        # #game-log
        log_ch = discord.utils.get(guild.text_channels, name="game-log")
        if log_ch:
            print("  ✓ #game-log already exists")
        else:
            log_ch = await guild.create_text_channel("game-log", category=game_category)
            await log_ch.set_permissions(everyone, read_messages=True, send_messages=False)
            await log_ch.set_permissions(gm_role, send_messages=True)
            await log_ch.set_permissions(owner_role, read_messages=True)
            print("  ✓ Created #game-log")

        # #system-log
        system_log_ch = discord.utils.get(guild.text_channels, name="system-log")
        if system_log_ch:
            print("  ✓ #system-log already exists")
        else:
            system_log_ch = await guild.create_text_channel("system-log", category=game_category)
            await system_log_ch.set_permissions(everyone, read_messages=False)
            await system_log_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
            await system_log_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
            print("  ✓ Created #system-log")

        # --- 秘密チャンネル ---

        # #werewolf-room
        wolf_ch = discord.utils.get(guild.text_channels, name="werewolf-room")
        if wolf_ch:
            print("  ✓ #werewolf-room already exists")
        else:
            wolf_ch = await guild.create_text_channel("werewolf-room", category=game_category)
            await wolf_ch.set_permissions(everyone, read_messages=False)
            await wolf_ch.set_permissions(werewolf_role, read_messages=True, send_messages=True)
            await wolf_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
            await wolf_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
            print("  ✓ Created #werewolf-room")

        # #seer-room (占い師専用)
        seer_ch = discord.utils.get(guild.text_channels, name="seer-room")
        if seer_ch:
            print("  ✓ #seer-room already exists")
        else:
            seer_ch = await guild.create_text_channel("seer-room", category=game_category)
            await seer_ch.set_permissions(everyone, read_messages=False)
            await seer_ch.set_permissions(created_roles["seer"], read_messages=True, send_messages=True)
            await seer_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
            await seer_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
            print("  ✓ Created #seer-room")

        # #knight-room (騎士専用)
        knight_ch = discord.utils.get(guild.text_channels, name="knight-room")
        if knight_ch:
            print("  ✓ #knight-room already exists")
        else:
            knight_ch = await guild.create_text_channel("knight-room", category=game_category)
            await knight_ch.set_permissions(everyone, read_messages=False)
            await knight_ch.set_permissions(created_roles["knight"], read_messages=True, send_messages=True)
            await knight_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
            await knight_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
            print("  ✓ Created #knight-room")

        # #graveyard
        grave_ch = discord.utils.get(guild.text_channels, name="graveyard")
        if grave_ch:
            print("  ✓ #graveyard already exists")
        else:
            grave_ch = await guild.create_text_channel("graveyard", category=game_category)
            await grave_ch.set_permissions(everyone, read_messages=False)
            await grave_ch.set_permissions(dead_role, read_messages=True, send_messages=True)
            await grave_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
            await grave_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
            print("  ✓ Created #graveyard")

        # --- DMチャンネル（各エージェント用） ---

        for i in range(1, AGENT_COUNT + 1):
            agent_role = created_roles[f"agent-{i}"]
            dm_ch_name = f"dm-agent-{i}"
            dm_ch = discord.utils.get(guild.text_channels, name=dm_ch_name)
            if dm_ch:
                print(f"  ✓ #{dm_ch_name} already exists")
            else:
                dm_ch = await guild.create_text_channel(dm_ch_name, category=dm_category)
                await dm_ch.set_permissions(everyone, read_messages=False)
                await dm_ch.set_permissions(agent_role, read_messages=True, send_messages=True)
                await dm_ch.set_permissions(owner_role, read_messages=True, send_messages=True)
                await dm_ch.set_permissions(gm_role, read_messages=True, send_messages=True)
                print(f"  ✓ Created #{dm_ch_name}")

        # ========== 3. Bot にロールを付与 ==========
        print("\n🔐 Assigning roles to bots...")

        # 各 Bot のユーザー ID を取得（HTTP API経由で安全に取得）
        bot_ids = {}

        # GM Bot
        gm_token = os.environ.get('GAME_MASTER_TOKEN')
        if gm_token and gm_token != "your_gm_bot_token_here":
            gm_id = await get_bot_user_id(gm_token)
            if gm_id:
                bot_ids['gm'] = gm_id

        # Agent Bots
        for i in range(1, AGENT_COUNT + 1):
            agent_token = os.environ.get(f'AGENT_{i}_TOKEN')
            if agent_token and agent_token != f"your_agent{i}_bot_token_here":
                agent_id = await get_bot_user_id(agent_token)
                if agent_id:
                    bot_ids[f'agent-{i}'] = agent_id

        # ロールを付与
        # GM Bot
        if 'gm' in bot_ids:
            gm_member = guild.get_member(bot_ids['gm'])
            if gm_member:
                if gm_role in gm_member.roles:
                    print(f"  ✓ GM Bot already has @game-master")
                else:
                    await gm_member.add_roles(gm_role)
                    print(f"  ✓ Assigned @game-master to GM Bot")
            else:
                print(f"  ⚠️  GM Bot がサーバーに見つかりません")
        else:
            print(f"  ⚠️  GM Bot のトークンが未設定か無効です")

        # Agent Bots
        for i in range(1, AGENT_COUNT + 1):
            agent_key = f'agent-{i}'
            if agent_key in bot_ids:
                agent_member = guild.get_member(bot_ids[agent_key])
                agent_role = created_roles[agent_key]
                if agent_member:
                    if agent_role in agent_member.roles:
                        print(f"  ✓ Agent {i} already has @agent-{i}")
                    else:
                        await agent_member.add_roles(agent_role)
                        print(f"  ✓ Assigned @agent-{i} to Agent {i}")
                else:
                    print(f"  ⚠️  Agent {i} がサーバーに見つかりません")
            else:
                print(f"  ⚠️  Agent {i} のトークンが未設定か無効です")

        # オーナー（実行者本人）に @owner を付与
        owner_member = guild.me
        if owner_member:
            if owner_role in owner_member.roles:
                print(f"  ✓ You already have @owner")
            else:
                await owner_member.add_roles(owner_role)
                print(f"  ✓ Assigned @owner to you")

        # ========== 4. .env に Discord ID を保存 ==========
        print("\n💾 Saving Discord IDs to .env...")

        project_root = Path(__file__).parent.parent.parent
        env_file = project_root / ".env"

        if env_file.exists():
            # .env ファイルを読み込んで更新
            env_content = env_file.read_text()
            lines = env_content.split('\n')

            # 更新する行を探す
            updated_lines = []
            updated_keys = set()

            for line in lines:
                if '=' in line:
                    key = line.split('=')[0]
                    # AGENT_N_DISCORD_ID ならスキップ（後で追加する）
                    if key.endswith('_DISCORD_ID'):
                        updated_keys.add(key)
                        continue
                updated_lines.append(line)

            # Discord ID を追加
            for i in range(1, AGENT_COUNT + 1):
                key = f'AGENT_{i}_DISCORD_ID'
                if f'agent-{i}' in bot_ids:
                    discord_id = bot_ids[f'agent-{i}']
                    updated_lines.append(f'{key}={discord_id}')
                    print(f"  ✓ {key}={discord_id}")

            env_file.write_text('\n'.join(updated_lines))
            print(f"  ✓ Saved {len([k for k in bot_ids.keys() if k.startswith('agent-')])} Discord IDs to .env")

        # ========== 5. システムログに記録 ==========
        if system_log_ch:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_embed = discord.Embed(
                title="🔧 サーバーセットアップ完了",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            log_embed.add_field(name="実行時刻", value=timestamp, inline=False)
            log_embed.add_field(name="GM Bot", value="✅ ロール付与済み" if 'gm' in bot_ids else "⚠️ 未設定", inline=True)
            log_embed.add_field(name="Agent Bots", value=f"✅ {len([k for k in bot_ids.keys() if k.startswith('agent-')])}/{AGENT_COUNT} 準備完了", inline=True)
            log_embed.add_field(name="Owner", value="✅ ロール付与済み", inline=True)

            await system_log_ch.send(embed=log_embed)
            print(f"\n  📝 システムログを #system-log に送信しました")

        # ========== 6. 完了 ==========
        print("\n" + "=" * 50)
        print("✅ Server setup complete!")
        print("=" * 50)
        print("\n🎮 準備完了！これでゲームを開始できます")

        await client.close()

    await client.start(OWNER_TOKEN)


@click.command()
@click.option('--agent-configs/--no-agent-configs', default=True, help='エージェント設定ファイルのセットアップを実行するか（デフォルト: 実行）')
@click.option('--server/--no-server', default=True, help='Discord サーバーのセットアップを実行するか（デフォルト: 実行）')
@click.option('--skip-missing-claude/--fail-missing-claude', default=True, help='.claude ディレクトリがない場合にスキップするか（デフォルト: スキップ）')
def main(agent_configs, server, skip_missing_claude):
    """Discord サーバーの初期設定を実行

    \b
    例:
        uv run werewolf-setup              # すべて実行
        uv run werewolf-setup --no-server  # エージェント設定のみ
        uv run werewolf-setup --no-agent-configs  # サーバーセットアップのみ
    """
    # エージェント設定ファイルを作成
    if agent_configs:
        setup_agent_configs(skip_missing_claude=skip_missing_claude)
    else:
        print("⏭️  Skipping agent configurations")

    # サーバーセットアップ
    if server:
        asyncio.run(setup_server())
    else:
        print("⏭️  Skipping server setup")


if __name__ == '__main__':
    main()
