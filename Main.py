import requests
from bs4 import BeautifulSoup

# --- Step 1: Fetch the HTML Content ---
# The URL of the news website we want to scrape.
URL = "https://www.bbc.com/news"

# Headers to mimic a browser visit. Some websites block scripts,
# so a User-Agent can help make the request look like it's from a real user.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching news from: {URL}")

try:
    # Send a GET request to the website.
    response = requests.get(URL, headers=HEADERS)
    # This will raise an exception if the request returned an error status code (like 404 or 500).
    response.raise_for_status()

    # --- Step 2: Parse the HTML ---
    # Create a BeautifulSoup object to parse the page's HTML.
    soup = BeautifulSoup(response.content, 'html.parser')

    # --- Step 3: Find and Extract Headlines ---
    # Find all HTML elements that contain the headlines.
    # On BBC News, headlines are often in <h2> tags.
    # Note: This might change. You may need to inspect the website's source code
    # in your browser (right-click -> Inspect) to find the correct tags.
    headline_tags = soup.find_all('h2')

    # Create an empty list to store the extracted headlines.
    headlines = []
    for tag in headline_tags:
        # Get the text content from the tag and remove extra whitespace.
        headline_text = tag.get_text(strip=True)
        # Add the cleaned-up headline to our list.
        if headline_text: # Ensure we don't add empty strings
            headlines.append(headline_text)

    # --- Step 4: Save Headlines to a .txt File ---
    # Check if we actually found any headlines.
    if headlines:
        # Open 'headlines.txt' in write mode ('w'). 'utf-8' encoding is used
        # to handle special characters correctly.
        with open('headlines.txt', 'w', encoding='utf-8') as file:
            print(f"Found {len(headlines)} headlines. Saving to headlines.txt...")
            # Write each headline to the file on a new line.
            for headline in headlines:
                file.write(headline + '\n')
        print("✅ Success! Headlines have been saved to headlines.txt.")
    else:
        print("⚠️ Could not find any headlines. The website's structure may have changed.")

except requests.exceptions.RequestException as e:
    print(f"❌ Error: Could not connect to the website. Please check your internet connection. Details: {e}")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
