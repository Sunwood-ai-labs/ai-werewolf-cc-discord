#!/bin/bash
#
# 役職配布テストスクリプト
#
# ゲーム開始時の役職配布が正しく行われることを確認します
#

set -e

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"

echo ""
log "════════════════════════════════════════════════════════════"
log "🎭 役職配布テスト"
log "════════════════════════════════════════════════════════════"
echo ""

log "📋 テスト内容:"
log "  - 各エージェントの役職を確認"
log "  - 人狼が2名であることを確認"
log "  - 占い師が1名であることを確認"
log "  - 騎士が1名であることを確認"
log "  - 村人が2名であることを確認"
echo ""

log "⏳ テスト開始..."
echo ""

seer_found=false
knight_found=false
werewolf_count=0
villager_count=0
roles_summary=""

# 各エージェントの役職を確認
for i in {1..6}; do
    log "=== Agent-$i 役職確認 ==="

    # whoami で役職を確認
    output=$(cd "$AGENTS_DIR/agent_$i" && uv run werewolf whoami 2>/dev/null || true)

    echo "$output"

    # 役職を判定
    if echo "$output" | grep -qi "人狼\|werewolf"; then
        werewolf_count=$((werewolf_count + 1))
        roles_summary="${roles_summary}[✗] Agent-$i: 🐺 人狼\n"
    elif echo "$output" | grep -qi "占い師\|seer"; then
        seer_found=true
        roles_summary="${roles_summary}[✓] Agent-$i: 👁️ 占い師\n"
    elif echo "$output" | grep -qi "騎士\|knight"; then
        knight_found=true
        roles_summary="${roles_summary}[✓] Agent-$i: 🛡️ 騎士\n"
    else
        villager_count=$((villager_count + 1))
        roles_summary="${roles_summary}[✓] Agent-$i: 👤 村人\n"
    fi

    echo ""
done

# 結果集計
echo ""
log "════════════════════════════════════════════════════════════"
log "📊 役職配布結果"
log "════════════════════════════════════════════════════════════"
echo ""
echo -e "$roles_summary"

log "集計:"
echo "  🐺 人狼: $werewolf_count/2 (期待: 2)"
echo "  👁️ 占い師: $( [ "$seer_found" = true ] && echo "1/1" || echo "0/1" ) (期待: 1)"
echo "  🛡️ 騎士: $( [ "$knight_found" = true ] && echo "1/1" || echo "0/1" ) (期待: 1)"
echo "  👤 村人: $villager_count/2 (期待: 2)"
echo ""

# 判定
if [ "$werewolf_count" -eq 2 ] && [ "$seer_found" = true ] && [ "$knight_found" = true ] && [ "$villager_count" -eq 2 ]; then
    log_success "✅ 役職配布テスト: PASSED"
    exit 0
else
    log_error "❌ 役職配布テスト: FAILED"
    exit 1
fi
