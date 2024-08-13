import requests
from bs4 import BeautifulSoup
import markdown2

def get_fellows_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='full-fellow-mobile-link')
    return [f"https://www.mandelawashingtonfellowship.org{link['href']}" for link in links]

def scrape_bio(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    bio_div = soup.find('div', class_='fellow-bio')
    if bio_div:
        return bio_div.get_text(strip=True)
    return None

def main():
    base_url = "https://www.mandelawashingtonfellowship.org/fellows/"
    all_bios = []

    for page in range(1, 17):  # 16 pages in total
        url = f"{base_url}?sf_paged={page}"
        fellow_links = get_fellows_links(url)
        
        for link in fellow_links:
            bio = scrape_bio(link)
            if bio:
                fellow_name = link.split('/')[-2].replace('-', ' ').title()
                all_bios.append(f"# {fellow_name}\n\n{bio}\n\n---\n\n")

    with open('fellow_bios.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_bios))

if __name__ == "__main__":
    main()
