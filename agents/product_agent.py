import requests, os
from utils.gemini import gemini_llm
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)


MAGENTO_URL = os.getenv("MAGENTO_GRAPHQL_URL")

def product_agent(query: str) -> str:
    q = {
        "query": '''
        query ($search: String!) {
          products(search: $search, pageSize: 5) {
            items {
              name
              sku
              url_key
              url_suffix

              description {
                html
              }

              price_range {
                minimum_price {
                  final_price {
                    value
                    currency
                  }
                }
              }
            }
          }
        }
        ''',
        "variables": {"search": query}
    }
    r = requests.post(MAGENTO_URL, json=q).json()
    items = r.get("data", {}).get("products", {}).get("items", [])
    return gemini_llm(str(items))
