import base64
import requests
from requests import post, get
import json

CLIENT_ID = '0eb4a8d852b8488fbad67a83956d0a0e'
CLIENT_SECRET = '071812ad19cd47df8fe78085995820a1'


def get_token():
    """
    gets token
    """
    auth_code = f'{CLIENT_ID}:{CLIENT_SECRET}'
    code_credential = str(base64.b64encode(auth_code.encode("utf-8")), "utf-8")
    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + code_credential,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_res = json.loads(result.content)
    return json_res["access_token"]

def get_aut_head(token):
    """
    gets autorization header
    """
    return {'Authorization': f'Bearer {token}'}

def search_aut(token, artist):
    """
    searches for artist
    """
    url = 'https://api.spotify.com/v1/search'
    request_params = {
        'query': artist,
        'type': 'artist'
    }
    response = requests.get(url, headers = get_aut_head(token), params=request_params)
    response_data = response.json()
    with open("kved_results.json", "w", encoding="utf-8") as fff:
        json.dump(response_data, fff, indent = 4, ensure_ascii=False)
    return response_data

def main():
    """
    print all information
    """
    artist = input("Input the name of artist: ")
    artist_info = search_aut(get_token(), artist)

    opt = input("write what you are going to check from items (followers, genres, popularity): ")
    while opt != "followers" and opt != "genres" and opt != "popularity":
        opt = input("There is a mistake in word you wrote, write one from the list below: ")
    if opt == "followers":
        print(artist_info["artists"]["items"][0]["followers"]["total"])
    else:
        print(artist_info["artists"]["items"][0][opt])

if __name__ == "__main__":
    main()
