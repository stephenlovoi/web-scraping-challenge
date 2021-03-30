from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


#setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    #creating dictionary
    data = {}

    results = soup.find_all('div', class_="content_title")
    title = []

    for result in results:
        if (result.a):
            if (result.a.text):
                title.append(result)

    #add title to dict
    data["title"] = title

    paragraphs = soup.find_all('div', class_="rollover_description_inner")
    paragraphs

    pgraph = []
    for x in range(6):
        news = paragraphs[x].text
        pgraph.append(news)

    data["paragraph"] = pgraph

    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars1.jpg"
    browser.visit(featured_image_url)

    facts_url = "https://space-facts.com/mars/"
    response_2 = requests.get(facts_url)
    soup_2 = bs(response_2.text, 'html.parser')

    facts_table = pd.read_html(facts_url)
    mars_facts_df = facts_table[0]
    mars_facts_df


    mars_facts_html = mars_facts_df.to_html()

    mars_facts_html.replace('\n', '')

    mars_facts_df.to_html('mars_facts.html')

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)


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

    data["images_list"] = images_list

    hemisphere_url = []

    valles = {"title": image_title[3], "img_url": images_list[3]}
    cerberus = {"title": image_title[0], "img_url": images_list[0]}
    schiaparelli = {"title": image_title[1], "img_url": images_list[1]}
    syrtis = {"title": image_title[2], "img_url": images_list[2]}

    hemisphere_url = [valles, cerberus, schiaparelli, syrtis]

    return data

if __name__ == "__main__":
    scrape()




