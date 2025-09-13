import gradio as gr
import random


def random_response(message, history):
    return random.choice(["Yes", "No"])


def main():
    gr.ChatInterface(fn=random_response, type="messages").launch()


if __name__ == "__main__":
    main()
