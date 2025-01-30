import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from github import Github

# Load GitHub token from environment variables
 GH_PAT  = os.getenv(" GH_PAT ")
REPO_NAME = os.getenv("REPO_NAME")  # Example: "yourusername/exchange-rate-repo"

def get_euro_to_toman():
    url = "https://www.tgju.org/profile/price_eur"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"}).text.replace(",", "")
        return int(price) / 10  # Convert Rials to Tomans
    else:
        print("Failed to fetch data")
        return None

def update_json(rate):
    data = {"rate": rate, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    with open("exchange_rate.json", "w") as file:
        json.dump(data, file, indent=4)

def commit_to_github():
    g = Github( GH_PAT )
    repo = g.get_repo(REPO_NAME)
    
    with open("exchange_rate.json", "r") as file:
        content = file.read()
    
    try:
        contents = repo.get_contents("exchange_rate.json")
        repo.update_file(contents.path, "Update exchange rate", content, contents.sha)
    except:
        repo.create_file("exchange_rate.json", "Create exchange rate file", content)

if __name__ == "__main__":
    rate = get_euro_to_toman()
    if rate:
        update_json(rate)
        commit_to_github()
