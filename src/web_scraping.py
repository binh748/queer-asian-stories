"""This module contains functions to scrape gaysiandiaries.com and
https://gaysianthirdspace.tumblr.com/."""

from bs4 import BeautifulSoup
import requests


def create_soup(url):
    """Creates a BeautifulSoup object for a given URL."""
    response_text = requests.get(url).text
    soup = BeautifulSoup(response_text, 'html5lib')
    return soup


def create_soups(urls):
    """Creates a list of BeautifulSoup objects for a list of URLs."""
    soups = []
    for url in urls:
        soup = create_soup(url)
        soups.append(soup)
    return soups


def gd_get_num_pages(base_url):
    soup = create_soup(base_url)
    return int(soup.find_all('a', class_='jump_page')[-1].text)


def gd_get_page_urls(base_url):
    page_urls = [base_url]
    num_pages = gd_get_num_pages(base_url)
    for i in range(2, num_pages+1):
        page_urls.append(f'{base_url}page/{i}')
    return page_urls


def gd_get_blog_urls(base_url):
    page_urls = gd_get_page_urls(base_url)
    blog_urls = []
    for url in page_urls:
        soup = create_soup(url)
        for element in soup.find_all(class_='post_title'):
            blog_urls.append(element.findNext().get('href'))
    return blog_urls


def gd_get_blog_title(blog_url):
    soup = create_soup(blog_url)
    return soup.find(class_='post_title').text


def gd_get_blog_date(blog_url):
    soup = create_soup(blog_url)
    return soup.find(class_='post_date').text


def gd_get_blog_text(blog_url):
    paragraphs = []
    soup = create_soup(blog_url)
    # Start for loop at index 1 since
    # first paragrahph is a generic content warning.
    for element in soup.find_all('p')[1:]:
        paragraphs.append(element.text)
    text = '\n\n'.join(paragraphs) # Adding two line breaks for readability
    return text


def gd_get_blog_dicts(base_url):
    blog_urls = gd_get_blog_urls(base_url)
    blog_dicts = [
        {'title': gd_get_blog_title(blog_url),
         'date': gd_get_blog_date(blog_url),
         'text': gd_get_blog_text(blog_url)}
        for blog_url in blog_urls
    ]
    return blog_dicts


def g3s_get_tag_page_url(base_url):
    tag_pages = []
    soup = create_soup(base_url)
    for element in soup.find('div', class_='body-text').find_all('a'):
        tag_pages.append(element.get('href'))
    return tag_pages
