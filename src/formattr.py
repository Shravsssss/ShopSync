"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

from datetime import datetime
import math
import html

"""
The formatter module focuses on processing raw text and returning it in
the required format.
"""


def formatResult(website, titles, prices, links):
    """
    The formatResult function takes the scraped HTML as input and extracts the
    necessary values from the HTML code, e.g., extracting a price '$19.99' from
    a paragraph tag.
    """
    title, price, link = '', '', ''

    # Extract title
    if titles and hasattr(titles[0], 'get_text'):
        title = titles[0].get_text().strip()
    elif isinstance(titles, str):
        title = titles.strip()
    if prices:
        price_parts = [p.get_text().strip() if hasattr(p, 'get_text') else str(p).strip() for p in prices]
        price = ''.join(price_parts).replace('\n', '').replace(' ', '')

    # Extract link
    if links and hasattr(links[0], 'get'):
        link = links[0]['href']
    elif isinstance(links, str):
        link = links.strip()
    product = {
        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "title": html.unescape(title),
        "price": price,
        "link": f'www.{website}.com{link}' if link and not link.startswith('http') else link,
        "website": website,
    }

    # Adjust the link for specific websites if necessary
    if website in ['walmart', 'costco']:
        if link.startswith('http'):
            product['link'] = link

    return product


def sortList(arr, sortBy, reverse):
    """
    The sortList function is used to sort the products list based on the
    flags provided as args. Currently, it supports sorting by price.
    """
    if sortBy == "pr":
        return sorted(arr, key=lambda x: getNumbers(x["price"]), reverse=reverse)
    # To-do: sort by rating
    elif sortBy == "ra":
        # return sorted(arr, key=lambda x: getNumbers(x.price), reverse=reverse)
        pass
    return arr


def formatSearchQuery(query):
    """
    The formatSearchQuery function formats the search string into a string that
    can be sent as a url paramenter.
    """
    return query.replace(" ", "+")


def formatSearchQueryForCostco(query):
    """
    The formatSearchQueryForCostco function formats the search string into a string that
    can be sent as a url paramenter.
    """
    queryStrings = query.split(' ')
    formattedQuery = ""
    for str in queryStrings:
        formattedQuery += str
        formattedQuery += '+'
    formattedQuery = formattedQuery[:-1]
    return formattedQuery



def getNumbers(st):
    """
    The getNumbers function extracts float values (price) from a string.
    Ex. it extracts 10.99 from '$10.99' or 'starting at $10.99'
    """
    ans = ''
    for ch in st:
        if (ch >= '0' and ch <= '9') or ch == '.':
            ans += ch
    try:
        ans = float(ans)
    except:  # noqa: E722
        ans = math.inf
    return ans
