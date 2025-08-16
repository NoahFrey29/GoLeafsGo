import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 29, "name": "Noah", "views": 100}, {"likes": 18, "name": "Krupa", "views": 100000}, {"likes": 10, "name": "Pikachu", "views": 2}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "video/2")
print(response.json())