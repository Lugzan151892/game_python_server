from flask import request
from api.Api import Api
import urllib.request
from decouple import config
import json

class Steam():
    steam_url = config('STEAM_URL')
    steam_key = config('STEAM_KEY')
    def get_banned_user_data(self, path):
        html = urllib.request.urlopen(path).read().decode("utf-8")
        steamId = html.split('"steamid":"')[1].split('",')[0]
        result = {
            "steamId": steamId
        }
        if 'class="profile_ban_info"' in html:
            result['banned'] = True
        else:
            result['banned'] = False
        return result


    def get_steam_html(self):
        path = request.args.get('path')
        if not path:
            return Api('Steam link invalid').bad_request()
        user = self.get_banned_user_data(path)
        return Api("User has found", user).response()
    
    def get_banned_users_data(self):
        list = request.json['banned_list']
        data = urllib.request.urlopen(f"{self.steam_url}?key={self.steam_key}&steamids={','.join(list)}").read().decode("utf-8")
        if not data:
            return Api('Something went wrong on server side').internal()
        result = []
        for player in json.loads(data)['response']['players']:
            new_item = player
            new_item['banned'] = self.get_banned_user_data(path=player["profileurl"])["banned"]
            result.append(new_item)
        return Api(data={"players": result}).response()

