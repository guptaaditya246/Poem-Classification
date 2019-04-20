#importing libraries needed
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import time
import csv


user_agent = UserAgent()
print("Loading All URLs...\n")
data = pd.read_csv('URL_file.csv', header=None)
data.columns = ['Title','Link','Category']
data.dropna(axis=0, inplace=True)
data.reset_index(inplace=True)
print("Links Loaded!!\n")

#copying all previous data to list to properly iterate through it and write it to csv accordingly
links = list(data['Link'])
AllTitles = list(data['Title'])
categories = list(data['Category'])

#creating empty lists where our extracted content will be appended
poems = []
authors = []
category = []
titles = []

print("Getting Poems....Please Wait\n")
with open('MyDataset.csv','a',encoding="utf-8") as file:
    fileWriter = csv.writer(file)
    
    for i in range(len(links)):
        
        print(i+1, end='\n')        
        page = requests.get(url=links[i], headers={'user-agent':user_agent.chrome})
        html = page.content
        soup = BeautifulSoup(html, 'lxml')
    


        poem = []
        div = soup.find('div',class_='poem_body')
        text1 =''
        if div.find('p') == None:
            text1 = list(div.findAll(text=True))
            poem = ''.join(text1[:len(text1)-15])
            poems.append(str(poem))
        else:
            st =[]
            for child in div.findChildren('p'):
        
                if child.text == '\r\n\t\xa0':        
                    continue
                text1 += child.text
            
            st.append(str(text1))
            text1 = list(div.findAll(text=True))
            text1 = ''.join(text1)
            st.append(text1)
            poem = ''.join(st)
            poems.append(str(poem))

        span = soup.find('span',class_='n')
        author_name = span.a.text    
        authors.append(author_name)
        category.append(categories[i])
        titles.append(AllTitles[i])
        data = list(zip(authors,titles, poems, category))
        for row in data:
            fileWriter.writerow(row)

    
        if( i!=0 and i%19 == 0):
            time.sleep(20)
    



print("Types and length of each extracted list\n")
print('Links   ' + " --> " + str(type(links)) + " --> " + str(len(links)))
print('titles  ' + " --> " + str(type(titles)) + " --> " + str(len(titles)))
print('category' + " --> " + str(type(category)) + " --> " + str(len(category)))
print('poems   ' + " --> " + str(type(poems)) + " --> " + str(len(poems)))
print('authors ' + " --> " + str(type(authors)) + " --> " + str(len(authors)))



