"""Reusable AI helper integrating LangChain Gemini with optional structured output.

Usage examples:

from pydantic import BaseModel
from ai import AI

class Translation(BaseModel):
    french: str

ai = AI()
text = ai.generate(
    prompt="Translate to French.",
    input_text="I love programming.",
)

structured = ai.generate(
    prompt="Translate to French and return only the translation.",
    input_text="I love programming.",
    output_model=Translation,
)
print(text)
print(structured.french)
"""

from typing import Optional, Type, Union, List
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI


DEFAULT_SYSTEM = "You are a helpful, concise assistant."


class AI:
    """Wrapper around ChatGoogleGenerativeAI supporting plain & structured outputs.

    Methods
    -------
    generate(prompt, input_text, output_model=None, system=None) -> Union[str, BaseModel]
        Pass a prompt and input text; optionally supply a Pydantic model type for structured output.
    """

    def __init__(
        self,
        *,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.0,
        max_retries: int = 2,
    ) -> None:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Allow construction; raise only when used.
            self._missing_key = True
        else:
            self._missing_key = False
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_tokens=None,
            timeout=None,
            max_retries=max_retries,
            api_key=api_key,
        )

    def generate(
        self,
        *,
        prompt: str,
        input_text: str,
        output_model: Optional[Type[BaseModel]] = None,
        system: Optional[str] = None,
    ) -> Union[str, BaseModel]:
        """Generate a response.

        Parameters
        ----------
        prompt: High-level instruction / task.
        input_text: User content or data to operate on.
        output_model: Optional Pydantic model class. If provided, structured output is returned.
        system: Optional system message override.
        """
        if getattr(self, "_missing_key", False):
            raise RuntimeError("GEMINI_API_KEY is not set in environment.")

        sys_msg = system or DEFAULT_SYSTEM
        # Compose a single human message including prompt & input for simplicity.
        human_content = f"{prompt}\n\nInput:\n{input_text}".strip()

        messages: List = [("system", sys_msg), ("human", human_content)]

        if output_model:
            # Structured output path using LangChain's adapter; returns model instance.
            structured_llm = self.llm.with_structured_output(output_model)
            return structured_llm.invoke(messages)

        # Plain text path
        resp = self.llm.invoke(messages)
        return resp.content


def _demo():  # pragma: no cover - manual example
    class Translation(BaseModel):
        french: str

    ai = AI()
    print("Plain text response:")
    txt = ai.generate(prompt="Translate to French.", input_text="I love programming.")
    print(txt)

    print("\nStructured response:")
    tr = ai.generate(
        prompt="Translate to French and return only the translation.",
        input_text="I love programming.",
        output_model=Translation,
    )
    print(tr.french)


if __name__ == "__main__":
    if os.environ.get("GEMINI_API_KEY"):
        _demo()
    else:
        print("GEMINI_API_KEY not set; skipping demo.")
