#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################### START NOTES ###################
# Current alternative to manually going through the list - check the syllabus for each class. But doesn't give you a nice visual representation easily. 
################### END NOTES ###################

from bs4 import BeautifulSoup
from selenium import webdriver


# driver = webdriver.Firefox()
driver = webdriver.PhantomJS()
# driver.save_screenshot("screen.png")

driver.get("http://registrar.berkeley.edu/sis-SC-message")

html = driver.page_source

soup = BeautifulSoup(html, "lxml")


table = soup.find("table")
# table_body = table.find("tbody")
print("TABLE START")

# for row in table.find_all("tr")[1:]:
#     for col in row.find_all("td"):
#         print(col.get_text())

row_data = []
for row in table.find_all("tr")[1:]:
    temp = []
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    # row_data.append([ele for ele in cols if ele])
    row_data.append(cols)
print(row_data)




def main():
    pass



################### SCRAPYARD ###################

# result = soup.find_all("div", class_="product-review")

# for link in soup.find_all("a"):
#     print(link.get("href",None),link.get_text())

# for tag in soup.find_all("title"):
#     print(tag.text)
#     print("~end~")
