"""
ゲーム状態の管理
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta


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
class PhaseTimeLimit:
    """フェーズの時間制限"""
    day_discussion: int = 60     # 昼の議論時間（秒）
    day_voting: int = 30         # 投票時間（秒）
    night: int = 30              # 夜の時間（秒）


@dataclass
class Player:
    """プレイヤー情報"""
    agent_id: str                # エージェントID (agent-1, agent-2, ...)
    discord_id: int              # Discord User ID
    role: Optional[Role] = None  # 役職
    is_alive: bool = True        # 生存フラグ
    has_voted: bool = False      # 投票済みフラグ
    vote_target: Optional[str] = None  # 投票先


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

    # 時間管理
    phase_started_at: Optional[datetime] = None  # 現在のフェーズ開始時刻
    phase_time_limit: PhaseTimeLimit = field(default_factory=PhaseTimeLimit)
    current_sub_phase: str = "discussion"  # "discussion" or "voting" for day phase

    @classmethod
    def with_custom_time_limits(cls, day_discussion: int = 60, day_voting: int = 30, night: int = 30):
        """カスタム時間制限で GameState を作成"""
        return cls(
            phase_time_limit=PhaseTimeLimit(
                day_discussion=day_discussion,
                day_voting=day_voting,
                night=night
            )
        )

    def get_phase_time_limit_seconds(self) -> int:
        """現在のフェーズの時間制限（秒）を取得"""
        if self.phase == Phase.DAY:
            if self.current_sub_phase == "discussion":
                return self.phase_time_limit.day_discussion
            elif self.current_sub_phase == "voting":
                return self.phase_time_limit.day_voting
        elif self.phase == Phase.NIGHT:
            return self.phase_time_limit.night
        return 0

    def get_remaining_seconds(self) -> int:
        """残り時間（秒）を取得"""
        if not self.phase_started_at:
            return 0

        limit = self.get_phase_time_limit_seconds()
        if limit == 0:
            return 0

        elapsed = (datetime.now() - self.phase_started_at).total_seconds()
        remaining = max(0, limit - elapsed)
        return int(remaining)

    def is_phase_timeout(self) -> bool:
        """フェーズが時間切れかどうか"""
        return self.get_remaining_seconds() <= 0

    def get_phase_end_time(self) -> Optional[datetime]:
        """フェーズ終了時刻を取得"""
        if not self.phase_started_at:
            return None
        limit = self.get_phase_time_limit_seconds()
        if limit == 0:
            return None
        return self.phase_started_at + timedelta(seconds=limit)

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
        self.current_sub_phase = "discussion"  # 議論フェーズから開始
        self.phase_started_at = datetime.now()  # フェーズ開始時刻を記録

    def transition_to_night(self):
        """夜フェーズに移行"""
        self.phase = Phase.NIGHT
        self.phase_started_at = datetime.now()  # フェーズ開始時刻を記録

    def start_voting_phase(self):
        """投票フェーズを開始"""
        self.current_sub_phase = "voting"
        self.phase_started_at = datetime.now()  # 投票開始時刻を記録
        # 全プレイヤーの投票をリセット
        for player in self.players.values():
            player.has_voted = False
            player.vote_target = None

    def end_game(self, winner: str):
        """ゲームを終了"""
        self.phase = Phase.GAME_OVER
        self.winner = winner
        self.phase_started_at = None

    def cast_vote(self, voter_id: str, target_id: str) -> bool:
        """投票を処理"""
        voter = self.get_player(voter_id)
        target = self.get_player(target_id)

        if not voter or not target:
            return False
        if not voter.is_alive or not target.is_alive:
            return False

        voter.has_voted = True
        voter.vote_target = target_id
        return True

    def get_vote_results(self) -> Dict[str, int]:
        """投票結果を集計（対象 -> 票数）"""
        results: Dict[str, int] = {}
        for player in self.players.values():
            if player.is_alive and player.vote_target:
                results[player.vote_target] = results.get(player.vote_target, 0) + 1
        return results

    def get_most_voted_player(self) -> Optional[str]:
        """最多投票者を取得（同数の場合は None）"""
        results = self.get_vote_results()
        if not results:
            return None

        max_votes = max(results.values())
        most_voted = [pid for pid, count in results.items() if count == max_votes]

        # 同数の場合は None
        if len(most_voted) > 1:
            return None
        return most_voted[0]

    def count_voters(self) -> int:
        """投票した生存プレイヤー数を取得"""
        return len([p for p in self.players.values() if p.is_alive and p.has_voted])
