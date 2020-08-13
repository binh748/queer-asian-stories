"""This module contains functions to scrape gaysiandiaries.com and
https://gaysianthirdspace.tumblr.com/."""
# Need to go back and clean this code so I'm not creating a soup every time.
# I should just pass soup into the function.

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
         'url': blog_url,
         'text': gd_get_blog_text(blog_url)}
        for blog_url in blog_urls
    ]
    return blog_dicts


def g3s_get_tag_page_url(base_url):
    soup = create_soup(base_url)
    tag_pages = []
    for element in soup.find('div', class_='body-text').find_all('a'):
        tag_pages.append(element.get('href'))
    return tag_pages


def g3s_get_num_tag_pages(url):
    soup = create_soup(url)
    if soup.find(class_='next'):
        return int(soup.find(class_='next').get('data-total-pages'))
    return 1


def g3s_get_blog_urls(urls):
    blog_urls = []
    for url in urls:
        urls_to_scrape = [url]
        num_pages = g3s_get_num_tag_pages(url)
        if num_pages > 1:
            for i in range(2, num_pages+1):
                urls_to_scrape.append(f'{url}/page/{i}')
        soups = create_soups(urls_to_scrape)
        for soup in soups:
            for element in soup.find_all(class_='meta-item post-notes'):
                blog_urls.append(element.get('href').replace('#notes', ''))
    # Using set to return all unique blog_urls since some may be repeating due
    # to having mutliple tags featured in Post Directory page
    return list(set(blog_urls))


def g3s_get_blog_title(blog_url):
    soup = create_soup(blog_url)
    if soup.find(class_='title'):
        return soup.find(class_='title').text
    if soup.find(class_='link-title'):
        return soup.find(class_='link-title').text
    return None


def g3s_get_blog_date(blog_url):
    soup = create_soup(blog_url)
    return soup.find(class_='meta-item post-date').text


def g3s_get_blog_text(blog_url):
    paragraphs = []
    soup = create_soup(blog_url)
    for element in soup.find_all('p'):
        paragraphs.append(element.text)
    text = '\n\n'.join(paragraphs) # Adding two line breaks for readability
    return text


def g3s_get_blog_dicts(blog_urls):
    counter = 0
    blog_dicts = []
    for blog_url in blog_urls:
        blog_dicts.append(
            {'title': g3s_get_blog_title(blog_url),
             'date': g3s_get_blog_date(blog_url),
             'url': blog_url,
             'text': g3s_get_blog_text(blog_url)})
        counter += 1
        print(counter)
    return blog_dicts
