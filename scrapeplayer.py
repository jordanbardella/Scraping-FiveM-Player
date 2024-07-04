import datetime
import requests
import re
import time

listcfx = 'listfr.txt'

def extract_codes():
    with open(listcfx, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    pattern = re.compile(r'\b(?=\w*[a-zA-Z])(?=\w*[0-9])\w{6}\b')
    return pattern.findall(contenu)

def fiveminfo(fivemid: str):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{fivemid}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    with requests.Session() as session:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Hostname: {data['Data']['hostname']}")
            print(f"Max Players: {data['Data']['sv_maxclients']}")
            print(f"Current Players: {data['Data']['clients']}")
            players = data['Data']['players']
            file_path = f"playersfr.txt"
            with open(file_path, "a", encoding='utf-8') as file:
                for player in players:
                    player_info = f"Name: {player['name']}, Identifiers: {player['identifiers']}, Endpoint: {player['endpoint']}\n"
                    file.write(player_info)
        else:
            print(f"Failed to fetch server data for {fivemid}.")


def remove_duplicates(input_file, output_file):
    lines_seen = set()
    with open(output_file, "w") as output_file:
        for each_line in open(input_file, "r"):
            if each_line not in lines_seen:
                output_file.write(each_line)
                lines_seen.add(each_line)

def main():
    while True:
        codes = extract_codes()
        for code in codes:
            fiveminfo(code)
            time.sleep(1)
        remove_duplicates('players.txt', 'players_unique.txt')
        print("wait 3.5 minutes.")
        time.sleep(210)

if __name__ == '__main__':
    main()
