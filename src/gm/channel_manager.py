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

    async def set_seer_role(self, agent_id: str):
        """占い師ロールを付与"""
        seer_role = self.get_role("seer")
        if not seer_role:
            return

        member = discord.utils.get(self.guild.members, name=agent_id)
        if member:
            await member.add_roles(seer_role)

    async def set_knight_role(self, agent_id: str):
        """騎士ロールを付与"""
        knight_role = self.get_role("knight")
        if not knight_role:
            return

        member = discord.utils.get(self.guild.members, name=agent_id)
        if member:
            await member.add_roles(knight_role)

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
