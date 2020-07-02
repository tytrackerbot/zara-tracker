from bs4 import BeautifulSoup as BS
import requests
import jsonpickle
import os


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

    def isSmallSizeAvailable(self):
        return self.__isSizeAvailable(size='S')

    def isMediumSizeAvailable(self):
        return self.__isSizeAvailable(size='M')

    def isLargeSizeAvailable(self):
        return self.__isSizeAvailable(size='L')

    def saveToJSON(self, filename):
        with open(filename, 'w') as file:
            frozen = jsonpickle.encode(self)
            file.write(frozen)
            file.truncate()


if __name__ == "__main__":
    url = input('URL: ')
    item = ZaraItem(url)
    data_file = os.path.dirname(os.path.abspath(
        __file__)) + os.path.sep + os.path.join('..', 'data', 'data.json')
    item.saveToJSON(data_file)
