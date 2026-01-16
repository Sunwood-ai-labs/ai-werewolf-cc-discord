# テストスクリプト使い方

人狼ゲームの各機能をテストするためのスクリプトと手順です。

## 📋 概要

以下のテストスクリプトが用意されています：

| スクリプト | 説明 |
|----------|------|
| `interactive.sh` | 各エージェントになりかわって操作できる**インタラクティブスクリプト** |
| `test_role_assignment.sh` | 役職配布テスト |
| `test_seer.sh` | 占い師の占いテスト |
| `test_knight.sh` | 騎士の護衛テスト |
| `test_werewolf.sh` | 人狼の襲撃テスト |
| `test_voting.sh` | 投票テスト |
| `test_random_elimination.sh` | ランダム脱落テスト |
| `run_all_tests.sh` | 全テストを一括実行 |

## 🚀 セットアップ

### 1. テスト用の `.env` を使用

```bash
# テスト用設定をコピー
cp .env.test .env

# .env を編集してトークン等を設定
vim .env
```

### 2. テスト用設定内容

`.env.test` には以下の設定が含まれています：

```bash
# テスト用に短時間設定
DAY_DISCUSSION_TIME=30    # 昼の議論時間（30秒）
DAY_VOTING_TIME=20        # 投票時間（20秒）
NIGHT_TIME=15             # 夜の時間（15秒）

# ランダム脱落を有効化（100%で発生）
RANDOM_ELIMINATION_ENABLED=true
RANDOM_ELIMINATION_CHANCE=100
```

## 🎮 テスト手順

### 🌟 方法1: インタラクティブに操作（おすすめ）

**前提**: GM Bot が既に起動していること

```bash
# インタラクティブスクリプトを起動
./tests/interactive.sh
```

インタラクティブモードでの操作例：

```bash
# エージェントを切り替え
[agent_1]> agent 2
[✓] agent_2 に切り替えました

# 全体状況を確認
[agent_2]> overview

# 村の広場で発言
[agent_2]> say みんな、おはよう！

# 投票する
[agent_2]> dm 投票: agent-1

# 投票なしテスト：投票フェーズで待機
[agent_1]> wait 35

# 終了
[agent_1]> exit
```

**コマンド一覧**:
- `agent [1-6]` - エージェントを切り替え
- `overview` - 全体状況を確認
- `whoami` - 自分の状態を確認
- `channels` - アクセス可能チャンネル一覧
- `read [channel]` - チャンネルを読む (village, werewolf-room, graveyard)
- `say [message]` - 村の広場で発言
- `dm [message]` - GMにDM送信
- `wait [seconds]` - 指定秒数待機（投票時間切れ待ち用）
- `help` - ヘルプを表示
- `exit` - 終了

### 方法2: 全テスト一括実行

**前提**: GM Bot が既に起動していること

```bash
# 全テストを一括実行
./tests/run_all_tests.sh
```

### 方法3: 個別テスト実行

#### 役職配布テスト

```bash
./tests/test_role_assignment.sh
```

**確認内容**:
- 各エージェントの役職を確認
- 人狼が2名であること
- 占い師が1名であること
- 騎士が1名であること
- 村人が2名であること

#### 占い師テスト

```bash
./tests/test_seer.sh
```

**確認内容**:
- 占い師エージェントを特定
- 夜フェーズになるまで待機
- 占いを実行
- 占い結果が正しく返ってくること

#### 騎士の護衛テスト

```bash
./tests/test_knight.sh
```

**確認内容**:
- 騎士エージェントを特定
- 夜フェーズになるまで待機
- 護衛を実行
- 護衛結果が正しく返ってくること

#### 人狼の襲撃テスト

```bash
./tests/test_werewolf.sh
```

**確認内容**:
- 人狼エージェントを特定
- 夜フェーズになるまで待機
- 襲撃を実行
- 襲撃結果が正しく返ってくること

#### 投票テスト

```bash
./tests/test_voting.sh
```

**確認内容**:
- 投票フェーズになるまで待機
- 全エージェントが投票を実行
- 投票結果が正しく集計されること

#### ランダム脱落テスト

```bash
./tests/test_random_elimination.sh
```

**確認内容**:
- 投票フェーズになるまで待機
- 誰も投票せずに時間切れまで待機
- ランダム脱落が発生すること

## ✅ 確認事項

### 役職配布テスト

- [ ] 人狼が2名配布された
- [ ] 占い師が1名配布された
- [ ] 騎士が1名配布された
- [ ] 村人が2名配布された

### 占い師テスト

- [ ] 占い師エージェントを特定できた
- [ ] 夜フェーズを検出できた
- [ ] 占い結果がDMで返ってきた
- [ ] 結果が正しい（人狼かどうか）

### 騎士の護衛テスト

- [ ] 騎士エージェントを特定できた
- [ ] 夜フェーズを検出できた
- [ ] 護衛結果がDMで返ってきた
- [ ] 対象が保護された

### 人狼の襲撃テスト

- [ ] 人狼エージェントを特定できた
- [ ] 夜フェーズを検出できた
- [ ] 襲撃結果がDMで返ってきた
- [ ] 対象が襲撃された

### 投票テスト

- [ ] 投票フェーズを検出できた
- [ ] 全員が投票できた
- [ ] 投票結果が正しく集計された
- [ ] 最多投票者が処刑された

### ランダム脱落テスト

- [ ] 投票フェーズを検出できた
- [ ] 誰も投票しなかった
- [ ] ランダム脱落が発生した
- [ ] 脱落したプレイヤーが `#graveyard` に追加された

## 🔧 トラブルシューティング

### 投票フェーズが始まらない

- GM Bot が起動しているか確認
- `.env` の設定が正しいか確認

### ランダム脱落が発生しない

```bash
# .env の設定を確認
cat .env | grep RANDOM_ELIMINATION
```

期待される出力：
```
RANDOM_ELIMINATION_ENABLED=true
RANDOM_ELIMINATION_CHANCE=100
```

### エージェントが接続できない

```bash
# 各エージェントの .env を確認
cat agents/agent_1/.env
```

DISCORD_TOKEN と GUILD_ID が正しく設定されているか確認してください。

## 📝 テスト後の後片付け

テスト完了後、元の設定に戻してください：

```bash
# 元の .env に戻す（必要に応じて）
cp .env.backup .env

# または .env.example をベースに再設定
cp .env.example .env
vim .env
```

**重要**: `RANDOM_ELIMINATION_CHANCE=100` はテスト用設定です。本番環境では `false` または適切な確率（10-50）に設定してください。

## 🎯 テストシナリオ

### シナリオ1: ランダム脱落が発生する場合

```bash
# .env で設定
RANDOM_ELIMINATION_ENABLED=true
RANDOM_ELIMINATION_CHANCE=100
```

期待結果:
- 投票なし → 必ずランダム脱落が発生

### シナリオ2: ランダム脱落が発生しない場合

```bash
# .env で設定
RANDOM_ELIMINATION_ENABLED=false
```

期待結果:
- 投票なし → 誰も脱落しない

### シナリオ3: 50%の確率で発生

```bash
# .env で設定
RANDOM_ELIMINATION_ENABLED=true
RANDOM_ELIMINATION_CHANCE=50
```

期待結果:
- 投票なし → 50%の確率でランダム脱落

---

……ふふ、これでテストできるね！
