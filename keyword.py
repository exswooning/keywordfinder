import requests
from bs4 import BeautifulSoup
import re

def scrape_nest_nepal():
    """
    Scrapes the Nest Nepal homepage to find products and associated keywords.
    """
    url = "https://nestnepal.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Fetching content from {url}...")

    try:
        response = requests.get(url, headers=headers)
        # Raise an exception if the request was not successful
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch the website. {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    products = {}
    keywords = set()

    # Look for common tags that might contain product names (h2, h3, strong)
    # This makes the scraper more robust than looking for a single, specific class
    potential_product_tags = soup.find_all(['h2', 'h3', 'strong'])

    # Keywords that are likely to be part of a product title on this site
    product_indicators = ['hosting', 'domain', 'server', 'vps', 'wordpress', 'google workspace', 'microsoft 365', 'zoho', 'nord vpn', 'azure']

    print("Analyzing content to find products...")

    for tag in potential_product_tags:
        title = tag.get_text(strip=True)
        
        # Check if any of our indicator words are in the title
        if any(indicator in title.lower() for indicator in product_indicators):
            # Clean up the title to be a good product name
            cleaned_title = re.sub(r'Check Plans$', '', title).strip()
            
            # Extract keywords from the title
            product_keywords = set(re.findall(r'\b\w+\b', cleaned_title.lower()))
            
            # Store the product and its keywords
            if cleaned_title not in products:
                products[cleaned_title] = product_keywords
                keywords.update(product_keywords)

    return products, sorted(list(keywords))

def main():
    """
    Main function to run the scraper and print the results.
    """
    found_products, found_keywords = scrape_nest_nepal()

    if found_products:
        print("\n--- 🕵️ Found Products and Their Keywords ---\n")
        for product, p_keywords in found_products.items():
            print(f"🔹 Product: {product}")
            print(f"   Keywords: {', '.join(sorted(list(p_keywords)))}\n")
        
        print("\n--- 🔑 All Unique Keywords Found ---\n")
        print(', '.join(found_keywords))
        print("\n------------------------------------------")
    else:
        print("\nCould not find any products. The website structure may have changed.")

if __name__ == "__main__":
    main()