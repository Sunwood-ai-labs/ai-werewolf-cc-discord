#!/bin/bash
#
# 全テスト実行スクリプト
#
# 全てのテストを順番に実行し、結果をまとめて表示します
#

set -e

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_header() { echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"; echo -e "${MAGENTA}$1${NC}"; echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"; }

TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"

# テスト結果のカウンター
total_tests=0
passed_tests=0
failed_tests=0

# テストを実行する関数
run_test() {
    local test_name=$1
    local test_script=$2

    total_tests=$((total_tests + 1))

    echo ""
    log_header "🧪 テスト $total_tests: $test_name"

    if bash "$test_script"; then
        passed_tests=$((passed_tests + 1))
        log_success "$test_name: PASSED"
    else
        failed_tests=$((failed_tests + 1))
        log_error "$test_name: FAILED"
    fi
}

# メイン処理
main() {
    echo ""
    log_header "🎮 人狼ゲーム 全テスト実行"
    echo ""

    log "📋 実行するテスト:"
    log "  1. 役職配布テスト"
    log "  2. 占い師テスト"
    log "  3. 騎士の護衛テスト"
    log "  4. 人狼の襲撃テスト"
    log "  5. 投票テスト"
    log "  6. ランダム脱落テスト"
    echo ""

    log "⏳ テスト開始..."
    echo ""

    # テスト1: 役職配布
    run_test "役職配布テスト" "$TESTS_DIR/test_role_assignment.sh"

    # テスト2: 占い師
    run_test "占い師テスト" "$TESTS_DIR/test_seer.sh"

    # テスト3: 騎士の護衛
    run_test "騎士の護衛テスト" "$TESTS_DIR/test_knight.sh"

    # テスト4: 人狼の襲撃
    run_test "人狼の襲撃テスト" "$TESTS_DIR/test_werewolf.sh"

    # テスト5: 投票
    run_test "投票テスト" "$TESTS_DIR/test_voting.sh"

    # テスト6: ランダム脱落
    run_test "ランダム脱落テスト" "$TESTS_DIR/test_random_elimination.sh"

    # 結果集計
    echo ""
    log_header "📊 テスト結果"
    echo ""

    echo "  実行したテスト: $total_tests"
    echo -e "  ${GREEN}成功: $passed_tests${NC}"
    echo -e "  ${RED}失敗: $failed_tests${NC}"

    if [ $failed_tests -eq 0 ]; then
        echo ""
        log_success "🎉 全テスト PASSED！"
        exit 0
    else
        echo ""
        log_error "❌ 一部のテストが FAILED しました"
        exit 1
    fi
}

# 割り込みハンドラ
trap 'log_error "⚠️ ユーザーにより中断されました"; exit 130' INT

# 実行
main
