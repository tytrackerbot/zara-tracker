from bs4 import BeautifulSoup as BS
import requests
import jsonpickle
import os


class ZaraItem:
    def __init__(self, url, count=0):
        self.url = url
        self.mail_count = count

    def __iter__(self):
        yield 'url', self.url
        yield 'mail_count', self.mail_count

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f'URL: {self.url}, Mail Count: {self.mail_count}, '
            f'Small Size Available: {self.isSmallSizeAvailable()}'
        )

    def __getParsedHTML(self):
        response = requests.get(self.url)
        soup = BS(response.text, 'html.parser')
        return soup

    def isSmallSizeAvailable(self):
        soup = self.__getParsedHTML()
        size_list = soup.find(class_='size-list')
        small_size_class_attr = ', '.join(size_list.contents[2].attrs['class'])
        return small_size_class_attr.find('disable') == -1

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
