from bs4 import BeautifulSoup
import csv
import requests

html_doc = requests.get('https://www.sadikturan.com/')
obj = BeautifulSoup(html_doc.text,'html.parser')
#-- Course image, Course Title, Course Description, Course Link
courses = obj.select_one('#kurslar')
courses = courses.find_all(class_='kurs')

with open('data.csv','w',encoding='UTF-8',newline='') as file:
    file_writer = csv.writer(file)
    file_writer.writerow(['Course img','Course Name','Course Description','Course Link'])
    for course in courses:
        img = course.find('img')['src']
        name = course.find('h2').string
        description = course.find('span').string
        link = course.find_all('a')[1]['href']
        file_writer.writerow([img,name,description,link])