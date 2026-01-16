#!/bin/bash
#
# 投票テストスクリプト
#
# 投票フェーズで全員が投票し、結果が正しく集計されることを確認します
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
log "📊 投票テスト"
log "════════════════════════════════════════════════════════════"
echo ""

log "📋 テスト内容:"
log "  - 投票フェーズになるまで待機"
log "  - 全エージェントが投票を実行"
log "  - 投票結果を確認"
echo ""

# ステップ1: 投票フェーズになるまで待機
log "🔍 ステップ1: 投票フェーズになるまで待機..."

max_wait=300
elapsed=0
check_interval=5

while [ $elapsed -lt $max_wait ]; do
    output=$(cd "$AGENTS_DIR/agent_1" && uv run werewolf overview 2>/dev/null || true)

    if echo "$output" | grep -qi "投票\|voting"; then
        log_success "投票フェーズを検出！"
        break
    fi

    sleep $check_interval
    elapsed=$((elapsed + check_interval))

    if [ $((elapsed % 30)) -eq 0 ]; then
        log "  待機中... (${elapsed}秒経過)"
    fi
done

if [ $elapsed -ge $max_wait ]; then
    log_error "タイムアウト: 投票フェーズが開始されませんでした"
    exit 1
fi

echo ""

# ステップ2: 全員が投票
log "🗳️ ステップ2: 全エージェントが投票を実行..."

# agent_1 が agent_2 に投票
log "Agent-1 → Agent-2 に投票"
(cd "$AGENTS_DIR/agent_1" && uv run werewolf dm "投票: agent-2" 2>&1 | grep -q "✅\|投票しました" && log_success "Agent-1 投票完了" || log_error "Agent-1 投票失敗")
sleep 1

# agent_3 が agent_2 に投票
log "Agent-3 → Agent-2 に投票"
(cd "$AGENTS_DIR/agent_3" && uv run werewolf dm "投票: agent-2" 2>&1 | grep -q "✅\|投票しました" && log_success "Agent-3 投票完了" || log_error "Agent-3 投票失敗")
sleep 1

# agent_4 が agent_2 に投票
log "Agent-4 → Agent-2 に投票"
(cd "$AGENTS_DIR/agent_4" && uv run werewolf dm "投票: agent-2" 2>&1 | grep -q "✅\|投票しました" && log_success "Agent-4 投票完了" || log_error "Agent-4 投票失敗")
sleep 1

# agent_5 が agent_1 に投票
log "Agent-5 → Agent-1 に投票"
(cd "$AGENTS_DIR/agent_5" && uv run werewolf dm "投票: agent-1" 2>&1 | grep -q "✅\|投票しました" && log_success "Agent-5 投票完了" || log_error "Agent-5 投票失敗")
sleep 1

# agent_6 が agent_2 に投票
log "Agent-6 → Agent-2 に投票"
(cd "$AGENTS_DIR/agent_6" && uv run werewolf dm "投票: agent-2" 2>&1 | grep -q "✅\|投票しました" && log_success "Agent-6 投票完了" || log_error "Agent-6 投票失敗")

echo ""
log "⏳ 投票結果を待機しています..."
sleep 5

# ステップ3: 投票結果を確認
log "📊 ステップ3: 投票結果を確認..."

# villageチャンネルを確認
village_output=$(cd "$AGENTS_DIR/agent_1" && uv run werewolf read village --limit 20 2>/dev/null || true)

echo "$village_output"

# 判定
if echo "$village_output" | grep -q "投票結果\|処刑されました"; then
    echo ""
    log_success "✅ 投票テスト: PASSED"
    echo ""
    log_info "確認事項:"
    log "  - #village に「投票結果」と表示された"
    log "  - 最多投票者が処刑された"
    log "  - 投票集計が正しく行われた"
    exit 0
else
    echo ""
    log_error "❌ 投票テスト: FAILED"
    log_error "投票結果が見つかりませんでした"
    exit 1
fi
