# PDF質問応答アプリ

PDFファイルをアップロードして、その内容に基づいて質問に回答するGradioアプリです。

## セットアップ

1. 依存関係のインストール
```sh
$ uv sync
```

2. OpenAI APIキーの設定
```sh
# .envファイルを作成
$ cp .env.example .env

# .envファイルを編集してOpenAI APIキーを設定
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

1. アプリケーションの起動
```sh
$ uv run main.py

# 下記のURLにてローカルサーバーが起動する
http://127.0.0.1:7860/
```

2. PDFファイルをアップロード
3. PDF内容について質問をチャットで入力
4. AIが回答を生成

## 開発

### Lintチェック
```sh
$ uv run ruff check
```

### テスト実行
```sh
$ uv run pytest
```

## 技術仕様

- **フレームワーク**: Gradio 5.45.0
- **PDF処理**: PyMuPDF (fitz)
- **AI**: OpenAI GPT-3.5-turbo
- **環境変数管理**: python-dotenv

## 注意事項

- OpenAI APIキーが必要です
- 大きなPDFファイルは処理に時間がかかる場合があります
- API使用料金にご注意ください
