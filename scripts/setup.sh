#!/bin/bash

# =================================================================
# Claude Common Assets Setup Script
# =================================================================

CLAUDE_DIR="$HOME/.claude"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🚀 Starting Claude configuration sync..."

# Create backup directory if it doesn't exist
BACKUP_DIR="$CLAUDE_DIR/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Function to create safe symlinks
link_asset() {
    local src=$1
    local dest=$2

    if [ -e "$dest" ] || [ -L "$dest" ]; then
        echo "📦 Backing up existing $(basename "$dest") to $BACKUP_DIR"
        mv "$dest" "$BACKUP_DIR/"
    fi

    echo "🔗 Linking $src -> $dest"
    ln -s "$src" "$dest"
}

# 1. Link CLAUDE.md (Global Rules)
link_asset "$REPO_DIR/rules/global.md" "$CLAUDE_DIR/CLAUDE.md"

# 2. Link Skills directory
link_asset "$REPO_DIR/skills" "$CLAUDE_DIR/skills"

# 3. Link Knowledge directory
link_asset "$REPO_DIR/knowledge" "$CLAUDE_DIR/knowledge"

echo "✅ Setup complete! Claude is now powered by your git-managed assets."
echo "💡 Remember to restart your Claude session to apply major changes."
