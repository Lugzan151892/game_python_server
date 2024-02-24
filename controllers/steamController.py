from flask import request
from api.Api import Api
import urllib.request
from decouple import config
import json

class Steam():
    steam_url = config('STEAM_URL')
    steam_key = config('STEAM_KEY')
    def get_steam_html(self):
        path = request.args.get('path')
        print(path)
        if not path:
            return Api('Steam link invalid').bad_request()
        
        html = urllib.request.urlopen(path).read().decode("utf-8")
        steamId = html.split('"steamid":"')[1].split('",')[0]
        response = { "steamId": steamId }
        return Api("User has found", response).response()
    
    def get_banned_users_data(self):
        list = request.json['banned_list']
        data = urllib.request.urlopen(f"{self.steam_url}?key={self.steam_key}&steamids={','.join(list)}").read().decode("utf-8")
        if not data:
            return Api('Something went wrong on server side').internal()
        print(json.loads(data)['response'])
        return Api(data=json.loads(data)['response']).response()

