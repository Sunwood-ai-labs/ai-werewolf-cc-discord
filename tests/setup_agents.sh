#!/bin/bash
#
# エージェント環境変数設定スクリプト
#
# メインの .env から各エージェントの .env を自動生成します
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
MAIN_ENV="$PROJECT_ROOT/.env"

echo ""
log "════════════════════════════════════════════════════════════"
log "🔧 エージェント環境変数設定"
log "════════════════════════════════════════════════════════════"
echo ""

# メインの.envが存在するか確認
if [ ! -f "$MAIN_ENV" ]; then
    log_error ".env が見つかりません"
    log_info "まず .env.example をコピーして設定してください:"
    log "  cp .env.example .env"
    log "  vim .env"
    exit 1
fi

log "メインの .env から各エージェントの .env を生成します..."
echo ""

# メインの.envから値を読み込む
GUILD_ID=$(grep "^GUILD_ID=" "$MAIN_ENV" | cut -d'=' -f2)

if [ -z "$GUILD_ID" ]; then
    log_error "GUILD_ID が .env に設定されていません"
    exit 1
fi

log_success "GUILD_ID: $GUILD_ID"
echo ""

# 各エージェントの.envを生成
for i in {1..6}; do
    agent_dir="$AGENTS_DIR/agent_$i"
    env_file="$agent_dir/.env"

    # トークン変数名
    token_var="AGENT_${i}_TOKEN"
    agent_id="agent-$i"

    # メインの.envからトークンを取得
    token=$(grep "^${token_var}=" "$MAIN_ENV" | cut -d'=' -f2)

    if [ -z "$token" ]; then
        log_warning "${token_var} が .env に設定されていません"
        continue
    fi

    # .envを生成
    cat > "$env_file" <<EOF
# ========================================
# Agent $i Settings
# ========================================

# Discord Bot Token (このエージェント用)
DISCORD_TOKEN=$token

# Discord Server ID
GUILD_ID=$GUILD_ID

# エージェント ID
AGENT_ID=$agent_id
EOF

    log_success "作成しました: agents/agent_$i/.env"
done

echo ""
log_success "✅ 全エージェントの .env 設定完了"
echo ""
log_info "確認コマンド:"
log "  cd agents/agent_1 && uv run werewolf whoami"
log ""
log_info "これでテストスクリプトを実行できます:"
log "  ./tests/test_seer.sh"
echo ""
