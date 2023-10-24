import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter
from dotenv import load_dotenv

load_dotenv()

def parser(link):
    res = requests.get(link)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    tags = soup.findAll('img')
    for match in tags:
        match.decompose()
    tags = soup.findAll('picture')
    for match in tags:
        match.decompose()
    tags = soup.findAll('head')
    for match in tags:
        match.decompose()
    tags = soup.findAll('header')
    for match in tags:
        match.decompose()
    tags = soup.findAll('script')
    for match in tags:
        match.decompose()
    tags = soup.findAll('noscript')
    for match in tags:
        match.decompose()
    tags = soup.findAll('a')
    for match in tags:
        del match["href"]
    tags = soup.findAll('div')
    for match in tags:
        del match["class"]
        del match["id"]
        del match["role"]
    
    if str(soup.find('article')) != 'None':
        main = soup.find('article')
    elif str(soup.find('main')) != 'None':
        main = soup.find('main')
    else:
        main = soup.find('body')
    cleaned_html = str(main)
    markdown_text = markdownify.markdownify(cleaned_html)
    return markdown_text