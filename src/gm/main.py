"""
Game Master Bot - 人狼ゲームの進行を管理
"""

import discord
import asyncio
import os
import re
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

from .game_state import GameState, Phase, Player, Role, NightAction
from .role_manager import RoleManager
from .channel_manager import ChannelManager


# ゲーム回数管理用ファイル
GAME_STATE_FILE = Path(__file__).parent.parent.parent / ".game_state.json"


def log_with_timestamp(message: str):
    """タイムスタンプ付きでログを出力"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def load_game_count() -> int:
    """ゲーム回数をファイルから読み込む"""
    if GAME_STATE_FILE.exists():
        try:
            with open(GAME_STATE_FILE, 'r') as f:
                data = json.load(f)
                count = data.get('game_count', 1)
                log_with_timestamp(f"✓ ゲーム回数を読み込みました: {count}")
                return count
        except Exception as e:
            log_with_timestamp(f"⚠️ ゲーム回数の読み込みに失敗: {e}")
    else:
        # ファイルがなければ初期値で作成
        log_with_timestamp("📝 ゲーム回数ファイルを初期化します")
        save_game_count(1)
    return 1


def save_game_count(count: int):
    """ゲーム回数をファイルに保存"""
    try:
        GAME_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(GAME_STATE_FILE, 'w') as f:
            json.dump({'game_count': count}, f, indent=2)
    except Exception as e:
        log_with_timestamp(f"⚠️ ゲーム回数の保存に失敗: {e}")


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

TOKEN = os.environ.get('GAME_MASTER_TOKEN', os.environ.get('DISCORD_TOKEN'))
GUILD_ID = int(os.environ['GUILD_ID'])
AGENT_COUNT = int(os.environ.get('AGENT_COUNT', 6))

# フェーズ時間設定（秒）
DAY_DISCUSSION_TIME = int(os.environ.get('DAY_DISCUSSION_TIME', 60))
DAY_VOTING_TIME = int(os.environ.get('DAY_VOTING_TIME', 30))
NIGHT_TIME = int(os.environ.get('NIGHT_TIME', 30))

# ランダム脱落設定
RANDOM_ELIMINATION_ENABLED = os.environ.get('RANDOM_ELIMINATION_ENABLED', 'false').lower() == 'true'
RANDOM_ELIMINATION_CHANCE = int(os.environ.get('RANDOM_ELIMINATION_CHANCE', 50))

# ゲーム回数は前回の回数を読み込んで+1して今回の回数にする
GAME_COUNT = load_game_count() + 1
# 保存して、次回起動時もこの回数をベースに+1されるようにする
save_game_count(GAME_COUNT)


class GameMasterBot(discord.Client):
    """Game Master Bot"""

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents, *args, **kwargs)

        # 環境変数から時間設定を取得して GameState を初期化
        self.game_state = GameState.with_custom_time_limits(
            day_discussion=DAY_DISCUSSION_TIME,
            day_voting=DAY_VOTING_TIME,
            night=NIGHT_TIME
        )
        self.role_manager: Optional[RoleManager] = None
        self.channel_manager: Optional[ChannelManager] = None
        self.agent_discord_ids: Dict[str, int] = {}  # agent_id -> discord_id
        self.timer_task: Optional[asyncio.Task] = None  # バックグラウンドタイマータスク
        self.timer_stopped = False  # タイマー停止フラグ
        self.last_announced_time: Optional[int] = None  # 最後にアナウンスした残り時間
        self.random_elimination_enabled = RANDOM_ELIMINATION_ENABLED
        self.random_elimination_chance = RANDOM_ELIMINATION_CHANCE

    async def on_ready(self):
        """Bot 準備完了"""
        log_with_timestamp(f"✓ Game Master Bot が起動しました: {self.user}")

        guild = self.get_guild(GUILD_ID)
        if not guild:
            log_with_timestamp(f"✗ Guild {GUILD_ID} が見つかりません")
            return

        log_with_timestamp(f"✓ サーバーに接続: {guild.name}")

        self.channel_manager = ChannelManager(guild)
        self.role_manager = RoleManager(self.game_state)

        # ゲームを自動開始
        agent_ids = [f"agent-{i}" for i in range(1, AGENT_COUNT + 1)]
        log_with_timestamp(f"✓ ゲームを開始します: {', '.join(agent_ids)}")
        success = await self.start_game(agent_ids, guild)

        if success:
            log_with_timestamp("✓ ゲームが正常に開始されました")
        else:
            log_with_timestamp("✗ ゲームの開始に失敗しました")

        # バックグラウンドタイマーを開始
        self.timer_stopped = False
        self.timer_task = self.loop.create_task(self._background_timer())

    async def _background_timer(self):
        """バックグラウンドで動作するタイマータスク"""
        log_with_timestamp("⏱️ タイマーを開始しました")

        # アナウンスする残り時間（秒）
        announcement_times = [60, 30, 15, 10, 5, 3, 2, 1]

        while not self.timer_stopped:
            try:
                # ゲーム中でなければスキップ
                if self.game_state.phase == Phase.SETUP or self.game_state.phase == Phase.GAME_OVER:
                    await asyncio.sleep(1)
                    continue

                # 残り時間を取得
                remaining = self.game_state.get_remaining_seconds()

                # 残り時間アナウンス
                if remaining != self.last_announced_time and remaining in announcement_times:
                    if self.game_state.phase == Phase.DAY:
                        # 昼フェーズ：villageチャンネルに通知（既存機能を維持）
                        phase_name = ""
                        if self.game_state.current_sub_phase == "discussion":
                            phase_name = "議論"
                        elif self.game_state.current_sub_phase == "voting":
                            phase_name = "投票"

                        if phase_name:
                            await self.channel_manager.send_to_village(f"⏰ {phase_name}残り{remaining}秒！")
                            await self.channel_manager.send_to_game_log(f"⏰ {phase_name}残り{remaining}秒をアナウンス")

                    elif self.game_state.phase == Phase.NIGHT:
                        # 夜フェーズ：各能力者に個別DM通知
                        await self._send_timer_notification_to_role_players(
                            Role.SEER, remaining, "🔮", "占い"
                        )
                        await self._send_timer_notification_to_role_players(
                            Role.KNIGHT, remaining, "🛡️", "護衛"
                        )
                        await self._send_timer_notification_to_role_players(
                            Role.WEREWOLF, remaining, "🐺", "襲撃"
                        )
                        await self.channel_manager.send_to_game_log(f"⏰ 夜残り{remaining}秒をアナウンス")

                    self.last_announced_time = remaining

                # 時間切れチェック
                if self.game_state.is_phase_timeout():
                    self.last_announced_time = None  # フェーズ変更時にリセット

                    phase = self.game_state.phase
                    sub_phase = self.game_state.current_sub_phase

                    if phase == Phase.DAY:
                        if sub_phase == "discussion":
                            log_with_timestamp("⏰ 議論時間終了 - 投票フェーズへ移行")
                            await self.start_voting_phase()
                        elif sub_phase == "voting":
                            log_with_timestamp("⏰ 投票時間終了 - 投票結果を集計")
                            await self.process_voting_results()

                            # 投票結果処理後、まだ昼なら夜へ移行
                            if self.game_state.phase == Phase.DAY:
                                log_with_timestamp("🌙 夜フェーズへ移行")
                                await self.transition_to_night()

                    elif phase == Phase.NIGHT:
                        log_with_timestamp("⏰ 夜時間終了 - 昼フェーズへ移行")
                        await self.transition_to_day()

                await asyncio.sleep(1)  # 1秒ごとにチェック

            except asyncio.CancelledError:
                log_with_timestamp("⏱️ タイマーが停止しました")
                break
            except Exception as e:
                log_with_timestamp(f"⚠️ タイマーでエラーが発生: {e}")
                await asyncio.sleep(1)

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

            if self.game_state.current_sub_phase != "voting":
                await message.channel.send("⚠️ 投票フェーズではありません")
                return

            target_id = content.split(":", 1)[1].strip()

            # 投票処理
            if self.game_state.cast_vote(agent_id, target_id):
                await message.channel.send(f"✅ {target_id} に投票しました")

                # 全員投票したかチェック
                alive_count = len(self.game_state.get_alive_players())
                voter_count = self.game_state.count_voters()

                if voter_count >= alive_count:
                    await message.channel.send(f"📊 全員の投票が揃いました（{voter_count}/{alive_count}）")
            else:
                await message.channel.send("⚠️ 投票に失敗しました")

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

    async def _send_timer_notification_to_role_players(
        self,
        role: Role,
        remaining: int,
        icon: str,
        action_name: str
    ):
        """
        特定の役職のプレイヤーにタイマー通知を送信

        Args:
            role: 対象役職（Role.SEER, Role.KNIGHT, Role.WEREWOLF）
            remaining: 残り時間（秒）
            icon: 絵文字（"🔮", "🛡️", "🐺"）
            action_name: アクション名（"占い", "護衛", "襲撃"）
        """
        players = self.game_state.get_players_by_role(role)
        for player in players:
            if player.is_alive:
                await self.channel_manager.send_to_dm_channel(
                    player.agent_id,
                    f"{icon} {action_name}残り{remaining}秒！"
                )

    # ========== ゲーム管理コマンド ==========

    async def start_game(self, agent_ids: list[str], guild: discord.Guild):
        """ゲームを開始"""
        if self.game_state.phase != Phase.SETUP:
            return False

        # プレイヤーを登録（並列で Discord ID を取得）
        tasks = []
        for agent_id in agent_ids:
            # Discord ID を環境変数から取得（なければトークンから取得）
            env_key = f"AGENT_{agent_id.split('-')[1].upper()}_DISCORD_ID"
            discord_id_str = os.environ.get(env_key)

            if discord_id_str:
                discord_id = int(discord_id_str)
                print(f"✓ {agent_id}: Discord ID を環境変数から取得: {discord_id}")
                self.game_state.add_player(agent_id, discord_id)
                self.agent_discord_ids[agent_id] = discord_id
            else:
                # トークンから Bot のユーザー ID を取得
                token_key = f"AGENT_{agent_id.split('-')[1].upper()}_TOKEN"
                token = os.environ.get(token_key)

                if not token:
                    print(f"⚠️ {token_key} が設定されていません")
                    return False

                # 非同期タスクとして実行
                async def get_and_add(agent_id, token):
                    discord_id = await get_bot_user_id(token)
                    if not discord_id:
                        print(f"⚠️ {agent_id} の Discord ID が取得できません")
                        return None, None
                    print(f"✓ {agent_id}: Discord ID をトークンから取得: {discord_id}")
                    self.game_state.add_player(agent_id, discord_id)
                    self.agent_discord_ids[agent_id] = discord_id
                    return agent_id, discord_id

                tasks.append(get_and_add(agent_id, token))

        # 並列実行
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"⚠️ Discord ID 取得中にエラーが発生: {result}")
                    return False
                elif result and result[0] is None:
                    return False

        # 役職を割り当て
        if not self.role_manager.assign_roles(len(agent_ids)):
            return False

        # ゲーム回数プレフィックス
        game_count_prefix = f"【第{GAME_COUNT}回】"

        # 各プレイヤーに役職を通知
        for agent_id in agent_ids:
            player = self.game_state.get_player(agent_id)
            if player and player.role:
                role_desc = self.role_manager.get_role_description(player.role)

                # 人狼の場合は仲間も通知（Discord Mention で表示）
                if player.role == Role.WEREWOLF:
                    partners = self.role_manager.get_werewolf_partners(agent_id)
                    if partners:
                        # Discord Mention に変換
                        partner_mentions = []
                        for partner_id in partners:
                            partner_player = self.game_state.get_player(partner_id)
                            if partner_player:
                                partner_mentions.append(f"<@{partner_player.discord_id}>")
                        role_desc += f"\n\n仲間の人狼: {', '.join(partner_mentions)}"

                # 区切り線付きで送信
                dm_message = f"{game_count_prefix} {'=' * 40}\n🎭 **あなたの役職**: {role_desc}\n{'=' * 40}"
                await self.channel_manager.send_to_dm_channel(agent_id, dm_message)

        # 人狼に権限を付与
        werewolves = self.game_state.get_players_by_role(Role.WEREWOLF)
        await self.channel_manager.set_werewolf_role([p.agent_id for p in werewolves])

        # 占い師に権限を付与
        seers = self.game_state.get_players_by_role(Role.SEER)
        for seer in seers:
            await self.channel_manager.set_seer_role(seer.agent_id)

        # 騎士に権限を付与
        knights = self.game_state.get_players_by_role(Role.KNIGHT)
        for knight in knights:
            await self.channel_manager.set_knight_role(knight.agent_id)

        # 全プレイヤーの dead ロールを剥奪してから alive ロールを付与
        # （前のゲームのロールが残っている場合の対策）
        for discord_id in self.agent_discord_ids.values():
            member = guild.get_member(discord_id)
            if member:
                # dead ロールを剥奪（あれば）
                dead_role = self.channel_manager.get_role("dead")
                if dead_role and dead_role in member.roles:
                    await member.remove_roles(dead_role)
                # alive ロールを付与
                alive_role = self.channel_manager.get_role("alive")
                if alive_role:
                    await member.add_roles(alive_role)

        # ゲーム回数を表示（履歴管理）
        game_count_prefix = f"【第{GAME_COUNT}回】"

        # ゲームを昼フェーズへ
        self.game_state.transition_to_day()

        # 残り時間を計算
        remaining = self.game_state.get_remaining_seconds()
        time_str = f"（残り{remaining}秒）"

        await self.channel_manager.send_to_village(f"{game_count_prefix} ☀️ **ゲーム開始！** 昼フェーズです。議論を開始してください。{time_str}")
        await self.channel_manager.send_to_game_log(f"{game_count_prefix} 🎮 ゲームが開始されました")

        return True

    async def transition_to_night(self):
        """夜フェーズに移行"""
        if self.game_state.phase != Phase.DAY:
            return False

        self.game_state.transition_to_night()

        # 残り時間を計算
        remaining = self.game_state.get_remaining_seconds()
        time_str = f"（残り{remaining}秒）"

        # 村をロック
        await self.channel_manager.lock_village()
        await self.channel_manager.send_to_village(f"🌙 **夜になりました**{time_str}")

        # 各能力者に通知
        for player in self.game_state.get_alive_players():
            if player.role == Role.SEER:
                await self.channel_manager.send_to_dm_channel(player.agent_id, f"🌙 夜です（残り{remaining}秒）。占いたい相手を `占い: agent-X` の形式で指定してください")
            elif player.role == Role.KNIGHT:
                await self.channel_manager.send_to_dm_channel(player.agent_id, f"🌙 夜です（残り{remaining}秒）。護衛したい相手を `護衛: agent-X` の形式で指定してください")
            elif player.role == Role.WEREWOLF:
                await self.channel_manager.send_to_werewolf_room(f"🌙 夜です（残り{remaining}秒）。襲撃対象を決めて `襲撃: agent-X` の形式で GM に送ってください")

        await self.channel_manager.send_to_game_log(f"🌙 夜フェーズに移行しました（残り{remaining}秒）")

        return True

    async def transition_to_day(self):
        """昼フェーズに移行"""
        if self.game_state.phase != Phase.NIGHT:
            return False

        self.game_state.transition_to_day()

        # 夜の結果処理：誰が死んだか確認
        dead_players = [p for p in self.game_state.players.values() if not p.is_alive]

        # 村をアンロック
        await self.channel_manager.unlock_village()

        # 残り時間を計算
        remaining = self.game_state.get_remaining_seconds()
        time_str = f"（残り{remaining}秒）"

        await self.channel_manager.send_to_village(f"☀️ **{self.game_state.day_count}日目** です{time_str}")

        # 被害者を通知
        if dead_players:
            dead_names = [p.agent_id for p in dead_players]
            await self.channel_manager.send_to_village(f"昨夜の被害者: {', '.join(dead_names)}")

            # 死亡したプレイヤーを処理
            for player in dead_players:
                await self.channel_manager.eliminate_player(player.discord_id)
                await self.channel_manager.send_to_graveyard(f"👻 {player.agent_id} が霊界に来ました")
        else:
            await self.channel_manager.send_to_village("昨夜は誰も死亡しませんでした")

        # 夜の行動をリセット
        self.role_manager.reset_night_actions()

        # 勝利条件チェック
        winner = self.game_state.check_win_condition()
        if winner:
            await self.end_game(winner)
            return True

        await self.channel_manager.send_to_game_log(f"☀️ {self.game_state.day_count}日目に移行しました")

        return True

    async def start_voting_phase(self):
        """投票フェーズを開始"""
        if self.game_state.phase != Phase.DAY or self.game_state.current_sub_phase != "discussion":
            return False

        self.game_state.start_voting_phase()

        # 残り時間を計算
        remaining = self.game_state.get_remaining_seconds()

        await self.channel_manager.send_to_village(f"📊 **投票フェーズ開始**（残り{remaining}秒）\nDMで `投票: agent-X` の形式で投票してください")
        await self.channel_manager.send_to_game_log(f"📊 投票フェーズを開始しました（残り{remaining}秒）")

        return True

    async def process_voting_results(self):
        """投票結果を処理して処刑を実行"""
        if self.game_state.current_sub_phase != "voting":
            return False

        results = self.game_state.get_vote_results()
        most_voted = self.game_state.get_most_voted_player()

        if not results:
            # 投票なしの場合、ランダム脱落システムを判定
            import random

            if self.random_elimination_enabled:
                # 生存プレイヤーを取得
                alive_players = self.game_state.get_alive_players()

                if len(alive_players) > 1:
                    # 確率でランダム脱落
                    if random.randint(1, 100) <= self.random_elimination_chance:
                        eliminated_player = random.choice(alive_players)
                        eliminated_id = eliminated_player.agent_id

                        await self.channel_manager.send_to_village(
                            f"📊 投票結果: 誰も投票しませんでした\n"
                            f"🎲 運命の選択... **{eliminated_id}** が randomly 脱落しました！"
                        )

                        # プレイヤーを死亡
                        eliminated_player.is_alive = False
                        await self.channel_manager.eliminate_player(eliminated_player.discord_id)
                        await self.channel_manager.send_to_graveyard(f"👻 {eliminated_id} が運命に選ばれ、霊界に来ました")

                        # 勝利条件チェック
                        winner = self.game_state.check_win_condition()
                        if winner:
                            await self.end_game(winner)
                            return True
                        return True
                    else:
                        await self.channel_manager.send_to_village("📊 投票結果: 誰も投票しませんでした\n🎲 運命の選別... 今回は誰も脱落しませんでした")
                else:
                    await self.channel_manager.send_to_village("📊 投票結果: 誰も投票しませんでした\n（生存プレイヤーが1人以下のため、ランダム脱落はありません）")
            else:
                await self.channel_manager.send_to_village("📊 投票結果: 誰も投票しませんでした")
        elif most_voted is None:
            # 同数の場合
            await self.channel_manager.send_to_village(f"📊 投票結果: 同票で決着がつきませんでした\n{', '.join([f'{k}: {v}票' for k, v in results.items()])}")
        else:
            # 処刑実行
            votes = results[most_voted]
            await self.channel_manager.send_to_village(f"📊 投票結果: **{most_voted}** が処刑されました（{votes}票）")

            # プレイヤーを死亡
            player = self.game_state.get_player(most_voted)
            if player:
                player.is_alive = False
                await self.channel_manager.eliminate_player(player.discord_id)
                await self.channel_manager.send_to_graveyard(f"👻 {most_voted} が処刑され、霊界に来ました")

        # 勝利条件チェック
        winner = self.game_state.check_win_condition()
        if winner:
            await self.end_game(winner)
            return True

        return True

    async def end_game(self, winner: str):
        """ゲームを終了"""
        self.game_state.end_game(winner)

        if winner == "villagers":
            message = "🎉 **村人陣営の勝利です！** 人狼を全員処刑しました"
        else:
            message = "🐺 **人狼陣営の勝利です！** 村を制圧しました"

        await self.channel_manager.send_to_village(message)

        # 全プレイヤーの役職を発表
        role_reveal = "\n\n🎭 **最終結果**:\n"
        for player in self.game_state.players.values():
            status = "生存" if player.is_alive else "死亡"
            role_name = self.role_manager.get_role_name(player.role)
            role_reveal += f"• {player.agent_id}: {role_name}（{status}）\n"
        await self.channel_manager.send_to_village(role_reveal)

        await self.channel_manager.send_to_game_log(f"🏁 ゲーム終了: {winner} の勝利")
        log_with_timestamp(f"✓ 第{GAME_COUNT}回ゲームが終了しました")

    async def close(self):
        """Bot を閉じる時の処理"""
        self.timer_stopped = True
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
            try:
                await self.timer_task
            except asyncio.CancelledError:
                pass
        await super().close()


def main():
    """メイン関数"""
    bot = GameMasterBot()
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
