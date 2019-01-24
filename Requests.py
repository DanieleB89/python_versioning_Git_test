import requests
from googleapiclient.discovery import build
import pprint

# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# print(r.status_code)
# print(r.headers['content-type'])
# print(r.encoding)
# print(r.text)
# r.json()


my_api_key = "AIzaSyBjbnQYk10Eot70wTg_2MV1Pk5oK1VSdEA"
my_cse_id = "007585256921825425247:6wnzpstauiu"


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


results = google_search('wikipedia', my_api_key, my_cse_id, num=1)
for result in results:
    print("---", result)
    if result == "items":
        for item in results[result]:
            print("---*---")
            print(item['link'])
    else:
        print(results[result])
# for result in results:
#     pprint.pprint(result)
