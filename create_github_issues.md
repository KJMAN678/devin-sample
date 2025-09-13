# GitHub Issues to Create

## Issue 1: PDF処理ライブラリの選定と実装

**Title:** PDF処理ライブラリの選定と実装 (PyMuPDF採用)

**Labels:** enhancement, documentation

**Body:**
## 概要
PDFアップロード機能のためのPDF処理ライブラリを選定し、実装しました。

## 採用技術: PyMuPDF (fitz)

### 選択理由
- ✅ 高速で信頼性が高い
- ✅ 日本語PDFに対応
- ✅ テキスト抽出精度が高い
- ✅ Pythonでの統合が容易
- ✅ メモリ効率が良い

### 代替案との比較
| ライブラリ | 速度 | 精度 | 日本語対応 | メモリ効率 |
|-----------|------|------|-----------|-----------|
| PyMuPDF | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| pdfplumber | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| PyPDF2 | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ |

### 実装詳細
```python
import fitz  # PyMuPDF

def extract_pdf_text(pdf_file):
    doc = fitz.open(pdf_file.name)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
```

### 依存関係
```toml
dependencies = [
    "pymupdf>=1.23.0",
]
```

---

## Issue 2: AI質問応答サービスの選定と実装

**Title:** AI質問応答サービスの選定と実装 (OpenAI API採用)

**Labels:** enhancement, ai, documentation

**Body:**
## 概要
PDF内容に基づく質問応答機能のためのAIサービスを選定し、実装しました。

## 採用技術: OpenAI API (GPT-3.5-turbo)

### 選択理由
- ✅ 高精度な自然言語理解
- ✅ 日本語での質問応答に優れた性能
- ✅ PDFテキストを含むコンテキスト処理が可能
- ✅ 安定したAPI提供
- ✅ Gradioとの統合が容易

### 代替案との比較
| サービス | 精度 | 日本語対応 | コスト | 可用性 |
|---------|------|-----------|-------|--------|
| OpenAI API | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Claude API | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| Hugging Face | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

### 実装詳細
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_pdf(message, pdf_content):
    prompt = f"""
    以下のPDFの内容に基づいて質問に回答してください。
    
    PDF内容: {pdf_content[:4000]}
    質問: {message}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content
```

### セキュリティ考慮
- 環境変数によるAPIキー管理
- `.env.example`ファイルでの設定ガイド
- エラーハンドリングによる情報漏洩防止

### コスト分析
- 質問1回あたり: 約0.1-0.5円
- 月間1000回利用: 約100-500円
- PDF処理: 無料（ローカル処理）

---

## Issue 3: Gradio UIの拡張実装

**Title:** Gradio UIの拡張実装 (PDFアップロード + チャット統合)

**Labels:** enhancement, ui, frontend

**Body:**
## 概要
既存のシンプルなチャットボットUIを、PDFアップロード機能付きの本格的な質問応答アプリに拡張しました。

## 実装した機能

### 1. PDFアップロード機能
```python
pdf_upload = gr.File(
    label="PDFファイルをアップロード",
    file_types=[".pdf"],
    type="filepath"
)
```

### 2. アップロード状況表示
```python
upload_status = gr.Textbox(
    label="アップロード状況",
    interactive=False,
    lines=2
)
```

### 3. チャットインターフェース統合
```python
gr.ChatInterface(
    fn=chat_with_pdf,
    type="messages",
    title="PDFについて質問してください"
)
```

### UI構成
1. **ヘッダー**: アプリタイトルと説明
2. **アップロードエリア**: PDF選択とステータス表示
3. **チャットエリア**: 質問応答インターフェース

### ユーザーエクスペリエンス
- ✅ 直感的なドラッグ&ドロップ操作
- ✅ リアルタイムステータス更新
- ✅ エラーメッセージの適切な表示
- ✅ 日本語での自然な対話

### エラーハンドリング
- PDFアップロード前の質問への適切な応答
- ファイル形式エラーの検出
- API呼び出しエラーの処理

---

## Issue 4: テストスイートの実装

**Title:** 包括的なテストスイートの実装

**Labels:** testing, quality-assurance

**Body:**
## 概要
PDF処理と質問応答機能の品質保証のため、包括的なテストスイートを実装しました。

## テスト構成

### 1. PDF処理テスト
```python
def test_extract_pdf_text_success():
    # PyMuPDFのモックを使用したテスト
    
def test_extract_pdf_text_error():
    # エラーハンドリングのテスト
```

### 2. 質問応答テスト
```python
def test_chat_with_pdf_success():
    # OpenAI APIのモックを使用したテスト
    
def test_chat_with_pdf_api_error():
    # API呼び出しエラーのテスト
```

### 3. エラーハンドリングテスト
- PDFアップロード前の質問
- APIキー未設定時の処理
- ファイル処理エラー

### テスト結果
```
============== test session starts ==============
collected 8 items

tests/test_pdf_processing.py .......     [ 87%]
tests/test_sample.py .                   [100%]

============== 8 passed in 1.84s ===============
```

### 品質保証
- ✅ 全テストケース通過
- ✅ Lintチェック通過
- ✅ 型安全性の確保
- ✅ モックを使用した外部依存の分離

---

## Issue 5: 環境設定とデプロイメント

**Title:** 環境設定とデプロイメント手順の整備

**Labels:** documentation, deployment, setup

**Body:**
## 概要
アプリケーションの環境設定、依存関係管理、デプロイメント手順を整備しました。

## 依存関係管理

### pyproject.toml更新
```toml
dependencies = [
    "gradio==5.45.0",
    "ruff==0.13.0",
    "pytest==8.4.2",
    "pymupdf>=1.23.0",      # PDF処理
    "openai>=1.0.0",        # OpenAI API
    "python-dotenv>=1.0.0", # 環境変数管理
]
```

## 環境変数設定

### .env.example
```bash
# OpenAI API Key
# https://platform.openai.com/api-keys から取得してください
OPENAI_API_KEY=your_openai_api_key_here
```

## セットアップ手順

### 1. 依存関係のインストール
```bash
uv sync
```

### 2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルにOpenAI APIキーを設定
```

### 3. アプリケーションの起動
```bash
uv run main.py
```

### 4. アクセス
http://127.0.0.1:7860/

## 検証コマンド
```bash
# Lintチェック
uv run ruff check

# テスト実行
uv run pytest

# アプリケーション起動
uv run main.py
```

## 今後の拡張計画
- [ ] 複数PDFファイルの同時処理
- [ ] PDF内容の永続化
- [ ] ベクトル検索機能
- [ ] 画像PDFのOCR処理
- [ ] Docker化
- [ ] クラウドデプロイメント

## セキュリティ考慮事項
- APIキーの環境変数管理
- ファイルアップロードの制限
- エラー情報の適切な処理
- HTTPS通信の推奨
