"""This module contains functions to scrape gaysiandiaries.com and
https://gaysianthirdspace.tumblr.com/."""
# Need to go back and clean this code so I'm not creating a soup every time.
# I should just pass soup into the function.

from bs4 import BeautifulSoup
import requests


def create_soup(url):
    """Creates a BeautifulSoup object for a URL."""
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
    """Returns the number of Gaysian Diary pages. A page can contain multiple blog
    posts."""
    soup = create_soup(base_url)
    return int(soup.find_all('a', class_='jump_page')[-1].text)


def gd_get_page_urls(base_url):
    """Returns a list of URLs for each page in the Gaysian Diaries. A page can
    contain multiple blog posts.

    Args:
        base_url: Gaysian Diaries home page URL.
    """
    page_urls = [base_url]
    num_pages = gd_get_num_pages(base_url)
    for i in range(2, num_pages+1):
        page_urls.append(f'{base_url}page/{i}')
    return page_urls


def gd_get_blog_urls(base_url):
    """Returns a list of URLs for each blog post in the Gaysian Diaries.

    Args:
        base_url: Gaysian Diaries home page URL.
    """
    page_urls = gd_get_page_urls(base_url)
    blog_urls = []
    for url in page_urls:
        soup = create_soup(url)
        for element in soup.find_all(class_='post_title'):
            blog_urls.append(element.findNext().get('href'))
    return blog_urls


def gd_get_blog_title(blog_url):
    """Returns the title of the Gaysian Diaries blog post."""
    soup = create_soup(blog_url)
    return soup.find(class_='post_title').text


def gd_get_blog_date(blog_url):
    """Returns the publishing date of the Gaysian Diaries blog post."""
    soup = create_soup(blog_url)
    return soup.find(class_='post_date').text


def gd_get_blog_text(blog_url):
    """Returns the text of the Gaysian Diaries blog post."""
    paragraphs = []
    soup = create_soup(blog_url)
    # Start for loop at index 1 since
    # first paragrahph is a generic content warning.
    for element in soup.find_all('p')[1:]:
        paragraphs.append(element.text)
    text = '\n\n'.join(paragraphs) # Adding two line breaks for readability
    return text


def gd_get_blog_num_notes(blog_url):
    """Returns the number of tumblr notes for the Gaysian Diaries blog post.

    To learn more about tumblr notes, visit:
    https://tumblr.zendesk.com/hc/en-us/articles/231855888-Notes."""
    soup = create_soup(blog_url)
    if soup.find(class_='notes'):
        num_notes = len(soup.find(class_='notes').find_all('li'))
        return num_notes
    return 0


def gd_get_blog_dicts(base_url):
    """Returns a list of dicts of key information for each Gaysian Diaries blog
    post.

    Args:
        base_url: Gaysian Diaries home page URL.
    """
    blog_urls = gd_get_blog_urls(base_url)
    blog_dicts = [
        {'title': gd_get_blog_title(blog_url),
         'date': gd_get_blog_date(blog_url),
         'num_notes': gd_get_blog_num_notes(blog_url),
         # Will get filled in when combining with Google Analytics data
         'unique_pageviews': None,
         'url': blog_url,
         'text': gd_get_blog_text(blog_url)}
        for blog_url in blog_urls
    ]
    return blog_dicts


def g3s_get_tag_page_url(base_url):
    """Returns list of Gaysian Third Space tag page URLs.

    A tag page is a page belonging to a specific tag such as body image,
    career, coming out, etc. The tags are listed on the post directory page:
    https://gaysianthirdspace.tumblr.com/tags.

    Args:
        base_url: Gaysian Third Space post directory page.
    """
    soup = create_soup(base_url)
    tag_pages = []
    for element in soup.find('div', class_='body-text').find_all('a'):
        tag_pages.append(element.get('href'))
    return tag_pages


def g3s_get_num_tag_pages(url):
    """Returns the number of tag pages in the Gaysian Third Space.

    A tag page is a page belonging to a specific tag such as body image,
    career, coming out, etc. The tags are listed on the post directory page:
    https://gaysianthirdspace.tumblr.com/tags."""
    soup = create_soup(url)
    if soup.find(class_='next'):
        return int(soup.find(class_='next').get('data-total-pages'))
    return 1


def g3s_get_blog_urls(urls):
    """Returns list of URLs for all Gaysian Third Space blog posts.

    Args:
        urls: Gaysian Third Space tag page urls.
    """
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
    """Returns the title of the Gaysian Third Space blog post."""
    soup = create_soup(blog_url)
    if soup.find(class_='title'):
        return soup.find(class_='title').text
    if soup.find(class_='link-title'):
        return soup.find(class_='link-title').text
    return None


def g3s_get_blog_date(blog_url):
    """Returns the publishing date of the Gaysian Third Space blog post."""
    soup = create_soup(blog_url)
    return soup.find(class_='meta-item post-date').text


def g3s_get_blog_text(blog_url):
    """Returns the text of the Gaysian Third Space blog post."""
    paragraphs = []
    soup = create_soup(blog_url)
    for element in soup.find_all('p'):
        paragraphs.append(element.text)
    text = '\n\n'.join(paragraphs) # Adding two line breaks for readability
    return text


def g3s_get_blog_num_notes(blog_url):
    """Returns the number of tumblr notes for the Gaysian Third Space blog post.

    To learn more about tumblr notes, visit:
    https://tumblr.zendesk.com/hc/en-us/articles/231855888-Notes."""
    soup = create_soup(blog_url)
    if soup.find(class_='meta-item post-notes'):
        num_notes = int(soup.find(class_='meta-item post-notes') \
            .text.split()[0].replace(',', ''))
        return num_notes
    return 0


def g3s_get_blog_dicts(blog_urls):
    """Returns list of dicts of key information for each Gaysian Third Space blog
    post.

    Args:
        blog_urls: List of URLs for all Gaysian Third Space blog posts.
    """
    counter = 0
    blog_dicts = []
    for blog_url in blog_urls:
        blog_dicts.append(
            {'title': g3s_get_blog_title(blog_url),
             'date': g3s_get_blog_date(blog_url),
             'num_notes': g3s_get_blog_num_notes(blog_url),
             # Will get filled in when combining with Google Analytics data
             'unique_pageviews': None,
             'url': blog_url,
             'text': g3s_get_blog_text(blog_url)})
        counter += 1
        print(counter)
    return blog_dicts
