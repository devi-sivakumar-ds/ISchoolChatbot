import requests
import time
import os
import urllib.robotparser
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Function to get the domain from a URL
def get_domain(url):
    return urlparse(url).netloc

# Function to save content as a text file
def save_as_text(content, filename, folder="data/raw_text"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to check robots.txt for webcrawling compliance
def check_robots_txt(url, user_agent='MyWebCrawler'):
    domain = urlparse(url).netloc
    robots_url = f'http://{domain}/robots.txt'
    
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    
    # Check if we're allowed to crawl the URL
    is_allowed = rp.can_fetch(user_agent, url)
    crawl_delay = rp.crawl_delay(user_agent)
    return is_allowed, crawl_delay

# Function to scrape and crawl links 
def crawl_and_scrape(start_url, base_url, scraped_urls, user_agent='MyWebCrawler'):
    
    if start_url in scraped_urls:   # To avoid re-scraping the same URL
        return

    # Checking robots.txt for permissions and crawl delay
    is_allowed, crawl_delay = check_robots_txt(start_url, user_agent)
    
    if not is_allowed:
        print(f"Access to {start_url} is disallowed by robots.txt.")
        return
    
    print(f"Scraping: {start_url}")
    try:
        response = requests.get(start_url, headers={"User-Agent": user_agent})
        response.raise_for_status()

        # Saving the content as text
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text(strip=True)
        
        # Saving in the raw_text folder
        page_name = urlparse(start_url).path.replace('/', '_').strip('_') or 'index'
        save_as_text(content, f"{page_name}.txt", folder="data/raw_text")

        scraped_urls.add(start_url)

        # Respecting crawl delay, if specified
        if crawl_delay:
            print(f"Respecting crawl delay of {crawl_delay} seconds.")
            time.sleep(crawl_delay)
        
        # Finding all internal links to crawl
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            full_url = urljoin(start_url, href)
            
            # Checking if the link is part of the same domain and not already scraped
            if full_url.startswith(start_url) and full_url not in scraped_urls:
                crawl_and_scrape(full_url, base_url, scraped_urls, user_agent)

    except requests.RequestException as e:
        print(f"Failed to retrieve {start_url}: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    start_url = 'https://www.ischool.berkeley.edu/programs/mims/admissions'
    base_url = get_domain(start_url)
    scraped_urls = set()  # To track the URLs we've already scraped
    user_agent = 'MyWebCrawler'  # Defining the user-agent

    crawl_and_scrape(start_url, base_url, scraped_urls, user_agent)
    print("Crawling complete! All data saved in 'data/raw_text/'")

if __name__ == '__main__':
    main()
