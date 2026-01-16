#!/bin/bash
#
# インタラクティブ エージェント操作スクリプト
#
# 各エージェントになりかわってDiscordに操作を送信できます
#
# 使用方法:
#   ./tests/interactive.sh
#

set -e

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# プロジェクトルート
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"
CURRENT_AGENT="agent_1"

# ヘルプ関数
show_help() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}🎮 インタラクティブ エージェント操作${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}現在のエージェント:${NC} ${YELLOW}$CURRENT_AGENT${NC}"
    echo ""
    echo -e "${GREEN}コマンド一覧:${NC}"
    echo "  agent [1-6]       エージェントを切り替え"
    echo "  overview          全体状況を確認"
    echo "  whoami            自分の状態を確認"
    echo "  channels          アクセス可能チャンネル一覧"
    echo "  read [channel]    チャンネルを読む (village, werewolf-room, graveyard)"
    echo "  say [message]     村の広場で発言"
    echo "  dm [message]      GMにDM送信 (投票: agent-X, 占い: agent-X, 護衛: agent-X)"
    echo "  wait [seconds]    指定秒数待機 (投票時間切れ待ち用)"
    echo "  help              このヘルプを表示"
    echo "  exit              終了"
    echo ""
    echo -e "${YELLOW}例:${NC}"
    echo "  agent 2           → agent_2 に切り替え"
    echo "  say おはよう       → 「おはよう」と発言"
    echo "  dm 投票: agent-3   → agent-3 に投票"
    echo "  wait 35           → 35秒待機"
    echo ""
}

# エージェント切り替え関数
switch_agent() {
    local num=$1
    if [ "$num" -ge 1 ] && [ "$num" -le 6 ]; then
        CURRENT_AGENT="agent_$num"
        echo -e "${GREEN}[✓]${NC} ${YELLOW}$CURRENT_AGENT${NC} に切り替えました"
    else
        echo -e "${RED}[✗]${NC} 無効なエージェント番号: $num (1-6を指定してください)"
    fi
}

# コマンド実行関数
run_command() {
    local cmd=$1
    shift
    local args="$@"

    echo -e "${BLUE}[${CURRENT_AGENT}]${NC} $cmd $args"

    (cd "$AGENTS_DIR/$CURRENT_AGENT" && uv run werewolf $cmd $args 2>&1 || true)
}

# メインループ
main() {
    show_help

    while true; do
        echo -ne "${CYAN}[${CURRENT_AGENT}]> ${NC}"
        read -r input

        # 空入力は無視
        [ -z "$input" ] && continue

        # コマンドパース
        cmd=$(echo "$input" | awk '{print $1}')
        args=$(echo "$input" | cut -d' ' -f2-)

        case "$cmd" in
            agent)
                switch_agent "$args"
                ;;
            overview)
                run_command "overview"
                ;;
            whoami)
                run_command "whoami"
                ;;
            channels)
                run_command "channels"
                ;;
            read)
                if [ -z "$args" ]; then
                    echo -e "${YELLOW}[!] チャンネル名を指定してください${NC}"
                else
                    run_command "read" "$args"
                fi
                ;;
            say)
                if [ -z "$args" ]; then
                    echo -e "${YELLOW}[!] メッセージを指定してください${NC}"
                else
                    run_command "say" "village" "$args"
                fi
                ;;
            dm)
                if [ -z "$args" ]; then
                    echo -e "${YELLOW}[!] DM内容を指定してください${NC}"
                else
                    run_command "dm" "$args"
                fi
                ;;
            wait)
                if [ -z "$args" ]; then
                    echo -e "${YELLOW}[!] 待機秒数を指定してください${NC}"
                else
                    echo -e "${BLUE}[⏱️] ${args}秒間待機します...${NC}"
                    sleep "$args"
                fi
                ;;
            help)
                show_help
                ;;
            exit|quit)
                echo -e "${GREEN}[✓] 終了します${NC}"
                break
                ;;
            *)
                echo -e "${RED}[✗]${NC} 不明なコマンド: $cmd (help で確認)"
                ;;
        esac

        echo ""
    done
}

# 割り込みハンドラ
trap 'echo -e "\n${YELLOW}[!] 中断されました${NC}"; exit 130' INT

main
