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
