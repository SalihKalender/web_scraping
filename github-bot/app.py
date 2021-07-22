from os import link
from user_info import user_name,password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
class Github:
    
    url = 'https://github.com/'
    driver_path = 'C:\drivers\chrome\chromedriver'

    def __init__(self):
        self.userName = user_name
        self.password = password
        self.followers = []
        self.browser = webdriver.Chrome(Github.driver_path)

    def sign_in(self):
        self.browser.get(Github.url + 'login')
        self.browser.find_element_by_id('login_field').send_keys(self.userName)
        self.browser.find_element_by_id('password').send_keys(self.password)
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        self.browser.close(False) 

    def find_popular_repos(self,repoName):
        self.browser.get(Github.url)
        search_input = self.browser.find_element_by_css_selector('input[placeholder="Search GitHub"]')
        search_input.send_keys(repoName)
        search_input.send_keys(Keys.ENTER)
        repos = self.browser.find_elements_by_class_name('repo-list-item')
        datas = {}
        for repo in repos:
            try:
                repo_name = repo.find_elements_by_tag_name('a')[0].text
                repo_dsc = repo.find_elements_by_tag_name('p')[0].text
                keywords = repo.find_elements_by_tag_name('a')[1::]
                keyword_data = []
                for i in range(len(keywords) - 1):  
                    keyword_data.append(keywords[i].text)
                datas[repo_name] = { 'description': repo_dsc, "keywords": keyword_data }
            except IndexError:  
                continue
        with open('search_results.json','w',encoding='UTF-8') as file:
            json.dump(datas,file,indent=2,ensure_ascii=False)

    def get_followers(self,user_name):
        self.browser.get(Github.url + user_name + '?tab=followers')
        while True:
            links = self.browser.find_element_by_class_name('pagination').find_elements_by_tag_name('a')
            if(len(links) < 2):
                if(links[0].text == 'Next'):
                    self.add_followers()
                    links[0].click()
                    self.add_followers()
                else:
                    time.sleep(2)
                    self.browser.close()
                    break   
            else:
                links[1].click()
                self.add_followers()

    def add_followers(self):    
        users = self.browser.find_elements_by_css_selector('.d-table.table-fixed')
        # print(users)
        for user in users:
            user_Name = user.find_elements_by_tag_name('div')[1].find_element_by_tag_name('a').find_elements_by_tag_name('span')[0].text
            nick_name = user.find_elements_by_tag_name('div')[1].find_element_by_tag_name('a').find_elements_by_tag_name('span')[1].text
            self.followers.append({"user_name":user_Name,"nick_name":nick_name})
            

app = Github()
app.sign_in()
app.find_popular_repos('python')
app.get_followers('acatzk')
# print(app.followers)
