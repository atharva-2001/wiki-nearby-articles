from numpy.core.arrayprint import array2string
import requests
# S = requests.Session()
# # https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=1&titles=Pet_door&explaintext=1&formatversion=2
# URL = "https://en.wikipedia.org/w/api.php"

# PARAMS = {
#     "action": "query",
#     "format": "json",
#     "titles": "Atom",
#     "prop": "extracts",
#     # "pllimit": "max"
#     "exsentences":"2",
#     "exlimit": "1",
#     "explaintext": "1",
#     "formatversion": "2"
# }

# R = S.get(url=URL, params=PARAMS)
# DATA = R.json()
# # print(DATA)
# PAGES = DATA["query"]["pages"][0]
# # print(PAGES["extract"])



def article_summary_for_hover(article_name, number_of_lines):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": article_name,
        "prop": "extracts",
        "exsentences":number_of_lines,
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"][0]
    return PAGES["extract"]


# print(article_summary_for_hover(article_name="Atom", number_of_lines=2))
import re
def find_hover_text(str):
    lst = re.split(" ", str)
    lst = [" ".join(lst[i: i+3]) for i in range(0, len(lst), 3)]
    str = "<br>".join(["".join(item) for item in lst])
    return str
print(find_hover_text(article_summary_for_hover(article_name="Atom", number_of_lines="2")))


