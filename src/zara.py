from bs4 import BeautifulSoup as BS
import requests
import jsonpickle
import os
import argparse


class ZaraItem:
    def __init__(self, url, sizes=[], mail_count=0):
        self.url = url
        self.mail_count = mail_count
        self.sizes = sizes

    def __iter__(self):
        yield 'url', self.url
        yield 'mail_count', self.mail_count
        yield 'sizes', self.sizes

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f'URL: {self.url}, Mail Count: {self.mail_count}, '
            f'Tracked Sizes: {self.sizes}'
        )

    def __getParsedHTML(self):
        response = requests.get(self.url)
        soup = BS(response.text, 'html.parser')
        return soup

    def __isSizeAvailable(self, size):
        soup = self.__getParsedHTML()
        size_list = soup.find(class_='size-list')
        if size == 'S':
            small_size_class_attr = ', '.join(
                size_list.contents[0].attrs['class'])
        elif size == 'M':
            small_size_class_attr = ', '.join(
                size_list.contents[1].attrs['class'])
        elif size == 'L':
            small_size_class_attr = ', '.join(
                size_list.contents[2].attrs['class'])
        else:
            return False
        return small_size_class_attr.find('disable') == -1

    def isAnyTrackedSizeAvailable(self):
        if any([self.__isSizeAvailable(size) for size in self.sizes]):
            return True
        else:
            return False


class ZaraTrackingList:
    def __init__(self, items: list = []):
        self.items = items

    def __iter__(self):
        yield 'items', self.items

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '\n'.join([str(item) for item in self.items])

    def add_zara_item(self, new_item: ZaraItem):
        if new_item.url not in [item.url for item in self.items]:
            self.items.append(new_item)

    def remove_zara_item(self, remove_url: str):
        self.items = [item for item in self.items if item.url != remove_url]

    def saveToJSON(self, json_file):
        with open(json_file, 'w') as file:
            frozen = jsonpickle.encode(self, indent=4)
            file.write(frozen)
            file.truncate()

    @property
    def count(self):
        return len(self.items)


if __name__ == "__main__":
    # Usage
    parser = argparse.ArgumentParser()
    parser.add_argument('action', type=str, choices=['add', 'remove', 'print'])
    parser.add_argument('--url', type=str, default=None,
                        help='url of the tracked item, must be supplied for add/remove')
    parser.add_argument('--size', type=str, default=None, nargs='+', choices=['S', 'M', 'L'],
                        help='the tracked sizes with space between them.')
    args = parser.parse_args()
    if args.action in ['add', 'remove']:
        if args.url is None:
            parser.error(f'{args.action} requires --url.')
        if args.action == 'add' and args.size is None:
            parser.error(f'{args.action} requires --size.')
    args = parser.parse_args()

    # Start main
    data_file = os.path.dirname(os.path.abspath(
        __file__)) + os.path.sep + os.path.join('..', 'data', 'data.json')
    try:
        with open(data_file, 'r') as file:
            content = file.read()
            tracking_list = jsonpickle.decode(content)
    except:
        tracking_list = ZaraTrackingList()

    if args.action == 'add':
        new_item = ZaraItem(args.url, sizes=args.size)
        tracking_list.add_zara_item(new_item)
        tracking_list.saveToJSON(data_file)
    elif args.action == 'remove':
        tracking_list.remove_zara_item(args.url)
        tracking_list.saveToJSON(data_file)
    else:
        print(tracking_list)
