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

from typing import Optional, Type, Union, List, Sequence
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from pydantic import BaseModel
from langchain_core.messages import ToolMessage  
from langchain_core.tools import BaseTool  
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception as e:  # pragma: no cover
    # Defer hard failure until generate(); allows diagnosing import issues cleanly.
    ChatGoogleGenerativeAI = None  # type: ignore
    _IMPORT_ERROR = e


DEFAULT_SYSTEM = "You are a helpful, concise assistant."

# Pre-load environment so __main__ check sees variables even before AI() instantiation.
def _load_env():
    found = find_dotenv(usecwd=True)
    if found:
        load_dotenv(found)
    local_env = Path(__file__).parent / ".env"
    if local_env.exists():
        load_dotenv(local_env)

_load_env()


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
        model: str = "gemini-2.5-pro",
        temperature: float = 0.0,
        max_retries: int = 2,
    ) -> None:
        # Already loaded globally; allow explicit reload for updated values if needed.
        _load_env()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Allow construction; raise only when used.
            self._missing_key = True
        else:
            self._missing_key = False
        if ChatGoogleGenerativeAI is None:
            self.llm = None  # type: ignore
        else:
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
        if ChatGoogleGenerativeAI is None:
            raise RuntimeError(f"langchain_google_genai import failed: {_IMPORT_ERROR}")
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
    
    def generate_with_tools(
        self,
        *,
        prompt: str,
        input_text: str,
        tools: Sequence[BaseTool],
        system: Optional[str] = None,
        max_steps: int = 3,
    ) -> str:
        """
        Let Gemini call LangChain tools (function-calling) and return the final text.
        """
        if ChatGoogleGenerativeAI is None:
            raise RuntimeError(f"langchain_google_genai import failed: {_IMPORT_ERROR}")
        if getattr(self, "_missing_key", False):
            raise RuntimeError("GEMINI_API_KEY is not set in environment.")

        sys_msg = system or DEFAULT_SYSTEM
        human_content = f"{prompt}\n\nInput:\n{input_text}".strip()
        messages: List = [("system", sys_msg), ("human", human_content)]

        # Bind tools so Gemini can emit tool_calls
        llm_with_tools = self.llm.bind_tools(list(tools))

        for _ in range(max_steps):
            ai_msg = llm_with_tools.invoke(messages)
            messages.append(ai_msg)

            # If the model didn’t request any tools, we’re done
            tool_calls = getattr(ai_msg, "tool_calls", None) or []
            if not tool_calls:
                # Return whatever the model said
                return getattr(ai_msg, "content", "")

            # Execute tool calls and append ToolMessages
            for tc in tool_calls:
                name = tc.get("name")
                args = tc.get("args", {})
                call_id = tc.get("id")

                tool = next((t for t in tools if t.name == name), None)
                if tool is None:
                    # If Gemini called an unknown tool, tell it
                    messages.append(
                        ToolMessage(
                            content=f"Tool '{name}' is unavailable.",
                            name=name or "unknown_tool",
                            tool_call_id=call_id,
                        )
                    )
                    continue

                try:
                    result = tool.invoke(args)
                except Exception as e:
                    result = {"error": str(e)}

                messages.append(
                    ToolMessage(
                        content=str(result),
                        name=tool.name,
                        tool_call_id=call_id,
                    )
                )

        # Safety fallback if we hit max_steps without a final answer
        return "Tool loop ended without a final answer."

    def generate_structured_with_tools(
        self,
        *,
        prompt: str,
        input_text: str,
        tools: Sequence[BaseTool],
        output_model: Type[BaseModel],
        system: Optional[str] = None,
        max_steps: int = 3,
    ) -> BaseModel:
        """
        Same as generate_with_tools, but returns a structured Pydantic model.
        Strategy: run the tool-calling loop, then ask for the structured object.
        """
        if ChatGoogleGenerativeAI is None:
            raise RuntimeError(f"langchain_google_genai import failed: {_IMPORT_ERROR}")
        if getattr(self, "_missing_key", False):
            raise RuntimeError("GEMINI_API_KEY is not set in environment.")

        sys_msg = system or DEFAULT_SYSTEM
        human_content = f"{prompt}\n\nInput:\n{input_text}".strip()
        messages: List = [("system", sys_msg), ("human", human_content)]

        llm_with_tools = self.llm.bind_tools(list(tools))

        for _ in range(max_steps):
            ai_msg = llm_with_tools.invoke(messages)
            messages.append(ai_msg)

            tool_calls = getattr(ai_msg, "tool_calls", None) or []
            if not tool_calls:
                # No more tool calls; move to structured finalization
                break

            for tc in tool_calls:
                name = tc.get("name")
                args = tc.get("args", {})
                call_id = tc.get("id")

                tool = next((t for t in tools if t.name == name), None)
                if tool is None:
                    messages.append(
                        ToolMessage(
                            content=f"Tool '{name}' is unavailable.",
                            name=name or "unknown_tool",
                            tool_call_id=call_id,
                        )
                    )
                    continue

                try:
                    result = tool.invoke(args)
                except Exception as e:
                    result = {"error": str(e)}

                messages.append(
                    ToolMessage(
                        content=str(result),
                        name=tool.name,
                        tool_call_id=call_id,
                    )
                )

        # Ask for the final structured object, given the full transcript
        structured_llm = self.llm.with_structured_output(output_model)
        final_msg = structured_llm.invoke(messages + [("human", "Return ONLY the structured object.")])
        return final_msg
