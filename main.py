from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time



def roll_down(driver):
   
    script = """
        var d = document.documentElement;
        window.scrollTo(0, document.body.scrollHeight); 
        var offset = d.scrollTop + window.innerHeight;
        return offset;
        """
        

    prev = -1
    page = 0
    max_no = 50 #extracting content from 50 pages
    while (True and (page != max_no)):
        curr = driver.execute_script(script)
        if prev == curr:
                break
        time.sleep(2)
        prev = curr
        page+=1
        
    return driver, page

def extract_page(url, driver):

    #opening URL
    driver.get(url)

    #scrolling down the page to open all the pages
    driver, pages = roll_down(driver)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, 'lxml')
    #driver.quit()
    return soup, pages

def make_csv(data):
    import csv

    with open('dataset.csv','w') as file:
        fileWriter = csv.writer(file)
        for row in data:
            fileWriter.writerow(row)

def login(url):
    username = input("Enter Username : ")
    password = input("Enter Password : ")

    login_url = 'http://allpoetry.com/login'

    driver = webdriver.Chrome("/Users/Aditya/Desktop/Poem Classification/chromedriver")
    driver.get(login_url)

    username = driver.find_element_by_id('user_name')
    username.send_keys(username)

    password = driver.find_element_by_id('user_password')
    password.send_keys(password)


    signInButton = driver.find_element_by_xpath('//*[@id="new_user"]/div[4]/div[2]/input')
    signInButton.click()

    return driver


def main():
    links = []
    titles = []
    types = []

    
    base_url = 'http://allpoetry.com/poems/about/'
    login_url = 'http://allpoetry.com/login'
    base_link_url = 'http://allpoetry.com/'
    categories = ['Nature','Love','Humor','Spiritual']
    
    driver = login(login_url) #automating the login so that we can access pages after 15 
    
    for category in categories:
        url = base_url + category
        soup, pages = extract_page(url, driver)
        
        div1 = soup.find("div", attrs = {'class':"items_group inf", 'data-p':str(1)})
        a_tags = div1.findAll('a', attrs = {'class':"nocolor fn"})
        for eachLink in a_tags:
            links.append(base_link_url + eachLink['href'] )
            titles.append(eachLink.text)
            types.append(category)
            
        for page in range(pages-2):
            div = div1.find("div", attrs = {'class':"items_group", 'data-p':str(page+2)})
            a_tags = div.findAll('a', class_='nocolor fn')
            for eachLink in a_tags:
                links.append(base_link_url + eachLink['href'])
                titles.append(eachLink.text)
                types.append(category)


    data = list(zip(titles, links, types))
    make_csv(data)
    return titles, links,types


if __name__ == "__main__":
    main()


