import csv
import os
import requests
import re
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from optparse import OptionParser

URL_HOST = 'nytimes'
CSV_FILE = URL_HOST + '_news.csv'
PATTERN_NY_TIMES_URL = re.compile(
    "https?:\/\/(www\.nytimes.com\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")

# parse commandline arguments
parser = OptionParser()


def is_interactive():
    return not hasattr(sys.modules['__main__'], '__file__')


def saveNewsInCSV(headline, body, byline, publishAt):
    scrapedDate = datetime.now()

    try:
        append_write = None
        if os.path.exists(CSV_FILE):
            append_write = 'a'
        else:
            append_write = 'w'

        csvFile = open(CSV_FILE, append_write)

        # use csv Writer
        csvWriter = csv.writer(csvFile)

        if(append_write == 'w'):
            csvWriter.writerow(['headline',
                                'body',
                                'byline',
                                'publishAt',
                                'scrapedDate'
                                ])

        csvWriter.writerow([headline,
                            body,
                            byline,
                            publishAt,
                            scrapedDate
                            ])
    except Exception as error:
        print("Error saving news in cv file")
        print(error)


def getContentNews(news_url):

    response = requests.get(news_url)
    if(response.status_code != 200):
        if(response.status_code == 404):
            print("Error getting news, status code is: " +
                  str(response.status_code))
            raise Exception(
                'Woow looks like this page dont exists! Check if your URL is valid')
        else:
            print("Error getting news, status code is: " +
                  str(response.status_code))
            raise Exception(
                'Check if the URL is valid, if you have an internet connection or try later!')

    soupContent = BeautifulSoup(response.content, 'html.parser')

    headlineDiv = soupContent.find(attrs={"data-test-id": "headline"})
    headline = headlineDiv.text

    allBodyParagraphsDiv = soupContent.find_all(
        'div', class_='StoryBodyCompanionColumn')
    body = ''
    for paragraph in allBodyParagraphsDiv:
        body += "\n\n" + paragraph.text

    bylineSpan = soupContent.find(
        'span', class_='byline-prefix').find_next('a').contents[0]
    byline = bylineSpan.text

    publishAtTag = soupContent.find(
        'time')
    publishAt = publishAtTag.text

    saveNewsInCSV(headline, body, byline, publishAt)

    return {'body': body,
            'headline': headline
            }


def main():

    newsUrl = None
    argv = [] if is_interactive() else sys.argv[1:]
    (_, args) = parser.parse_args(argv)
    if len(args) <= 0:
        newsUrl = str(
            input('Type the url news from The New York Times site you want to get or type exit: '))
    else:
        newsUrl = args[0]

    try:
        if(newsUrl == 'exit'):
            exit()

        if(PATTERN_NY_TIMES_URL.match(newsUrl)):
            print("Getting news content for " + newsUrl + "...")
            getContentNews(newsUrl)
        else:
            raise Exception(
                'Invalid url for The New York Times site: ' + newsUrl)
    except Exception as error:
        print(error)
        exit()


if __name__ == "__main__":
    main()
