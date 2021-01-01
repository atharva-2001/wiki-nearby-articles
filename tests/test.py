import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')
page_py = wiki_wiki.page('Atom')

def print_sections(sections, level=0):
        for s in sections:
                print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
                print_sections(s.sections, level + 1)


# print_sections(page_py.sections)
link_data, link_title = [],[]

links = page_py.links
for link in links.keys():
    link_title.append(link)
    link_data.append(links[link])

# for a, b in zip(link_data, link_title):
#     print(a,"==>>",b)

# wiki_html = wikipediaapi.Wikipedia(
#         language='en',
#         extract_format=wikipediaapi.ExtractFormat.HTML
# )
# p_html = wiki_html.page("Atom")
# print(p_html.text)


import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "format": "json",
    "titles": "Atom",
    "prop": "links",
    "pllimit": "max"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

PAGES = DATA["query"]["pages"]

for k, v in PAGES.items():
    for l in v["links"]:
        print(l["title"])

print(DATA)