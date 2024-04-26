import json

import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.m3net.jp/attendance/circle2024sR.php"

def main():
    try:
        res = requests.get(TARGET_URL)
        res.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestExceptiona as e:
        print(f"Request error occurred: {e}")
    

    else:
        try:
            data = BeautifulSoup(res.text, "html.parser")
            # サークルの情報を取得
            booth_texts = [t.text.replace("\t","") for t in data.find_all('td', class_="left")]
            circle_name_texts = [t.text.split("http")[0].replace("\t","") for t in data.find_all('td', class_="center")]
            circle_describe_texts = [t.text.replace("\t","") for t in data.find_all('td', class_="right")]
            circle_urls = []
            for t in data.find_all('td', class_="center"):
                try:
                    url_part = "http" + t.text.split("http")[1].replace("\t", "")
                    circle_urls.append(url_part)
                except IndexError:
                    circle_urls.append("")
            # jsonで書き出し
            keys = ['booth', 'name', 'detail', 'url']
            list_of_dicts = [{keys[0]: v1, keys[1]: v2, keys[2]:v3, keys[3]:v4} for v1, v2, v3, v4 in zip(booth_texts, circle_name_texts, circle_describe_texts, circle_urls)]
            with open('data.jsonl', 'w') as jsonl_file:
                for item in list_of_dicts:
                    jsonl_file.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            print(f"Data Scraping Completed.")
        except Exception as e:
            print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
