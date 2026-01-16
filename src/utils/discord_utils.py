"""Discord utility functions."""

from typing import Optional
import aiohttp


async def get_bot_user_id(token: str) -> Optional[int]:
    """
    Bot トークンからユーザー ID を取得 (HTTP API経由)

    Args:
        token: Discord Bot Token

    Returns:
        Bot User ID (取得失敗時は None)
    """
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
