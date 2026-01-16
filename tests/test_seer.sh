#!/bin/bash
#
# 占い師テストスクリプト
#
# 占い師が夜に占いを実行し、結果が正しく返ってくることを確認します
#

set -e

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_info() { echo -e "${CYAN}[i]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"

echo ""
log "════════════════════════════════════════════════════════════"
log "👁️ 占い師テスト"
log "════════════════════════════════════════════════════════════"
echo ""

# 事前チェック
log "🔍 事前チェック..."

# エージェントの.envが設定されているか確認
if [ ! -f "$AGENTS_DIR/agent_1/.env" ]; then
    log_warning "agent_1/.env が見つかりません"
    log ""
    log_info "各エージェントの .env を設定してください:"
    log "  cp agents/agent_1/.env.example agents/agent_1/.env"
    log "  vim agents/agent_1/.env"
    log ""
    log_error "テストを中止します"
    exit 1
fi

log_success "エージェントの.env設定を確認しました"
echo ""

log "📋 テスト内容:"
log "  - 占い師エージェントを特定"
log "  - 夜フェーズになるまで待機"
log "  - 占いを実行"
log "  - 占い結果を確認"
echo ""

# ステップ1: 占い師を特定
log "🔍 ステップ1: 占い師エージェントを特定..."

seer_agent=""

for i in {1..6}; do
    # whoami で役職を確認
    output=$(cd "$AGENTS_DIR/agent_$i" && uv run werewolf whoami 2>/dev/null || true)

    # デバッグ用に出力を表示
    if [ -n "$output" ]; then
        echo "$output" | head -5
    fi

    if echo "$output" | grep -qi "占い師\|seer"; then
        seer_agent="agent_$i"
        log_success "占い師を発見: Agent-$i"
        break
    fi
done

if [ -z "$seer_agent" ]; then
    echo ""
    log_error "占い師が見つかりませんでした"
    echo ""
    log_info "考えられる原因:"
    log "  1. ゲームがまだ開始されていない"
    log "  2. エージェントの.env設定が不正"
    log "  3. GM Botが起動していない"
    echo ""
    log_info "確認コマンド:"
    log "  cd agents/agent_1 && uv run werewolf whoami"
    exit 1
fi

echo ""

# ステップ2: 夜フェーズになるまで待機
log "🌙 ステップ2: 夜フェーズになるまで待機..."

max_wait=300
elapsed=0
check_interval=5

while [ $elapsed -lt $max_wait ]; do
    output=$(cd "$AGENTS_DIR/$seer_agent" && uv run werewolf overview 2>/dev/null || true)

    if echo "$output" | grep -qi "夜\|night"; then
        log_success "夜フェーズを検出！"
        break
    fi

    sleep $check_interval
    elapsed=$((elapsed + check_interval))

    if [ $((elapsed % 30)) -eq 0 ]; then
        log "  待機中... (${elapsed}秒経過)"
    fi
done

if [ $elapsed -ge $max_wait ]; then
    log_error "タイムアウト: 夜フェーズが開始されませんでした"
    exit 1
fi

echo ""

# ステップ3: ターゲットを決定
log "🎯 ステップ3: 占いターゲットを決定..."

# 占い師以外のエージェントをターゲットに
target_agent="agent_1"
if [ "$seer_agent" = "agent_1" ]; then
    target_agent="agent_2"
fi

log_info "ターゲット: $target_agent"
echo ""

# ステップ4: 占いを実行
log "🔮 ステップ4: 占いを実行..."

log "$seer_agent → $target_agent を占います"

result=$(cd "$AGENTS_DIR/$seer_agent" && uv run werewolf dm "占い: $target_agent" 2>&1 || true)

echo "$result"

if echo "$result" | grep -q "✅\|成功\|占います"; then
    log_success "占いコマンド送信成功"
elif echo "$result" | grep -q "⚠️\|エラー\|失敗"; then
    log_error "占いコマンド送信失敗"
    exit 1
fi

echo ""
log "⏳ 3秒間待機してDMを確認..."
sleep 3

# ステップ5: DMを確認
log "📬 ステップ5: 占い結果を確認..."

dm_output=$(cd "$AGENTS_DIR/$seer_agent" && uv run werewolf read "dm-$seer_agent" --limit 10 2>/dev/null || true)

echo "$dm_output"

# 判定
if echo "$dm_output" | grep -q "占い結果"; then
    echo ""
    log_success "✅ 占い師テスト: PASSED"
    echo ""
    log_info "確認事項:"
    log "  - DMチャンネルに「占い結果」と表示された"
    log "  - ターゲットが人狼かどうかの判定が表示された"
    exit 0
else
    echo ""
    log_error "❌ 占い師テスト: FAILED"
    log_error "占い結果が見つかりませんでした"
    exit 1
fi
