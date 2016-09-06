import os
import sys
import tarfile

import click
import requests
import wget
from bs4 import BeautifulSoup


@click.command()
@click.option('--url')
@click.option('--start', default=0)
@click.option('--stop', default=10)
@click.option('--directory', default='downloads')
def download_files(url, start=0, stop=10, directory='downloads'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    nodes = soup.find_all('a')
    for node in nodes[start:stop]:
        href = node.get('href')
        if '..' not in href:
            file_url = url + href
            wget.download(file_url, out=directory)
    tarfilename = directory + '.tar.bz2'
    f = tarfile.open(tarfilename, 'w|bz2')
    f.add(directory)
    f.close()

if __name__ == '__main__':
    download_files(sys.argv[1:])
