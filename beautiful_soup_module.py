from bs4 import BeautifulSoup
import requests

def scrape_artwork(artname):
    url = f'https://www.memeraki.com/collections/{artname}?sort_by=best-selling'
    if(artname=="pichwai"): url='https://www.memeraki.com/collections/pichwai?sort_by=best-selling?filter.p.product_type=All+decor+plates&filter.p.product_type=Art+Supplies&filter.p.product_type=Handpainted+Artwork&filter.p.product_type=Home+Decor&filter.v.price.gte=&filter.v.price.lte='
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    ol_data = soup.find('ol', id='main-collection-product-grid')
    if not ol_data:
        return []
    li_items = ol_data.find_all('li')[:10]
    data = []
    for item in li_items:
        product_name = item.get('data-alpha')
        size = "N/A"
        details_div = item.find('div', style=lambda val: val and 'justify-content: space-between' in val)
        if details_div:
            p_tags = details_div.find_all('p')
            if len(p_tags) >= 2:
                size = p_tags[1].get_text(strip=True)
        price_tag = item.find('dl', class_='price__regular')
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
        data.append({
            'Product Name': product_name,
            'Size': size,
            'Price': price
        })
    return data
