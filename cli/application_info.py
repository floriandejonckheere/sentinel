from ai import AI
from models.llm_models import ApplicationIntel
from tools.web_tool import search_scrape_tool
def get_application_info():
    """Retrieve application information using the AI module."""
    ai = AI()
    prompt = (
        "Provide structured information about the product"
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        tools=[search_scrape_tool],
        output_model=ApplicationIntel,
    )
    return result