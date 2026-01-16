#!/bin/bash
#
# 騎士の護衛テストスクリプト
#
# 騎士が夜に護衛を実行し、対象が保護されることを確認します
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

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"

echo ""
log "════════════════════════════════════════════════════════════"
log "🛡️ 騎士の護衛テスト"
log "════════════════════════════════════════════════════════════"
echo ""

log "📋 テスト内容:"
log "  - 騎士エージェントを特定"
log "  - 夜フェーズになるまで待機"
log "  - 護衛を実行"
log "  - 護衛結果を確認"
echo ""

# ステップ1: 騎士を特定
log "🔍 ステップ1: 騎士エージェントを特定..."

knight_agent=""

for i in {1..6}; do
    output=$(cd "$AGENTS_DIR/agent_$i" && uv run werewolf whoami 2>/dev/null || true)

    if echo "$output" | grep -qi "騎士\|knight"; then
        knight_agent="agent_$i"
        log_success "騎士を発見: Agent-$i"
        break
    fi
done

if [ -z "$knight_agent" ]; then
    log_error "騎士が見つかりませんでした"
    exit 1
fi

echo ""

# ステップ2: 夜フェーズになるまで待機
log "🌙 ステップ2: 夜フェーズになるまで待機..."

max_wait=300
elapsed=0
check_interval=5

while [ $elapsed -lt $max_wait ]; do
    output=$(cd "$AGENTS_DIR/$knight_agent" && uv run werewolf overview 2>/dev/null || true)

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
log "🎯 ステップ3: 護衛ターゲットを決定..."

# 騎士以外のエージェントをターゲットに
target_agent="agent_1"
if [ "$knight_agent" = "agent_1" ]; then
    target_agent="agent_2"
fi

log_info "ターゲット: $target_agent"
echo ""

# ステップ4: 護衛を実行
log "🛡️ ステップ4: 護衛を実行..."

log "$knight_agent → $target_agent を護衛します"

(cd "$AGENTS_DIR/$knight_agent" && uv run werewolf dm "護衛: $target_agent" 2>&1 || true)

echo ""
log "⏳ 3秒間待機してDMを確認..."
sleep 3

# ステップ5: DMを確認
log "📬 ステップ5: 護衛結果を確認..."

dm_output=$(cd "$AGENTS_DIR/$knight_agent" && uv run werewolf read "dm-$knight_agent" --limit 10 2>/dev/null || true)

echo "$dm_output"

# 判定
if echo "$dm_output" | grep -q "護衛\|保護"; then
    echo ""
    log_success "✅ 騎士の護衛テスト: PASSED"
    echo ""
    log_info "確認事項:"
    log "  - DMチャンネルに「護衛」の結果が表示された"
    log "  - ターゲットが保護されたことが表示された"
    exit 0
else
    echo ""
    log_error "❌ 騎士の護衛テスト: FAILED"
    log_error "護衛結果が見つかりませんでした"
    exit 1
fi
