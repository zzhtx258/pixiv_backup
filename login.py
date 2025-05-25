from pixivpy3 import AppPixivAPI
from gppt import GetPixivToken
import os

def get_refresh_token(user, psw) -> str:
    with open("token.txt", "w+") as f:
        if refresh_token := f.read().strip():
            return refresh_token

        g = GetPixivToken(headless=True)
        refresh_token = g.login(username=user, password=psw)["refresh_token"]
        f.write(refresh_token)
    return refresh_token

def login():
    if (os.path.exists('token.txt')):
        with open("token.txt", 'r') as f:
            for l in f:
                REFRESH_TOKEN = l
    else:
        user = input("please enter user id (with out '@'):")
        psw = input("please enter password:")
        REFRESH_TOKEN = get_refresh_token(user, psw)
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)
    return api
    

if __name__ == "__main__":
    api = login()
    json_result = api.user_bookmarks_illust(api.user_id)
    print(json_result)