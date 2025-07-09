from beautiful_soup_module import scrape_artwork
from openai_module import generate_content
from openai_top_module import generate_content_top

if __name__ == "__main__":
    artnames=['madhubani','kalamkari','pichwai','gond-art','kalighat','bengal-pattachitra','miniature-paintings','mata-ni-pachedi','warli-paintings','blue-pottery','phad','kerala-mural','tanjore','lippan-kaam']
    print("Available choices:\n")
    for art in artnames:
        print(art)
    artname = input("Enter the artwork name (e.g., madhubani, kalamkari, etc.): ").strip()
    print(f"Scraping data for: {artname}")
    art_data = scrape_artwork(artname)
    if not art_data:
        print(f"No data found for {artname}.")
    else:
        try:
            result = generate_content(art_data)
            print("\n Generated Content for table:")
            print(result)
        except Exception as e:
            print(f"Error generating OpenAI content: {e}")
        
        try:
            result = generate_content_top(art_data,artname)
            print("\n Generated Content for top-selling:")
            print(result)
        except Exception as e:
            print(f"Error generating OpenAI content: {e}")

