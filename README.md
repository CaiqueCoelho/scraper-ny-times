# Web scraper to get news from The New York Times site

This is a simple scrape to get any news from The New York Times site and save in a csv file

## Requirements and Setup

You just need python3 and beautifulsoup4 to run. To install the dependencies just run in the terminal inside this repo directory:
```bash
>  pip3 install -r requirements.txt
```

### How to use

Just run in the terminal inside this repo directory:

```bash
> python3 scrape_newyorktimes.py news_url
```

Example:
```bash
> python3 scrape_newyorktimes.py https://www.nytimes.com/2020/12/16/us/politics/congress-stimulus-bill.html
```

### Features
- Checks if the url is valid
- Checks if the url is from The New York Times site
- Checks if response getted from the url is valid
- Get title, body, byline and publish date from news
- Save the news in csv file
- Save date when news was scraped

### Work to do
- Get a list of urls like argv param and scrape all news
- Create a endpoint hosting in heroku to return news