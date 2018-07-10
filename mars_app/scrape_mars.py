
def scrape_mars():
    from bs4 import BeautifulSoup
    import pandas as pd
    from selenium import webdriver
    import time
    import os

    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.binary_location = '.apt/usr/bin/google-chrome-stable'
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('headless')
    
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    print('browser is ready')


    # scraping news
    url = 'https://mars.nasa.gov/news/'
    browser.get(url)
    time.sleep(3)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title')\
    .find('a').get_text()

    news_p = soup.find('ul', class_='item_list ').find('li', class_='slide')\
    .find('div', class_='article_teaser_body').get_text()

    print(news_title)

    # scraping weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.get(url)
    time.sleep(3)

    tweet_features = 'Sol' and 'high' and 'low' and 'pressure' and 'hPa' and 'daylight'
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for tweet in soup.find_all('li', class_="js-stream-item stream-item stream-item "):
        if tweet_features in tweet.find('div', class_='js-tweet-text-container').find('p').text:
            mars_weather = tweet.find('div', class_='js-tweet-text-container').find('p').text
            break
    
    print(mars_weather)

    # scraping featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(url)
    time.sleep(3)

    browser.find_element_by_css_selector('div[class="default floating_text_area ms-layer"]').find_element_by_css_selector('footer')\
        .find_element_by_css_selector('a[class="button fancybox"]').click()
    time.sleep(3)

    browser.find_element_by_css_selector('div[id="fancybox-lock"]').find_element_by_css_selector('div[class="buttons"]')\
        .find_element_by_css_selector('a[class="button"]').click()

    featured_image_url = browser.find_element_by_css_selector('div[id="page"]').find_element_by_css_selector('section[class="content_page module"]')\
        .find_element_by_css_selector('figure[class="lede"]').find_element_by_tag_name('a').get_attribute('href')
   
    print(featured_image_url)


    #scraping facts
    url = 'http://space-facts.com/mars/'

    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Description', 'Value']
    df = df.set_index('Description')

    facts_table = df.to_html()
    # print(facts_table)

    #scraping hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.get(url)
    time.sleep(3)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    spheres = soup.find('div', class_='collapsible results').find_all('div', class_='item')

    hemisphere_image_urls = []

    for x in range(len(spheres)):
        title = spheres[x].find('div', class_="description").find('h3').text

        browser.find_element_by_css_selector('div[class="collapsible results"]').find_elements_by_css_selector('div[class="item"]')[x]\
        .find_element_by_css_selector('div[class="description"]').find_element_by_css_selector('a').click()

        img_url = browser.find_element_by_class_name('downloads').find_element_by_css_selector('a').get_attribute('href')
        browser.execute_script("window.history.go(-1)")

        dic = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(dic)
        
        time.sleep(3)
        
    # print(hemisphere_image_urls)

    scrape_dic = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'weather': mars_weather,
        'image': featured_image_url,
        'facts_table': facts_table,
        'hemispheres': hemisphere_image_urls
    }  
    print('scrape dictionary is ready')

    browser.quit()
    return scrape_dic
