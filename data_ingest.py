import requests
import pandas as pd
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

api_key = os.getenv("FOOTBALL_DATA_API_KEY")
HEADERS = {'X-Auth-Token': api_key}
BASE_URL = "https://api.football-data.org/v4/"
EPL_CODE = config["league"]


def fetch_matches(season = "2023"):
    url = f"{BASE_URL}competitions/{EPL_CODE}/matches?season={season}"
    
    while url:
        response = requests.get(url, headers = HEADERS)
        data = response.json()

        matches = []
        for match in data.get("matches", []):
            matches.append({
                "match_id": match["id"],
                "utc_date": match["utcDate"],
                "matchday": match["matchday"],
                "home_team": match["homeTeam"]["name"],
                "away_team": match["awayTeam"]["name"],
                "home_score": match["score"]["fullTime"]["home"],
                "away_score": match["score"]["fullTime"]["away"],
                "status": match["status"]
            })
        links = response.headers.get("Link", "")
        next_url = None
        for link in links.split(","):
            if 'rel="next"' in link:
                next_url = link[link.find("<")+1 : link.find(">")]
                break
        url = next_url
    
    df = pd.DataFrame(matches)
    print(f"Total matches fetched: {len(df)}")
    return df
                                     

def save_data(df, filename = "epl_matches.csv"):
    os.makedirs("data", exist_ok = True)
    df.to_csv(f"data/{filename}", index = False)

if __name__ == "__main__":
    df_24 = fetch_matches(season = "2024")
    df_23 = fetch_matches(season = "2023")
    df = pd.concat([df_24, df_23])
    df.sort_values(by = "utc_date", inplace = True)
    df.reset_index(drop = True, inplace = True)
    save_data(df)
    print("Data saved successfully")