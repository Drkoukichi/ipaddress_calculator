#!/bin/bash

# IPアドレス計算ツール用Snapパッケージビルドスクリプト
# このスクリプトは以下の処理を行います：
# 1. ipaddress_calculator/ipfx.py から実行可能な ipfx ファイルを作成
# 2. snapcraft でパッケージをビルド
# 3. 作成されたsnapファイルを確認

set -e  # エラーが発生したら即座に終了

# 色付きメッセージ用の定数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ出力関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# プロジェクトのルートディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "IPアドレス計算ツールのビルドを開始します..."

# 必要なファイルの存在確認
if [ ! -f "ipaddress_calculator/ipfx.py" ]; then
    log_error "ipaddress_calculator/ipfx.py が見つかりません"
    exit 1
fi

if [ ! -f "snap/snapcraft.yaml" ]; then
    log_error "snap/snapcraft.yaml が見つかりません"
    exit 1
fi

log_info "必要なファイルの存在を確認しました"

# 既存のipfxファイルがあれば削除
if [ -f "ipfx" ]; then
    log_warning "既存の ipfx ファイルを削除します"
    rm -f ipfx
fi

# ipaddress_calculator/ipfx.py から実行可能な ipfx ファイルを作成
log_info "ipaddress_calculator/ipfx.py から実行可能ファイル ipfx を作成中..."

# shebangを追加してipfxファイルを作成
echo '#!/usr/bin/env python3' > ipfx
cat ipaddress_calculator/ipfx.py >> ipfx

# 実行権限を付与
chmod +x ipfx

log_success "実行可能ファイル ipfx を作成しました"

# snapcraft の存在確認
if ! command -v snapcraft &> /dev/null; then
    log_error "snapcraft がインストールされていません"
    log_info "snapcraft をインストールしてください: sudo snap install snapcraft --classic"
    exit 1
fi

log_info "snapcraft の存在を確認しました"

# 既存のビルドをクリーンアップ
log_info "既存のビルドをクリーンアップ中..."
snapcraft clean > /dev/null 2>&1 || true

# snapcraft でビルド実行
log_info "snapcraft でパッケージをビルド中..."
log_info "この処理には数分かかる場合があります..."

if snapcraft; then
    log_success "snapcraft ビルドが完了しました"
else
    log_error "snapcraft ビルドに失敗しました"
    exit 1
fi

# 作成されたsnapファイルを確認
SNAP_FILES=(*.snap)
if [ -f "${SNAP_FILES[0]}" ]; then
    for snap_file in *.snap; do
        if [ -f "$snap_file" ]; then
            file_size=$(du -h "$snap_file" | cut -f1)
            log_success "snapパッケージが作成されました: $snap_file (サイズ: $file_size)"
            
            # パッケージの詳細情報を表示
            log_info "パッケージの詳細情報:"
            echo "  ファイル名: $snap_file"
            echo "  サイズ: $file_size"
            echo "  作成日時: $(stat -c %y "$snap_file")"
        fi
    done
else
    log_error "snapパッケージファイルが見つかりません"
    exit 1
fi

# インストール手順の案内
echo ""
log_info "=== インストール手順 ==="
echo "以下のコマンドでパッケージをインストールできます:"
echo ""
for snap_file in *.snap; do
    if [ -f "$snap_file" ]; then
        echo "  sudo snap install ./$snap_file --dangerous"
        break
    fi
done
echo ""
echo "インストール後、以下のコマンドでエイリアスを設定できます:"
echo "  sudo snap alias <パッケージ名>.ipfx ipfx"
echo ""
echo "使用例:"
echo "  ipfx 192.168.1.1/24"
echo "  ipfx 2001:db8::1/64"
echo ""

log_success "ビルドプロセスが完了しました！"
