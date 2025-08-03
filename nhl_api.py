import http.client

conn = http.client.HTTPSConnection("sports-information.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "sports-information.p.rapidapi.com"
}

conn.request("GET", "/nhl/team-players/21/", headers=headers) #/team-players/21

res = conn.getresponse()
data = res.read()

with open('nhl_players.json', 'w', encoding='utf-8') as f:
    f.write(data.decode("utf-8"))

print("Data successfully written to nhl_players.json")