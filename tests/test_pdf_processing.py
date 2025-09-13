from unittest.mock import Mock, patch
import os
from main import extract_pdf_text, chat_with_pdf


def test_extract_pdf_text_no_file():
    result = extract_pdf_text(None)
    assert result == "PDFファイルがアップロードされていません。"


@patch('main.fitz.open')
def test_extract_pdf_text_success(mock_fitz_open):
    mock_doc = Mock()
    mock_page = Mock()
    mock_page.get_text.return_value = "テストPDFの内容"
    mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
    mock_doc.close = Mock()
    mock_fitz_open.return_value = mock_doc
    
    mock_file = Mock()
    mock_file.name = "test.pdf"
    
    result = extract_pdf_text(mock_file)
    assert "PDFファイルが正常に処理されました" in result
    assert "9文字のテキストが抽出されました" in result


@patch('main.fitz.open')
def test_extract_pdf_text_error(mock_fitz_open):
    mock_fitz_open.side_effect = Exception("PDFエラー")
    
    mock_file = Mock()
    mock_file.name = "test.pdf"
    
    result = extract_pdf_text(mock_file)
    assert "PDFの処理中にエラーが発生しました" in result


def test_chat_with_pdf_no_content():
    global pdf_content
    import main
    main.pdf_content = ""
    
    result = chat_with_pdf("テスト質問", [])
    assert result == "まずPDFファイルをアップロードしてください。"


@patch.dict(os.environ, {}, clear=True)
def test_chat_with_pdf_no_api_key():
    import main
    main.pdf_content = "テストPDF内容"
    
    result = chat_with_pdf("テスト質問", [])
    assert "OpenAI APIキーが設定されていません" in result


@patch('main.get_openai_client')
@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
def test_chat_with_pdf_success(mock_get_client):
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "テスト回答"
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    import main
    main.pdf_content = "テストPDF内容"
    
    result = chat_with_pdf("テスト質問", [])
    assert result == "テスト回答"


@patch('main.get_openai_client')
@patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
def test_chat_with_pdf_api_error(mock_get_client):
    mock_get_client.side_effect = Exception("API エラー")
    
    import main
    main.pdf_content = "テストPDF内容"
    
    result = chat_with_pdf("テスト質問", [])
    assert "回答生成中にエラーが発生しました" in result
