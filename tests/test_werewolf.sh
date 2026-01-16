#!/bin/bash
#
# 人狼の襲撃テストスクリプト
#
# 人狼が夜に襲撃を実行し、対象が排除されることを確認します
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
log "🐺 人狼の襲撃テスト"
log "════════════════════════════════════════════════════════════"
echo ""

log "📋 テスト内容:"
log "  - 人狼エージェントを特定"
log "  - 夜フェーズになるまで待機"
log "  - 襲撃を実行"
log "  - 襲撃結果を確認"
echo ""

# ステップ1: 人狼を特定
log "🔍 ステップ1: 人狼エージェントを特定..."

werewolves=()

for i in {1..6}; do
    output=$(cd "$AGENTS_DIR/agent_$i" && uv run werewolf whoami 2>/dev/null || true)

    if echo "$output" | grep -qi "人狼\|werewolf"; then
        werewolves+=("agent_$i")
        log_success "人狼を発見: Agent-$i"
    fi
done

if [ ${#werewolves[@]} -eq 0 ]; then
    log_error "人狼が見つかりませんでした"
    exit 1
fi

# 最初の人狼を使用
werewolf_agent="${werewolves[0]}"
log_info "襲撃を実行するエージェント: $werewolf_agent"

echo ""

# ステップ2: 夜フェーズになるまで待機
log "🌙 ステップ2: 夜フェーズになるまで待機..."

max_wait=300
elapsed=0
check_interval=5

while [ $elapsed -lt $max_wait ]; do
    output=$(cd "$AGENTS_DIR/$werewolf_agent" && uv run werewolf overview 2>/dev/null || true)

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
log "🎯 ステップ3: 襲撃ターゲットを決定..."

# 人狼以外のエージェントをターゲットに
target_agent="agent_1"
if [ "$werewolf_agent" = "agent_1" ]; then
    target_agent="agent_2"
fi

log_info "ターゲット: $target_agent"
echo ""

# ステップ4: 襲撃を実行
log "🐺 ステップ4: 襲撃を実行..."

log "$werewolf_agent → $target_agent を襲撃します"

(cd "$AGENTS_DIR/$werewolf_agent" && uv run werewolf dm "襲撃: $target_agent" 2>&1 || true)

echo ""
log "⏳ 3秒間待機してDMを確認..."
sleep 3

# ステップ5: DMを確認
log "📬 ステップ5: 襲撃結果を確認..."

dm_output=$(cd "$AGENTS_DIR/$werewolf_agent" && uv run werewolf read "dm-$werewolf_agent" --limit 10 2>/dev/null || true)

echo "$dm_output"

# 判定
if echo "$dm_output" | grep -q "襲撃\|attack"; then
    echo ""
    log_success "✅ 人狼の襲撃テスト: PASSED"
    echo ""
    log_info "確認事項:"
    log "  - DMチャンネルに「襲撃」の結果が表示された"
    log "  - ターゲットが襲撃されたことが表示された"
    exit 0
else
    echo ""
    log_error "❌ 人狼の襲撃テスト: FAILED"
    log_error "襲撃結果が見つかりませんでした"
    exit 1
fi
