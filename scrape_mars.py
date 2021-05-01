from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    
##### Using Beautiful Soup to Scrape Latest Headline and Paragraph ####
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the content titles
    content_titles = soup.find_all('div', class_='content_title')
    # Get the first content title
    news_title = content_titles[1].text
    
    
    #Get the content paragraphs
    content_paragraphs = soup.find_all('div', class_='article_teaser_body')
    # Get the first paragraph
    news_p = content_paragraphs[0].text

    
    
#### Using Splinter To Get Featured Image ####
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    
    browser.click_link_by_partial_text('FULL IMAGE')  
    
    featured_img_url =  browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')["src"]
 
    
    
    
#### Using Pandas to scrape table ####

    data = pd.read_html("https://space-facts.com/mars/")
    
    #Print how many tables were pulled
    #print(len(data))
    
    facts_html_str = data[0].to_html(index = False)

                        
        
    hemisphere_image_urls = []
#### Using Splinter To Get 4 Images ####
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    image_hrefs_list = []
    for x in range(4):
        x = x + 1
        href_var = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div['+str(x)+']/a')["href"]
        image_hrefs_list.append(href_var)
        
    for href in image_hrefs_list:
        browser.visit(href)
        time.sleep(1)

        hemi_name= browser.find_by_xpath('//*[@id="splashy"]/div[1]/div[1]/div[3]/section/h2[1]').text

       
        browser.click_link_by_partial_text('Open') 
        wide_image =  browser.find_by_xpath('//*[@id="wide-image"]/img')["src"]
      
        
        hemisphere_image_urls.append({'title':hemi_name, 'img_url':wide_image})
        


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_img_url,
        "facts_html_str": facts_html_str,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    
    # Close the browser after scraping
    browser.quit()

    return mars_data


 
