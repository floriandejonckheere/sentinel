import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


class AI:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

    def test(self):
        messages = [
            (
                "system",
                "You are a helpful assistant that translates English to French. Translate the user sentence.",
            ),
            ("human", "I love programming."),
        ]
        ai_msg = self.llm.invoke(messages)
        print(ai_msg.content)
