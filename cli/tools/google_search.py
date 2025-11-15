from serpapi import GoogleSearch
import os

def serpapi_search(query: str, api_key: str, **kwargs):
    """
    Perform a Google search using SerpApi.

    Parameters:
        query (str): Search query text.
        api_key (str): Your SerpApi API key.
        **kwargs: Optional SerpApi parameters (location, num, etc.)

    Returns:
        dict: Parsed JSON search results.
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        **kwargs
    }

    search = GoogleSearch(params)
    results = search.get_dict()  # retrieves JSON results

    return results


if __name__ == "__main__":
    # Example usage
    MY_API_KEY = os.getenv("SERPAPI_KEY")

    if not MY_API_KEY:
        raise ValueError("SERPAPI_KEY not set!")

    response = serpapi_search(
        "1Password",
        api_key=MY_API_KEY,
        location="Austin, Texas, United States",
        num=3 #Top num results from google
    )

    # Print the top organic results
    for item in response.get("organic_results", []):
        print(f"- {item.get('title')}: {item.get('link')}")
