[![ipfx](https://snapcraft.io/ipfx/badge.svg)](https://snapcraft.io/ipfx)

# IP Address Calculator (ipfx)

A comprehensive command-line tool for IP address calculations and network analysis.

[日本語版はこちら](#日本語版) | [English Version](#english-version)

## English Version

### Features

- **IPv4 and IPv6 Support**: Calculate network information for both IPv4 and IPv6 addresses
- **Multiple Output Formats**: CIDR notation, Cisco notation, and Ubuntu subnet notation
- **Interactive Mode**: Continuous calculation mode for multiple addresses
- **Command-line Mode**: Perfect for scripting and automation
- **Detailed Information**: Network address, broadcast address, host count, and more
- **Lightweight**: Fast execution with no external dependencies

### Installation

#### From Snap Store
```bash
sudo snap install ipfx
sudo snap alias ipfx.ipfx ipfx
```

#### From Source
```bash
git clone https://github.com/Drkoukichi/ip-address-culcurator.git
cd ip-address-culcurator
./build.sh
sudo snap install ./ipfx_*.snap --dangerous
sudo snap alias ipfx.ipfx ipfx
```

### Usage

#### Command-line Mode
```bash
# IPv4 example
ipfx 192.168.1.1/24

# IPv6 example  
ipfx 2001:db8::1/64
```

#### Interactive Mode
```bash
ipfx
address: 192.168.1.1/24
address: 10.0.0.1/8
address: exit
```

### Output Example

```
==========IPv4 Address Information==========
ipaddress: 192.168.1.1
network_address: 192.168.1.0
broadcast_address: 192.168.1.255
host_count: 254
is_private: True
is_global: False
is_network_address: False
is_broadcast_address: False
reverse: 1.1.168.192.in-addr.arpa
cidr_notation: 192.168.1.1/24
cisco_notation: 192.168.1.1 255.255.255.0
ubuntu_subnet: 192.168.1.0/24
=============================================
```

### Building

Use the provided build script to create a snap package:

```bash
./build.sh
```

This script will:
1. Create an executable from `ipaddress_calculator/ipfx.py`
2. Build the snap package using snapcraft
3. Provide installation instructions

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 日本語版

IPアドレス計算とネットワーク解析のための包括的なコマンドラインツールです。

### 機能

- **IPv4とIPv6対応**: IPv4とIPv6の両方のアドレスのネットワーク情報を計算
- **複数の出力形式**: CIDR記法、Cisco記法、Ubuntu記法に対応
- **対話モード**: 複数のアドレスを連続して計算できる対話モード
- **コマンドラインモード**: スクリプトや自動化に最適
- **詳細情報**: ネットワークアドレス、ブロードキャストアドレス、ホスト数など
- **軽量**: 外部依存関係なしで高速実行

### インストール方法

#### Snap Storeから
```bash
sudo snap install ipfx
sudo snap alias ipfx.ipfx ipfx
```

#### ソースから
```bash
git clone https://github.com/Drkoukichi/ip-address-culcurator.git
cd ip-address-culcurator
./build.sh
sudo snap install ./ipfx_*.snap --dangerous
sudo snap alias ipfx.ipfx ipfx
```

### 使用方法

#### コマンドラインモード
```bash
# IPv4の例
ipfx 192.168.1.1/24

# IPv6の例
ipfx 2001:db8::1/64
```

#### 対話モード
```bash
ipfx
address: 192.168.1.1/24
address: 10.0.0.1/8
address: exit
```

### 出力例

```
==========IPv4 Address Information==========
ipaddress: 192.168.1.1
network_address: 192.168.1.0
broadcast_address: 192.168.1.255
host_count: 254
is_private: True
is_global: False
is_network_address: False
is_broadcast_address: False
reverse: 1.1.168.192.in-addr.arpa
cidr_notation: 192.168.1.1/24
cisco_notation: 192.168.1.1 255.255.255.0
ubuntu_subnet: 192.168.1.0/24
=============================================
```

### ビルド方法

付属のビルドスクリプトを使用してsnapパッケージを作成できます：

```bash
./build.sh
```

このスクリプトは以下の処理を行います：
1. `ipaddress_calculator/ipfx.py`から実行可能ファイルを作成
2. snapcraftを使用してsnapパッケージをビルド
3. インストール手順を表示

### ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご確認ください。
