#!/bin/bash
#
# ランダム脱落機能のテストスクリプト（シェル版）
#
# 使用方法:
#   1. GM Bot を起動しておく (.env で RANDOM_ELIMINATION_ENABLED=true)
#   2. このスクリプトを実行: ./tests/test_random_elimination.sh
#

set -e

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# プロジェクトルート
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"

echo ""
log "════════════════════════════════════════════════════════════"
log "🎲 ランダム脱落機能テスト（シェル版）"
log "════════════════════════════════════════════════════════════"
echo ""

log "📋 前提条件:"
log "  1. GM Bot が起動していること"
log "  2. .env で RANDOM_ELIMINATION_ENABLED=true であること"
log "  3. ゲームが進行中であること"
echo ""

log "📝 テスト内容:"
log "  - 投票フェーズになるまで待機"
log "  - 誰も投票せずに時間切れまで待機"
log "  - ランダム脱落が発生することを確認"
echo ""

log "⏳ テスト開始..."
echo ""

# 投票フェーズ検出関数
wait_for_voting_phase() {
    local max_wait=300  # 最大5分
    local elapsed=0
    local check_interval=5

    log "🔍 投票フェーズを待機中..."

    while [ $elapsed -lt $max_wait ]; do
        # agent_1 の状況を確認
        local output
        output=$(cd "$AGENTS_DIR/agent_1" && uv run werewolf overview 2>/dev/null || true)

        # 投票フェーズの判定
        if echo "$output" | grep -qi "投票\|voting"; then
            log_success "投票フェーズを検出！"
            return 0
        fi

        sleep $check_interval
        elapsed=$((elapsed + check_interval))

        # 進捗表示
        if [ $((elapsed % 30)) -eq 0 ]; then
            log "  待機中... (${elapsed}秒経過)"
        fi
    done

    log_error "タイムアウト: 投票フェーズが開始されませんでした"
    return 1
}

# 投票せずに待機関数
wait_for_timeout() {
    local voting_time=35  # 投票時間20秒 + 余裕

    log "⏰ 投票時間を待機中... (誰も投票しません)"
    log "  ${voting_time}秒間、何もせず待機します..."

    sleep $voting_time

    log_success "投票時間が経過しました"
}

# 結果確認関数
check_results() {
    log ""
    log "📊 各エージェントの状況を確認中..."

    for i in {1..6}; do
        echo ""
        log "=== Agent-$i 状況 ==="
        (cd "$AGENTS_DIR/agent_$i" && uv run werewolf overview 2>/dev/null || true) | head -20
    done
}

# メイン処理
main() {
    # 投票フェーズになるまで待機
    if ! wait_for_voting_phase; then
        log_error "テスト失敗: 投票フェーズを検出できませんでした"
        exit 1
    fi

    # 誰も投票せずに待機
    wait_for_timeout

    # 結果を確認
    check_results

    # 完了メッセージ
    echo ""
    log "════════════════════════════════════════════════════════════"
    log_success "✅ テスト完了"
    log "════════════════════════════════════════════════════════════"
    echo ""
    log "🎲 確認事項:"
    log "  - #village チャンネルに「誰も投票しませんでした」と表示されたか？"
    log "  - ランダム脱落が発生したか？ (「🎲 運命の選択...」)"
    log "  - 脱落したプレイヤーが #graveyard に追加されたか？"
    echo ""
}

# 割り込みハンドラ
trap 'log_warning "⚠️ ユーザーにより中断されました"; exit 130' INT

# 実行
main "$@"
