from login import login

def get_favorites(api, restrict):
    #get the id of works 
    all_ids=[]
    json_result = api.user_bookmarks_illust(api.user_id, restrict = restrict)
    while 1:
        illusts = json_result.get('illusts', [])
        all_ids.extend(illust['id'] for illust in illusts)
        next_qs = api.parse_qs(json_result.next_url)
        if not next_qs:
            break
        json_result = api.user_bookmarks_illust(**next_qs)
    return all_ids

if __name__ == "__main__":
    api = login()
    ids = get_favorites(api, "private")
    print(f"ID: {ids}")