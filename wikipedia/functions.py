import requests

WIKIPEDIA_API_URL = "https://uz.wikipedia.org/w/api.php"

def search_wikipedia(query):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|pageimages",
        "exintro": True,
        "explaintext": True,
        "piprop": "original",
        "titles": query
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    page_id = next(iter(data['query']['pages'].keys()))
    if page_id != "-1":
        page = data['query']['pages'][page_id]
        title = page['title']
        extract = page['extract']
        if 'original' in page['original']:
            image_url = page['original']['original']
        else:
            image_url = None
        return title, extract, image_url
    else:
        return None, None, None
