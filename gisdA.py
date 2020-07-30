#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Google image searching and downloading script (Ver 0.1)
"""

# import modules
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
from tqdm import tqdm
import requests
import time
import urllib.request
from urllib.parse import quote
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

class gisdA:
    def __init__(self):
        pass

    def ext_fig(self, keywords, limit):
        # make directory
        self.create_dir(root_dir, keywords)
        # scrolling google browser
        try:
            # browser extraction part ####
            chrome_opt = webdriver.ChromeOptions()
            chrome_opt.add_argument('--disable-gpu')
            pathx = "/Users/uksu/Downloads/chromedriver"
            browser = webdriver.Chrome(executable_path=pathx,options=chrome_opt)
            ActionChains(browser).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
            url = 'https://www.google.com/search?q=' + quote(
                keywords.encode('utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            browser.get(url)
            time.sleep(1)
            element = browser.find_element_by_tag_name("body")
            # Scroll down
            for i in range(30):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
            try:
                browser.find_element_by_id("smb").click()
                for i in range(50):
                    element.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.3)  # bot id protection
            except:
                for i in range(10):
                    element.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.3)  # bot id protection
            # click more
            elementx = browser.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input')
            browser.execute_script("arguments[0].click();", elementx)
            # scroll down2
            for i in range(30):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
            try:
                browser.find_element_by_id("smb").click()
                for i in range(50):
                    element.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)  # bot id protection
            except:
                for i in range(10):
                    element.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)  # bot id protectio
                    print("End of the searching pages")
                    time.sleep(0.3)
        except Exception as e:
            print(e)
            # exit(0)

        # extract figures one by one
        fig_list = []
        link_list = []
        i = 1
        while i < limit + 1:
            try:
                elementx1 = browser.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img')
                browser.execute_script("arguments[0].click();", elementx1)
                time.sleep(1)
                try:
                    l_path = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[3]/div[2]/a'
                    link = browser.find_element_by_xpath(l_path)
                    link_tmp = link.get_attribute('href')
                    link_list.append(link_tmp)
                    f_path = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img'
                    fig = browser.find_element_by_xpath(f_path)
                    fig_tmp = fig.get_attribute('src')
                    fig_list.append(fig_tmp)
                except:
                    print("Skip this item" + ":  " + link_tmp)
            except:
                print("Skip this item" + ":  " + link_tmp)
            i += 1
            # browser.quit()
        return link_list, fig_list

    def create_dir(self, root_dir, name):
        try:
            if not os.path.exists(root_dir):
                os.makedirs(root_dir)
                time.sleep(0.2)
                path = (name)
                sub_directory = os.path.join(root_dir, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                path = (name)
                sub_directory = os.path.join(root_dir, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)

        except OSError as e:
            if e.errno != 17:
                raise
            pass
        return

# HELP Section
parser = argparse.ArgumentParser(description='## Search and download images using Google engine ##', formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='''\
version history:
    [ver0.10]       release of this script (2020.07.30)

++ Copyright at uschoi@nict.go.jp / qtwing@naver.com ++
''')
parser.add_argument("Keyword", help="Keywords without space",)
parser.add_argument("Item_number", help="Searching item number")
# parser.add_argument("URL_output.txt", help="URL text files")
parser.add_argument('--version', action='version', version='Version 0.1')
parser.parse_args()

# assign arguments
keyword = sys.argv[1]
itemN = int(sys.argv[2])

# root directiory
root_dir = "gisdA_figure/"

# MAIN RUN
response = gisdA
links, figures = response().ext_fig(keyword, itemN)

# For-loop for downloading figures and links

# print(links)

path = root_dir + keyword
# link downloads
print("")
print(" +++++++++++++++++++++++++++++++++++++ NOW EXTRACTION IS STARTING +++++++++++++++++++++++++++++++++++++ ")
print("")
with open(os.path.join('./' + root_dir + '/', keyword + '.txt'), 'w') as f:
    print(" [ Extracting figure original addresses !! ] ")
    print(" ")
    pbar = enumerate(tqdm(links))
    for item_ind1, item1 in pbar:
        f.write(keyword + "-" + '%04d' %(item_ind1 + 1) + ":   " + "%s\n" % item1)
        time.sleep(0.01)
##
print(" ")
##
# figure downloads
print(" [ Now downloading Figures !! ] ")
print(" ")
pbar2 = enumerate(tqdm(figures))
for item_ind2, item2 in pbar2:
    if 'data:image' in item2:
        filename = keyword + "_" + '%04d' % (item_ind2 + 1) + ".jpg"
        urllib.request.urlretrieve(item2, os.path.join(path, filename))
    elif '.webp' in item2:
        filename_tmp = keyword + "_" + '%04d' % (item_ind2 + 1) + ".webp"
        filename = keyword + "_" + '%04d' % (item_ind2 + 1) + ".jpg"
        r = requests.get(item2)
        with open(os.path.join(path, filename_tmp), 'wb') as outfile:
            outfile.write(r.content)
        # convert webp to jpg
        im = Image.open(os.path.join(path, filename_tmp)).convert("RGB")
        im.save(os.path.join(path, filename), "jpeg")
    else:
        filename = keyword + "_" + '%04d' % (item_ind2 + 1) + ".jpg"
        r = requests.get(item2, verify=True)
        with open(os.path.join(path, filename), 'wb') as outfile:
            outfile.write(r.content)

print("")
print(" +++++++++++++++++++++++++++++++++++++ NOW EXTRACTION FINISHED ++++++++++++++++++++++++++++++++++++++++ ")
print("")
























#
