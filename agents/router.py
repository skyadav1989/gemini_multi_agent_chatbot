from utils.gemini import gemini_llm

def route_query(query: str) -> str:
    prompt = f"""
    Decide agent:
    FAQ → policy, return, shipping
    PRODUCT → price, product, search

    Query: {query}
    Reply only FAQ or PRODUCT
    """
    return gemini_llm(prompt).strip().upper()
