#!/usr/bin/env python3
"""
人狼ゲーム用 Stop Hook（シンプル版）

Claudeが止まろうとしたら「チャットを確認して続けろ」と指示する。
"""

import json
import sys
import os

# 標準入力からデータを読む
try:
    input_data = json.load(sys.stdin)
except:
    input_data = {}

# 停止をブロックして、続けるよう指示
output = {
    "decision": "block",
    "reason": f"""ゲームを続けてください。以下の手順で状況を確認し、適切にアクションを行ってください。

## Discord CLI コマンド

```bash
# 全体状況を確認（まずこれを実行！）
uv run werewolf overview

# 自分の状態・役職を確認
uv run werewolf whoami

# アクセス可能なチャンネル一覧
uv run werewolf channels

# 特定チャンネルを詳しく読む
uv run werewolf read village --limit 50
uv run werewolf read werewolf-room --limit 20  # 人狼のみ見える

# 村の広場で発言
uv run werewolf say village "おはようございます"

# GMへプライベートメッセージ（能力使用時）
uv run werewolf dm "占い: agent-3"
uv run werewolf dm "護衛: agent-5"
uv run werewolf dm "投票: agent-2"

# 最近の新着を確認
uv run werewolf updates --hours 1
```

## 役職の確認方法

`uv run werewolf channels` を実行して：

| 見えるチャンネル | あなたの役職 |
|-----------------|-------------|
| #werewolf-room が見える | 🐺 人狼 |
| #werewolf-room が見えない | 👤 村人陣営（村人/占い師/騎士） |
| #graveyard が見える | 👻 死亡済み |

## 行動指針

1. **毎ターン最初に** `uv run werewolf overview` で状況把握
2. DMチャンネルでGMからの指示を確認
3. 論理的に推理して議論に参加
4. **自分の役職は絶対にバラさない**
5. 人狼なら #werewolf-room で仲間と作戦会議
"""
}

print(json.dumps(output, ensure_ascii=False))
