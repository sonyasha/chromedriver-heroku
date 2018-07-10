

def scrape_mars():
    from bs4 import BeautifulSoup
    # from splinter import Browser
    import pandas as pd
    # from selenium import webdriver
    from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    import time
    import os

    # GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
    # CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = '/app/.apt/usr/bin/google-chrome'
    
    chrome_options.binary_location = '.apt/usr/bin/google-chrome-stable'
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('headless')
    
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    print('browser is ready')
    # chrome_driver_binary = '/app/.chromedriver/bin/chromedriver'

    # browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    

    # scraping news
    url = 'https://mars.nasa.gov/news/'
    browser.get(url)
    time.sleep(3)

    # html = browser.html
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title')\
    .find('a').get_text()

    news_p = soup.find('ul', class_='item_list ').find('li', class_='slide')\
    .find('div', class_='article_teaser_body').get_text()

    print(news_title)
    # print(news_p)

    # scraping weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.get(url)
    # browser.visit(url)
    time.sleep(3)

    tweet_features = 'Sol' and 'high' and 'low' and 'pressure' and 'hPa' and 'daylight'
    
    html = browser.page_source
    # html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    for tweet in soup.find_all('li', class_="js-stream-item stream-item stream-item "):
        if tweet_features in tweet.find('div', class_='js-tweet-text-container').find('p').text:
            mars_weather = tweet.find('div', class_='js-tweet-text-container').find('p').text
            break
    
    print(mars_weather)

    # scraping featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(url)
    browser.get(url)
    time.sleep(3)

    # browser.find_by_css('div[class="default floating_text_area ms-layer"]').find_by_css('footer')\
    # .find_by_css('a[class="button fancybox"]').click()
    browser.find_element_by_css_selector('div[class="default floating_text_area ms-layer"]').find_element_by_css_selector('footer')\
        .find_element_by_css_selector('a[class="button fancybox"]').click()
    time.sleep(3)

    # browser.find_by_css('div[id="fancybox-lock"]').find_by_css('div[class="buttons"]')\
    # .find_by_css('a[class="button"]').click()
    browser.find_element_by_css_selector('div[id="fancybox-lock"]').find_element_by_css_selector('div[class="buttons"]')\
        .find_element_by_css_selector('a[class="button"]').click()


    # featured_image_url = browser.find_by_css('div[id="page"]').find_by_css('section[class="content_page module"]')\
    # .find_by_css('figure[class="lede"]').find_by_css('a')['href']
    featured_image_url = browser.find_element_by_css_selector('div[id="page"]').find_element_by_css_selector('section[class="content_page module"]')\
        .find_element_by_css_selector('figure[class="lede"]').find_element_by_tag_name('a').get_attribute('href')
   

    print(featured_image_url)

# Due to Heroku 30 sec timeout limitation only changing data was left for scraping.
# Mars facts table and hemispheres data are static and don't change after scraping.
# The code below is working correctly

#start comment----------------------------------------------------
    # #scraping facts
    # url = 'http://space-facts.com/mars/'

    # tables = pd.read_html(url)

    # df = tables[0]
    # df.columns = ['Description', 'Value']
    # df = df.set_index('Description')

    # facts_table = df.to_html()
    # # print(facts_table)

    # #scraping hemispheres
    # url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.get(url)
    # # browser.visit(url)
    # time.sleep(3)

    # # html = browser.html
    # html = browser.page_source
    # soup = BeautifulSoup(html, 'html.parser')

    # spheres = soup.find('div', class_='collapsible results').find_all('div', class_='item')

    # hemisphere_image_urls = []

    # for x in range(len(spheres)):
    #     title = spheres[x].find('div', class_="description").find('h3').text

    #     #browser.find_by_css('div[class="collapsible results"]').find_by_css('div[class="item"]')[x]\
    #     #.find_by_css('div[class="description"]').find_by_css('a').click()
        
    #     browser.find_element_by_css_selector('div[class="collapsible results"]').find_elements_by_css_selector('div[class="item"]')[x]\
    #     .find_element_by_css_selector('div[class="description"]').find_element_by_css_selector('a').click()

    #     #for img in browser.find_by_css('div[class="downloads"]').find_by_css('a'):
    #         ## if ('Original' in img.text):
    #         ##     img_url = img['href']
    #        # if ('Sample') in img.text:
    #           #  img_url = img['href']
    #     img_url = browser.find_element_by_class_name('downloads').find_element_by_css_selector('a').get_attribute('href')
    #     browser.execute_script("window.history.go(-1)")
    #     # browser.click_link_by_partial_text('Back')

    #     dic = {'title': title, 'img_url': img_url}
    #     hemisphere_image_urls.append(dic)
        
    #     time.sleep(3)
        
    # # print(hemisphere_image_urls)
#end comment--------------------------------

    scrape_dic = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'weather': mars_weather,
        'image': featured_image_url,
        # 'facts_table': facts_table,
        # 'hemispheres': hemisphere_image_urls
        'facts_table': '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Value</th>\n    </tr>\n    <tr>\n      <th>Description</th>\n      <th></th>\n   </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n  </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n    <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>',
        'hemispheres': [
            {
            "title": "Cerberus Hemisphere Enhanced",
            "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"
            },
            {
            "title": "Schiaparelli Hemisphere Enhanced",
            "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"
            },
            {
            "title": "Syrtis Major Hemisphere Enhanced",
            "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"
            },
            {
            "title": "Valles Marineris Hemisphere Enhanced",
            "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"
            }
        ]
    }  
    print('scrape dictionary is ready')

    browser.quit()
    return scrape_dic
