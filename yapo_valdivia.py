#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 17:00:00 2018
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
import urllib.request
from selenium import webdriver
import time

profile = pd.DataFrame(columns=['Link', 'Title', 'Description', 'Price','Date', 'Name', 'Category'])

browser = webdriver.Chrome()
myUrl = 'https://www.yapo.cl/los_rios/todos_los_avisos?ca=11_s&l=0&w=1&cmn=243'
browser.get(myUrl)
pageSoup = soup(browser.page_source, 'html.parser')

pages = pageSoup.find('span',  {'class', 'nohistory FloatRight'}).a['href']

index = pages.rfind('=')

lastPage = int(pages[index+1:])

pages = pages[:index+1]

for i in range(lastPage):
    url = pages + str(i+1)
    browser.get(url)
    pageSoup = soup(browser.page_source, 'html.parser')
    links = pageSoup.findAll('td', {'class' : 'thumbs_subject'})
    for link in links:
        h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13 = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
        print(link.find('a',{'class':'title'})['href'])
        browser.get(link.find('a',{'class':'title'})['href'])
        pageSoup = soup(browser.page_source, 'html.parser')
        if(pageSoup.find('h1', {"id" : "da_subject"})):
            h1 = pageSoup.find('h1', {"id" : "da_subject"}).text.strip()
            
        if(pageSoup.find('article')):
            h2 = pageSoup.find('article').find('div',{"id" : "dataAd"}).attrs['data-datetime'].split(' ', 1)[0]
        
        if(pageSoup.find('aside', {"class" : "sidebar-right"})):
            aside = pageSoup.find('aside', {"class" : "sidebar-right"})
            print("username?")
            h3=aside.find('seller-info').attrs['username']
            print(h3)
        
        if(pageSoup.find('div', {"class" : "referencial-price text-right"})):
            h4 = pageSoup.find('div', {"class" : "referencial-price text-right"}).text.strip().replace(u'\n', u' ').replace(u'\t', u'')
        
        if(pageSoup.find('div', {"class" : "price text-right"})):
            h5 = pageSoup.find('div', {"class" : "price text-right"}).text.strip().replace(u'\n', u' ').replace(u'\t', u'')
            print("price:"+h5)
        	
        table = pageSoup.find('table')
        
        #tr = table.findAll('tr')
        #t = {}
        #for k in tr:
        #    if(k.th and k.td):
        #        t[k.th.text.strip()] = k.td.text.strip()
        
        #if 'Tipo de inmueble' in t.keys():
        #    h6 = t['Tipo de inmueble']
            
        #if 'Comuna' in t.keys():
        #    h7 = t['Comuna']
            
        #if 'Superficie total' in t.keys():
        #    h8 = t['Superficie total']
            
        #if 'Superficie útil' in t.keys():
        #    h9 = t['Superficie útil']
            
        #if 'Dormitorios' in t.keys():
        #    h10 = t['Dormitorios']
            
        #if 'Baños' in t.keys():
        #    h11 = t['Baños']
            
        #if 'Código' in t.keys():
        #    h12 = t['Código']
            
        if(pageSoup.find('div', {"class" : "description"})):
            try:
                h13 = pageSoup.find('div', {"class" : "description"}).text.split(' ', 1)[1].strip().replace(u'\n', u' ')
            except:
                continue

        if(pageSoup.find('div', {"class" : "breadcrumbs"})):
            h14 = pageSoup.find('div', {"class" : "breadcrumbs"}).find('a', {"id" : "breadcrumb_category"}).find('strong').text.strip().replace(u'\n', u' ')
            print(h14)


            
        #if(pageSoup.find('div', {'class':'phoneUser'})):
        #    h14_text = pageSoup.find('div', {'class':'phoneUser'})
        #    if(h14_text.img):
        #        h14 = 'yapo.cl' + h14_text.img['src']
        
        ser = pd.Series([link.a['href'], h1, h13, h5, h2, h3, h14],
                        index =['Link', 'Title', 'Description', 'Price', 'Date', 'Name', 'Category'])

        profile = profile.append(ser, ignore_index=True)
        print(link.a['href'])

#print(profile)
        filename = 'fre.xlsx'
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        profile.to_excel(writer, index=False)
        writer.save()
