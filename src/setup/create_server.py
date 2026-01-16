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
