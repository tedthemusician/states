from urllib.request import urlopen
from utils import get_states


def save_page(state):
    url = f'https://en.wikipedia.org/wiki/{state}'
    print('Fetching', state)
    page = urlopen(url)
    with open(f'./pages/{state}.html', 'wb') as f:
        f.write(page.read())


def main():
    states = get_states()
    for state in states:
        save_page(state)


# no ifmain since we've already done this, and we don't want to accidentally
# do it again
