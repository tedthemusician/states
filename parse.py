import json
import re
from bs4 import BeautifulSoup

from utils import get_states

nondigit = re.compile(r'\D+')
parenthetical = re.compile('\([^\)]+\)')


def parse_coord(coord):
    # Some states are decimal values of degrees, not degrees and minutes
    if '.' in coord:
        return float(coord.split('°')[0])

    degrees, *rest = re.split(nondigit, coord)

    # Some coords contain only degrees, no minutes
    if len(rest) == 1:
        return int(degrees)

    minutes = rest[0]
    return int(degrees) + (int(minutes) / 60)


def parse_coords(raw_coords):
    delim = ' to ' if ' to ' in raw_coords else '–'
    coords = raw_coords.split(delim)

    # Some boundaries are a parallel and only need one numeric value
    if len(coords) == 1:
        c = parse_coord(coords[0])
        return c, c

    c1, c2 = coords
    return parse_coord(c1), parse_coord(c2)


def make_coord_finder(label):
    def finder(doc):
        tag = doc.find(lambda tag: tag.contents == [label])
        next_tag = tag.next_sibling
        data = next_tag.contents

        # Most pages have coords as a plain string
        if len(data) == 1:
            return parse_coords(data[0])

        else:
            children = list(next_tag.children)

            # Some pages have one coord wrapped in an anchor tag
            if len(children) == 2:
                full_string = children[0].string + children[1].string
                return parse_coords(full_string)

            # Some pages have both coords wrapped in anchor tags
            elif len(data) == 3:
                children = list(next_tag.children)
                c1 = parse_coord(children[0].contents[0])
                c2 = parse_coord(children[2].contents[0])
                return c1, c2

        raise Exception('Bad data')

    return finder


get_lats = make_coord_finder('Latitude')
get_lons = make_coord_finder('Longitude')


def format_name(name):
    return re.sub(parenthetical, '', name.replace('_', ' ')).strip()


def read_page(state):
    with open(f'./pages/{state}.html', 'r') as f:
        page = f.read()
    doc = BeautifulSoup(page, features='html.parser')
    lats = get_lats(doc)
    lons = get_lons(doc)
    return {'name': format_name(state), 'lats': lats, 'lons': lons}


def main():
    states = get_states()
    points = [read_page(state) for state in states]
    with open('points.json', 'w') as f:
        json.dump(points, f)


if __name__ == '__main__':
    main()
