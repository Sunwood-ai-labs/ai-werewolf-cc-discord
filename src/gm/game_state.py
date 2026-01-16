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
