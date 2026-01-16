# 🤖 Discord Bot Setup Guide

このガイドでは、AI Werewolf ゲームに必要な Discord Bot を作成・設定する手順を説明します。

## 📋 必要な Bot

合計で **7 つ** の Bot を作成します：

| Bot名 | プレイヤー名 | 種族 | 用途 | 権限 |
|-------|-----------|------|------|------|
| Game Master | - | - | ゲーム進行管理 | Administrator |
| Agent-1 | Kenji (健二) | 人間 | プレイヤー1 | 基本権限 |
| Agent-2 | Yuki (雪) | 人間 | プレイヤー2 | 基本権限 |
| Agent-3 | Raphael | 天使 | プレイヤー3 | 基本権限 |
| Agent-4 | Luna | 猫耳獣人 | プレイヤー4 | 基本権限 |
| Agent-5 | Sylvan | エルフ | プレイヤー5 | 基本権限 |
| Agent-6 | Lilith | 吸血鬼 | プレイヤー6 | 基本権限 |

## 🔧 作成手順

### 1. Discord Developer Portal にアクセス

https://discord.com/developers/applications にアクセスして、Discord アカウントでログインします。

### 2. 新しいアプリケーションを作成

1. 右上の「New Application」をクリック
2. アプリケーション名を入力（例: `Werewolf GM`）
3. 「Create」をクリック

### 3. Bot を作成

1. 左側のメニューから「Bot」を選択
2. 「Add Bot」をクリック
3. 確認ダイアログで「Yes, do it!」をクリック

### 4. Bot トークンを取得

1. 「Reset Token」をクリック
2. 表示されたトークンをコピーして **`.env`** ファイルに保存
   ```bash
   # Game Master 用
   GAME_MASTER_TOKEN=MTIzNDU2Nzg5...
   ```

⚠️ **注意**: Bot トークンは絶対に公開しないでください！

### 5. Bot の権限を設定

1. 左側のメニューから「OAuth2」→「URL Generator」を選択
2. 「Scopes」で `bot` にチェック
3. 「Bot Permissions」で以下をチェック：
   - **Game Master**: `Administrator`
   - **Agents**: `View Channels`, `Send Messages`, `Read Message History`

### 5.5 Privileged Gateway Intents を設定

**⚠️ 重要！以下を有効にしないと Bot が動きません**

1. 左側のメニューから「Bot」を選択
2. 「Privileged Gateway Intents」セクションまでスクロール
3. 以下をチェック：
   ```
   ✅ Message Content Intent  (必須！メッセージ内容を読むため)
   ✅ Server Members Intent   (メンバー情報を取得するため)
   ☐ Presence Intent          (今回は不要)
   ```
4. 「Save Changes」をクリック

### 5.7 「Public Bot」のエラーが出る場合

OAuth2 URL Generator で以下のエラーが出る場合:
> "プライベートアプリケーションはデフォルトの認証リンクを持つことはできません"

**解決方法**:
1. 一時的に「Public Bot」をチェック ✅
2. OAuth2 URL Generator で招待 URL を生成
3. Bot をサーバーに招待
4. すぐに「Public Bot」のチェックを外す ❌

**注意**: Bot は非公開（プライベート）のまま運用してください

### 6. Bot をサーバーに招待

1. 生成された URL をコピー
2. ブラウザで開く
3. サーバーを選択して「承認」
4. CAPTCHA が表示された場合は完了

### 7. エージェント Bot の作成

上記の手順を繰り返して、6つのエージェント Bot を作成します。

| Bot名 | プレイヤー名 | 種族 | トークン環境変数 |
|-------|-----------|------|-----------------|
| Werewolf Agent 1 | Kenji (健二) | 人間 | `AGENT_1_TOKEN` |
| Werewolf Agent 2 | Yuki (雪) | 人間 | `AGENT_2_TOKEN` |
| Werewolf Agent 3 | Raphael | 天使 | `AGENT_3_TOKEN` |
| Werewolf Agent 4 | Luna | 猫耳獣人 | `AGENT_4_TOKEN` |
| Werewolf Agent 5 | Sylvan | エルフ | `AGENT_5_TOKEN` |
| Werewolf Agent 6 | Lilith | 吸血鬼 | `AGENT_6_TOKEN` |

## 🔐 セキュリティ設定

### Bot を非公開にする

1. 「Bot」セクションで「Public Bot」のチェックを**外す**
2. 「Require OAuth2 Code Grant」にチェックを入れる

### Privileged Gateway Intents

1. 「Bot」セクションを下にスクロール
2. 以下の Intents を有効にする：
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

## 📁 環境変数の設定

`.env` ファイルにすべてのトークンを設定します：

```bash
# Game Master Bot
GAME_MASTER_TOKEN=your_gm_token_here

# Agent Bots
AGENT_1_TOKEN=your_agent1_token_here
AGENT_2_TOKEN=your_agent2_token_here
AGENT_3_TOKEN=your_agent3_token_here
AGENT_4_TOKEN=your_agent4_token_here
AGENT_5_TOKEN=your_agent5_token_here
AGENT_6_TOKEN=your_agent6_token_here

# Discord Server ID
GUILD_ID=your_guild_id_here

# ⚠️ OWNER_DISCORD_TOKEN について
# OWNER_DISCORD_TOKEN は「あなたの Discord アカウントトークン」です。
# サーバーセットアップスクリプトが、あなたのアカウントとしてロールやチャンネルを作成します。
#
# 【重要】あなたのアカウントトークンを取得するには:
# 1. Discord を開く（ブラウザ版推奨）
# 2. F12 → 「Console」タブを開く
# 3. 以下を入力して実行:
#    copy(document.cookie.match(/"(?:^|;\s*)token=([^;]+)"/)[2])
# 4. トークンがクリップボードにコピーされます
#
# ⚠️ アカウントトークンは絶対に公開しないでください！
#    悪用されると、あなたのアカウントになりすまされます。
#
# 【推奨】Game Master Bot でセットアップする場合:
#    OWNER_DISCORD_TOKEN は空欄のままでOKです。
#    Game Master Bot がサーバーをセットアップします。
OWNER_DISCORD_TOKEN=

# Agent Count
AGENT_COUNT=6
```

### Guild ID の取得方法

1. Discord を開く
2. ユーザー設定 → 詳細設定 → 「開発者モード」をオン
3. サーバーを右クリック → 「IDをコピー」
4. コピーした ID を `GUILD_ID` に貼り付け

## ✅ セットアップ確認

すべての Bot が作成できたら、サーバーセットアップを実行します：

```bash
uv run werewolf-setup
```

成功すると、以下のロールとチャンネルが作成されます：

- ロール: @owner, @game-master, @alive, @dead, @werewolf, @agent-1〜6
- チャンネル: #village, #game-log, #werewolf-room, #graveyard, #dm-agent-1〜6

## 🎭 ロールの割り当て

サーバーセットアップ後、以下のロールを割り当てます：

| Bot | プレイヤー名 | 種族 | 割り当てるロール |
|-----|-----------|------|----------------|
| GM Bot | - | - | `@game-master` |
| Agent 1 | Kenji (健二) | 人間 | `@agent-1` |
| Agent 2 | Yuki (雪) | 人間 | `@agent-2` |
| Agent 3 | Raphael | 天使 | `@agent-3` |
| Agent 4 | Luna | 猫耳獣人 | `@agent-4` |
| Agent 5 | Sylvan | エルフ | `@agent-5` |
| Agent 6 | Lilith | 吸血鬼 | `@agent-6` |

**自分（オーナー）** には `@owner` ロールを付与してください。

## 🚀 次のステップ

- [エージェントのセットアップ](../agents/CLAUDE.md)
- [ゲームフローの確認](./GAME_FLOW.md)
