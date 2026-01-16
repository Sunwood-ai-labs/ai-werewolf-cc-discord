#!/bin/bash
#
# 全エージェントの役職一覧表示
#
# すべてのエージェントの whoami を一括表示します
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

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"

echo ""
echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"
echo -e "${MAGENTA}🎭 全エージェント役職一覧${NC}"
echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"
echo ""

for i in {1..6}; do
    agent_dir="$AGENTS_DIR/agent_$i"

    echo -e "${CYAN}═══ Agent-$i ═══${NC}"

    if [ -f "$agent_dir/.env" ]; then
        (cd "$agent_dir" && uv run werewolf whoami 2>&1 | grep -v "Unclosed\|connections:\|connector:" || true)
    else
        echo -e "${RED}[✗] .env が見つかりません${NC}"
    fi

    echo ""
done

echo -e "${MAGENTA}════════════════════════════════════════════════════════════${NC}"
