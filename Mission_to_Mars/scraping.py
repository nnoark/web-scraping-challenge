from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title, para = news(browser)
    hemisphere_image_urls = mars_hemispheres(browser)

    data = {
        'title': title,
        'para' : para,
        'featured_image': featured_image(browser),
        'mars_facts': mars_facts(),
        'hemispheres': hemisphere_image_urls,
        'last_update': dt.datetime.now()
        }
    browser.quit()

    return data

def news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html,'html.parser')
    
    try:
        element = soup.select_one('div.list_text')
        title = element.find('div',class_='content_title').get_text()
        para = element.find('div',class_='article_teaser_body').get_text()

    except AttributeError:
        return None,None
    
    return title, para

def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    image_soup = bs(html, 'html.parser')

    try:
        path = image_soup.find('img',class_='headerimage fade-in').get('src')
    
    except AttributeError:
        return None
    
    featured_image_url = f'https://spaceimages-mars.com/{path}'
    return featured_image_url

def mars_facts():
    try:
        mars_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None
    
    mars_df = mars_df.rename(columns={0:'Description',1:'Mars',2:'Earth'})
    mars_df = mars_df.set_index('Description')
    mars_df = mars_df.drop(index='Mars - Earth Comparison')

    return mars_df.to_html()

def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    for i in range(4):
        browser.links.find_by_partial_text('Hemisphere')[i].click()
        html = browser.html
        hemisphere_soup = bs(html,'html.parser')
        image_title = hemisphere_soup.find('h2', class_='title').get_text()
        image_url = hemisphere_soup.find('li').a.get('href')
        hemispheres = {}
        hemispheres['image_url'] = f'https://marshemispheres.com/{image_url}'
        hemispheres['title'] = image_title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape())




