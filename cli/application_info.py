from ai import AI
from models.llm_models import ApplicationIntel
from tools.web_tool import search_scrape_tool
def get_application_info(input_text: str) -> ApplicationIntel:
    """Retrieve application information using the AI module."""
    ai = AI()
    prompt = (
        "Provide structured information about the product"
        "including its name, vendor name, and a brief description."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=input_text,
        tools=[search_scrape_tool],
        output_model=ApplicationIntel,
        max_steps=2
    )
    return result

