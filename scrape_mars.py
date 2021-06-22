from bs4 import BeautifulSoup as bs
import datetime as dt
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    title, paragraph = mars_news(browser)

    data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
        }

    browser.quit()
    return data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = bs(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        title = slide_elem.find('div', class_="content_title").get_text()
        paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return title, paragraph

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = bs(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    facts_url = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    facts = mars_df.to_html()
    return facts

def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url + 'index.html')

    next_page_url = []
    image_title = []
    base_url = 'https://astrogeology.usgs.gov'


    html = browser.html
    soup = bs(html, 'html.parser')
    results_3 = soup.find_all('div', class_='description')

    number = 0
    for result in results_3:
        href=result.find('a')['href']
        img_title = result.a.find('h3')
        img_title_text = img_title.text
        image_title.append(img_title_text)
        next_page = base_url + href
        next_page_url.append(next_page)
        number = number+1
    
    images_list = []

    for x in next_page_url:
        browser.visit(x)
        html = browser.html
        img_soup = bs(html, 'html.parser')
        image = img_soup.find('img', class_='wide-image')['src']
        hem_image = base_url = image
        images_list.append(hem_image)

    hemisphere_url = []

    valles = {"title": image_title[3], "img_url": images_list[3]}
    cerberus = {"title": image_title[0], "img_url": images_list[0]}
    schiaparelli = {"title": image_title[1], "img_url": images_list[1]}
    syrtis = {"title": image_title[2], "img_url": images_list[2]}

    hemisphere_image_urls = [valles, cerberus, schiaparelli, syrtis]

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    hemi_soup = bs(html_text, "html.parser")

    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres


if __name__ == "__main__":
    scrape_info()




