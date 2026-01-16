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

    def get_role_name(self, role: Role) -> str:
        """役職名を取得"""
        names = {
            Role.VILLAGER: "村人",
            Role.WEREWOLF: "人狼",
            Role.SEER: "占い師",
            Role.KNIGHT: "騎士",
        }
        return names.get(role, "")
