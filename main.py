import gradio as gr
import fitz
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None
pdf_content = ""


def get_openai_client():
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。")
        client = OpenAI(api_key=api_key)
    return client


def extract_pdf_text(pdf_file):
    global pdf_content
    if pdf_file is None:
        return "PDFファイルがアップロードされていません。"
    
    try:
        doc = fitz.open(pdf_file.name)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        pdf_content = text
        return f"PDFファイルが正常に処理されました。{len(text)}文字のテキストが抽出されました。"
    except Exception as e:
        return f"PDFの処理中にエラーが発生しました: {str(e)}"


def chat_with_pdf(message, history):
    global pdf_content
    
    if not pdf_content:
        return "まずPDFファイルをアップロードしてください。"
    
    if not os.getenv("OPENAI_API_KEY"):
        return "OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。"
    
    try:
        prompt = f"""
以下のPDFの内容に基づいて質問に回答してください。

PDF内容:
{pdf_content[:4000]}

質問: {message}

回答は日本語で、PDF内容に基づいて正確に答えてください。PDF内容に関連しない質問の場合は、その旨を伝えてください。
"""
        
        openai_client = get_openai_client()
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"回答生成中にエラーが発生しました: {str(e)}"


def main():
    with gr.Blocks(title="PDF質問応答アプリ") as demo:
        gr.Markdown("# PDF質問応答アプリ")
        gr.Markdown("PDFファイルをアップロードして、その内容について質問してください。")
        
        with gr.Row():
            pdf_upload = gr.File(
                label="PDFファイルをアップロード",
                file_types=[".pdf"],
                type="filepath"
            )
            upload_status = gr.Textbox(
                label="アップロード状況",
                interactive=False,
                lines=2
            )
        
        pdf_upload.change(
            fn=extract_pdf_text,
            inputs=pdf_upload,
            outputs=upload_status
        )
        
        gr.Markdown("## チャット")
        gr.ChatInterface(
            fn=chat_with_pdf,
            type="messages",
            title="PDFについて質問してください"
        )
    
    demo.launch()


if __name__ == "__main__":
    main()
