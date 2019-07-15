import requests
import bs4
import pickle
from itertools import count

url = {'root': 'https://realpython.com'}
url['tutorials'] = url['root'] + '/tutorials/intermediate'

cache_filename = 'cached_responses.pickle'
cached_responses = {}

def load_cached_responses(filename):
    global cached_responses
    try:
        with open(filename, 'rb') as f:
            cached_responses.update(pickle.load(f))
    except IOError as e:
        print(e)

def save_cached_responses(filename):
    global cached_responses
    with open(filename, 'wb') as f:
        pickle.dump(cached_responses, f)

def get_response(url):
    global cached_responses
    if url in cached_responses:
        print(f"Loading cached response: {url}")
        response = cached_responses[url]
        return response
    else:
        with requests.Session() as session:
            response = session.get(url)

        if response.status_code == 200:
            print(f"Successful get: {url}")
            print(f"    content length: {len(response.content)}")
            cached_responses[url] = response
            print(f"    cached: True")
            return response
        else:
            print("Error: unsuccessful get")
            print(f"    url: {url}")
            print(f"    status: {response.status_code}")
            return None

def extract_tutorials(soup, root_url=""):
    premium_tutorials = {}
    non_premium_tutorials = {}

    cards = get_cards(soup)

    for card in cards:
        title, url = extract_card_info(card)
        if is_premium(card):
            premium_tutorials[title] = root_url + url
        else:
            non_premium_tutorials[title] = root_url + url

    return premium_tutorials, non_premium_tutorials

def get_cards(soup):
    return soup.findAll("div", {"class": "card border-0"})

def extract_card_info(card):
    body = card.find("div", {"class": "card-body"})
    title = body.find("h2").text
    url = body.find("a").attrs['href']
    return title, url

def extract_introduction(article_url):
    response = get_response(article_url)

    if response is not None:
        soup = bs4.BeautifulSoup(response.content, 'html5lib')
        article_body = soup.find('div', {'class': 'article-body'})

        # Introductory text is nested between divs at the beginning of the body.
        # As such, we begin by skipping over blank lines and divs:
        children = article_body.children
        while True:
            child = next(children)
            if child == '\n' or child.name == 'div':
                continue
            else: break

        # Store all remaining non-div elements until we hit the next div
        intro = [child]
        while True:
            child = next(children)
            if child == '\n':
                continue
            elif child.name == 'div' or child.name == 'h2':
                break
            else:
                intro.append(child)

        return intro
    else:
        return None

def format_introduction(tag_list):
    intro = []
    for tag in tag_list:
        for line in tag.decode().splitlines():
            intro.append(line)

    return intro

def is_premium(card):
    card_text = card.find("p", {"class": "card-text"})

    if card_text is None:
        print("Error while checking if `div` contains a premium tutorial.")
        print("    Unable to find paragraph with {'class': 'card-text'}.")
        return None

    result = card_text.find("a", {"href": "/account/join/"})
    # Note: this assumes /account/join/ will always be the first anchor
    # within the card-text paragraph

    if result is None:
        return False   # Did not find hyperlink to /account/join/
    else:
        return True    # Found hyperlink to /account/join/

def write_to_markdown(url_dict, filename="file.md", title="# Title\n", is_premium=False):
    with open(filename, 'w') as file:
        lines = [title, '\n']
        
        for title, url in url_dict.items():
            lines.append(f"### [{title}]({url})\n")
            if not is_premium:
                # Write the introduction to the file
                lines.append('\n')
                intro = extract_introduction(url)
                for line in format_introduction(intro):
                    lines.append('> ' + line + '\n')
                lines.append('\n')

        file.writelines(lines)
    
def main():
    load_cached_responses(cache_filename)

    # Initialize empty dictionaries
    premium = {}
    non_premium = {}

    print("Crawling tutorial pages...")

    for i in count(start=1):
        link = url['tutorials'] + f"/page/{i}/"
        response = get_response(link)

        if response is not None:
            soup = bs4.BeautifulSoup(response.content, 'html5lib')
            p, np = extract_tutorials(soup, root_url=url['root'])

            # Count initial number of tutorials
            initial_size = dict(
                p=len(premium),
                np=len(non_premium))

            premium.update(p)
            non_premium.update(np)

            # Check if new tutorials were found
            if len(premium) == initial_size['p'] \
                and len(non_premium) == initial_size['np']:
                print("    No new tutorials found.")
                break
            else:
                print(f"    # Premium tutorials:     {len(premium):3d}")
                print(f"    # Non-Premium tutorials: {len(non_premium):3d}")

        else:
            break

    print("Saving URLs into markdown...")

    write_to_markdown(
        premium, 
        filename="premium_tutorials.md",
        title="# Intermediate, premium tutorials from Real Python\n",
        is_premium=True)

    write_to_markdown(
        non_premium,
        filename="non_premium_tutorials.md",
        title="# Intermediate, non-premium tutorials from Real Python\n",
        is_premium=False)

    print("Saving cached responses...")
    save_cached_responses(cache_filename)

if __name__ == "__main__":
    main()