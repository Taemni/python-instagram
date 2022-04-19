import requests
import json
import os
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "referer": "https://www.instagram.com/",
}


def download(url, filename=None):
    if not filename:
        filename = url.split("/")[-1].split("?")[0]
    with open(filename, "wb") as file:
        try:
            response = requests.get(url, headers=headers)
            file.write(response.content)
        except Exception:
            return False
    return True


def get_cookie():
    with open("cookie.txt") as f:
        cookie = f.readline()
        cookie = cookie.replace('"', ";").replace("'", '"').replace(";", "'")
        cookie = json.loads(cookie)
    return cookie


def get_userid(username):
    r = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers, cookies=get_cookie()).json()["graphql"]["user"]
    print(f"[*] Username: {r['username']}")
    print(f"[*] Full name: {r['full_name']}")
    print(f"[*] User id: {r['id']}")
    print(f"[*] Following: {format(r['edge_follow']['count'], ',')}명")
    print(f"[*] Followers: {format(r['edge_followed_by']['count'], ',')}명")
    print(f"[*] Feeds: {format(r['edge_owner_to_timeline_media']['count'], ',')}개")
    return r['id']


def get_feed(username):
    feeds = []
    end_cursor = None
    after = ""
    while True:
        if end_cursor:
            after = f',"after":"{end_cursor}"'
        url = f'https://www.instagram.com/graphql/query/?query_hash=396983faee97f4b49ccbe105b4daf7a0&variables={{"id":"{username}","first":50{after}}}'
        r = requests.get(url, headers=headers, cookies=get_cookie()).json()

        feeds.extend(r["data"]["user"]["edge_owner_to_timeline_media"]["edges"])
        print(f"[+] Fetching {len(feeds)} feeds loaded.")

        end_cursor = r["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
        has_next_page = r["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
        if not has_next_page:
            break
    print(f"[!] Fetching done - {len(feeds)} feeds loaded.")
    return feeds


def main(username):
    user_id = get_userid(username)
    feeds = get_feed(user_id)
    output_path = username
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(input("[!] Press any key to continue."))

    for i in range(len(feeds)):
        feed = feeds[i]["node"]
        feed_url = f"https://www.instagram.com/p/{feed['shortcode']}"
        feed_text = feed["edge_media_to_caption"]["edges"][0]["node"]["text"] if feed["edge_media_to_caption"]["edges"] else ""
        str_id = feed["owner"]["username"]
        timestamp = feed["taken_at_timestamp"]
        dateTime = datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H.%M.%S")

        print(f"[*] Download feeds ({i+1}/{len(feeds)})")
        print(f" ㄴ {feed_url}")

        media_count = len(feed["edge_sidecar_to_children"]["edges"]) if "edge_sidecar_to_children" in feed else 1
        for media in range(0, media_count):
            media_array = feed["edge_sidecar_to_children"]["edges"][media]["node"] if "edge_sidecar_to_children" in feed else feed
            if media_array["is_video"]:
                media_path = f"{output_path}/{dateTime} {str_id} ({media+1}).mp4"
                media_url = media_array["video_url"]
                download(media_url, media_path)
                print(f" ㄴ {media_path}")
                print(f" ㄴ {media_url}")
            else:
                media_path = f"{output_path}/{dateTime} {str_id} ({media+1}).jpg"
                media_url = media_array["display_url"]
                download(media_url, media_path)
                print(f" ㄴ {media_path}")
                print(f" ㄴ {media_url}")
        if feed_text:
            with open(f"{output_path}/{dateTime} {str_id} (0).txt", "w", encoding="utf-8") as f:
                f.write(f"{str_id}: {feed_text}\n\n{feed_url}")


def mainone(url):
    output_path = "D:/라이브러리/다운로드"
    r = requests.get(f"{url}?__a=1", headers=headers, cookies=get_cookie())
    j = json.loads(r.text)
    feed = j["items"][0]
    feed_url = f"https://www.instagram.com/p/{feed['code']}"
    feed_text = feed["caption"]["text"] if feed["caption"] else None
    str_id = feed["user"]["username"]
    timestamp = feed["taken_at"]
    dateTime = datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H.%M.%S")
    print(f"[*] Download starting feed {url}")

    if "carousel_media" not in feed:
        media_url = feed["video_versions"][0]["url"] if feed["media_type"] == 2 else feed["image_versions2"]["candidates"][0]["url"]
        media_name = f"{output_path}/{dateTime} {str_id}.mp4" if feed["media_type"] == 2 else f"{output_path}/{dateTime} {str_id}.jpg"
        download(media_url, media_name)
        print(f" ㄴ {media_url}")
        print(f" ㄴ {media_name}")
    else:
        data = feed["carousel_media"]
        for i in range(0, len(data)):
            media_url = data[i]["video_versions"][0]["url"] if data[i]["media_type"] == 2 else data[i]["image_versions2"]["candidates"][0]["url"]
            media_name = f"{output_path}/{dateTime} {str_id} ({i+1}).mp4" if data[i]["media_type"] == 2 else f"{output_path}/{dateTime} {str_id} ({i+1}).jpg"
            download(media_url, media_name)
            print(f" ㄴ {media_url}")
            print(f" ㄴ {media_name}")

    if feed_text:
        with open(f"{output_path}/{dateTime} {str_id} (0).txt", "w", encoding="utf-8") as f:
            f.write(f"{str_id}: {feed_text}\n\n{feed_url}")


if __name__ == "__main__":
    username = input("Enter username: ")

    if "/p/" in username or "/tv/" in username or "/reel/" in username:
        mainone(username)
    else:
        main(username)

    print("[*] Writing Done.")
