import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO

import requests
from PIL import Image
from io import BytesIO

def display_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.show()

# 表示したい画像のURLを指定
# image_url = "https://example.com/image.jpg"

# # 関数を呼び出して画像を表示
# display_image_from_url(image_url)

def get_month_link(month):
    # 月ごとのリンクを持つディクショナリを作成
    month_links = {
        "1": "https://lovegreen.net/languageofflower2/p36245/",
        "2": "https://lovegreen.net/languageofflower2/p36253/",
        "3": "https://lovegreen.net/languageofflower2/p36279/",
        "4": "https://lovegreen.net/languageofflower2/p36289/",
        "5": "https://lovegreen.net/languageofflower2/p36352/",
        "6": "https://lovegreen.net/languageofflower2/p34975/",
        "7": "https://lovegreen.net/languageofflower2/p35088/",
        "8": "https://lovegreen.net/languageofflower2/p36231/",
        "9": "https://lovegreen.net/languageofflower2/p36368/",
        "10": "https://lovegreen.net/languageofflower2/p36369/",
        "11": "https://lovegreen.net/languageofflower2/p36370/",
        "12": "https://lovegreen.net/languageofflower2/p36371/",
    }

    # 指定された月のリンクを返す
    return month_links.get(str(month))

def get_day_link(month_link, day):
    # 指定された月のページを取得
    response = requests.get(month_link)
    if response.status_code == 200:
        # HTMLをパース
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 日付のリンクを取得
        day_link = soup.find("a", text=str(day))
        if day_link:
            return urljoin(month_link, day_link.get("href"))
        else:
            print("指定された日のリンクが見つかりませんでした。")
            return None
    else:
        print("ページにアクセスできませんでした。")
        return None

def scrape_day_page(month, day):
    # 指定された月のリンクを取得
    month_link = get_month_link(month)
    if not month_link:
        print("指定された月のリンクが見つかりませんでした。")
        return

    # 指定された日のリンクを取得
    day_link = get_day_link(month_link, day)
    if not day_link:
        return

    # 日のページの内容を取得
    response = requests.get(day_link)
    if response.status_code == 200:
        # HTMLをパース
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # "_月_日の誕生花は"で始まる文章を抽出する
        target_text = f"{month}月{day}日の誕生花は"
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            if p.text.startswith(target_text):
                print(p.text)
                # 対象の文章に含まれるclass="thumbnail"の要素を取得する
                thumbnail = p.find_next(class_="thumbnail")
                if thumbnail:
                    thumbnail_style = thumbnail.get("style")
                    # print("Thumbnail Style:", thumbnail_style)
                    h_n = thumbnail_style.find("https://")
                    thumbnail_style = thumbnail_style[h_n:-2]
                    # print(thumbnail_style)
                    # display_image_from_url(thumbnail_style)
                    return thumbnail_style
                else:
                    print("thumbnailが見つかりませんでした。")
                break  # 該当する文章が見つかったらループを抜ける
    else:
        print("ページにアクセスできませんでした。")
        
# 例として_月_日のページをスクレイプする
scrape_day_page(4,26)