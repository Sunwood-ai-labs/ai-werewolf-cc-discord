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

# カレントディレクトリの .env を確実に読み込む
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

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
    """🎭 自分の状態を確認（実際の役職をDMから取得）"""

    async def _whoami():
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = client.get_guild(GUILD_ID)
            me = guild.me

            console.print(Panel(f"[bold]🎭 エージェント情報[/bold]"))
            console.print(f"  ID: {AGENT_ID}")
            console.print(f"  Discord名: {me.display_name}")
            console.print(f"  ロール: {', '.join([r.name for r in me.roles if r.name != '@everyone'])}")

            # DMチャンネルから役職情報を取得
            dm_channel = discord.utils.get(guild.text_channels, name=f"dm-{AGENT_ID}")

            if dm_channel:
                # 最新のメッセージを取得して役職を特定
                messages = []
                async for msg in dm_channel.history(limit=50):
                    messages.append(msg)

                # 役職を特定
                role_found = False
                for msg in reversed(messages):
                    content = msg.content

                    # GMからの役職通知を検出
                    if "あなたは" in content and "です" in content:
                        # 役職が見つかった
                        if "占い師" in content:
                            console.print(f"\n[bold]🎭 あなたの役職:[/bold]")
                            console.print("  [blue]👁️ 占い師[/blue]")
                            role_found = True
                            break
                        elif "人狼" in content:
                            console.print(f"\n[bold]🎭 あなたの役職:[/bold]")
                            console.print("  [red]🐺 人狼[/red]")
                            role_found = True
                            break
                        elif "騎士" in content:
                            console.print(f"\n[bold]🎭 あなたの役職:[/bold]")
                            console.print("  [green]🛡️ 騎士[/green]")
                            role_found = True
                            break
                        elif "村人" in content:
                            console.print(f"\n[bold]🎭 あなたの役職:[/bold]")
                            console.print("  [green]👤 村人[/green]")
                            role_found = True
                            break

                if role_found:
                    # 生存状態を確認
                    visible_channels = [ch.name for ch in guild.text_channels
                                      if ch.permissions_for(me).read_messages]

                    if "graveyard" in visible_channels:
                        console.print(f"\n[bold]📊 状態:[/bold]")
                        console.print("  [dim]👻 死亡中[/dim]")
                    else:
                        console.print(f"\n[bold]📊 状態:[/bold]")
                        console.print("  [green]✓ 生存中[/green]")
                else:
                    # 役職が見つからない場合は推測モード
                    visible_channels = [ch.name for ch in guild.text_channels
                                      if ch.permissions_for(me).read_messages]

                    console.print(f"\n[bold]🔍 役職推測（DMから取得できませんでした）:[/bold]")
                    if "werewolf-room" in visible_channels:
                        console.print("  [red]🐺 あなたは人狼です！[/red]")
                    elif "graveyard" in visible_channels and "village" in visible_channels:
                        console.print("  [dim]👻 あなたは死亡しています[/dim]")
                    else:
                        console.print("  [green]👤 あなたは村人陣営です[/green]")
            else:
                console.print(f"\n[yellow]⚠️ DMチャンネルが見つかりません[/yellow]")

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
