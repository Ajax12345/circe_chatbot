from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json, time, re
from bs4 import BeautifulSoup as soup 
results = {}
d = webdriver.Chrome('/Users/jamespetullo/Downloads/chromedriver')
_schools = [i for b in json.load(open('all_schools.json')) for i in b]

for school in _schools:
    try:
        print('school', school)
        
        d.get('https://bigfuture.collegeboard.org/find-colleges')
        time.sleep(4)
        inputElement = d.find_element_by_id("supportModule_searchCollegeByName_hero_availablePanel")
        inputElement.send_keys(school)
        inputElement.send_keys(Keys.ENTER)
        time.sleep(5)
        _link = soup(d.page_source, 'html.parser').find('a', {'class':'copyMed arial'})['href']
        d.get(_link)
        time.sleep(5)
        elem = d.find_element_by_link_text("Majors & Learning Environment")
        elem.send_keys('\n')
        time.sleep(3)
        elem1 = d.find_element_by_link_text("All Majors")
        
        elem1.send_keys('\n')
        time.sleep(4)
        _table = soup(d.page_source, 'html.parser').find_all('table', {'class':re.compile('^majorsOfferedTable')})
        final_table = [[[[i.text for i in b.find_all('th')], [i.text for i in b.find_all('td')]] for b in h.find_all('tr')] for h in _table]
        results[school] = final_table
        print('final_table', final_table)
        time.sleep(1)
    except:
        pass


with open('full_school_major_listings.json', 'w') as f:
    json.dump(results, f)