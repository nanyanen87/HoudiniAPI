# HOUDINI API Server

このリポジトリは、3Dファイルを処理し、プロンプトに基づいて応答するAPIサーバーを提供します。

## 概要

このAPIは、特定のプロンプトと3Dファイルを受け取り、その内容を処理します。

## 必要条件

- Python 3.11.7
- pip
- Git

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

### 2. 仮想環境の作成と有効化

Windowsの場合:

```bash
localenv\Scripts\activate
```

Linux/macOSの場合:

未実装

### 3. 依存関係のインストール

以下のコマンドを実行して、必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

gitに上げたくないものは`.env`ファイルに記述してください。
それ以外は`config.py`に記述してください。

```plaintext
API_KEY=your_api_key
OTHER_PARAM=your_other_param
```

### 5. サーバーの起動

`main.py`を実行してAPIサーバーを起動します。
`/start_hars`にアクセスするとHARSが起動します。

```bash
python main.py
curl http://localhost:3000/start_hars
```

## APIの使用方法

このAPIは、プロンプトと3Dファイルを受け取ります。リクエストは以下の形式で行ってください。

### リクエスト形式

- **エンドポイント**: `/api/your_endpoint`
- **メソッド**: `POST`
- **ボディ**:
    - `prompt`: 実行するプロンプト（文字列）
    - `file`: 3Dファイル（ファイル形式に応じた形式でアップロード）

### サンプルリクエスト

```bash
curl -X POST http://localhost:5000/api/your_endpoint \
-H "Content-Type: multipart/form-data" \
-F "prompt=Your prompt text" \
-F "file=@path_to_your_3d_file"
```

## ライセンス

