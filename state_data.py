# first run this:
#   pip install requests==2.22.0 beautifulsoup4==4.8.1

import requests
from bs4 import BeautifulSoup
import json
import fire

links = [
    {"name": "Alabama", "route": "/elections/election-results/alabama-2020"},
    {"name": "Alaska", "route": "/elections/election-results/alaska-2020"},
    {"name": "Arizona", "route": "/elections/election-results/arizona-2020"},
    {"name": "Arkansas", "route": "/elections/election-results/arkansas-2020"},
    {"name": "California", "route": "/elections/election-results/california-2020"},
    {"name": "Colorado", "route": "/elections/election-results/colorado-2020"},
    {"name": "Connecticut", "route": "/elections/election-results/connecticut-2020"},
    {"name": "Delaware", "route": "/elections/election-results/delaware-2020"},
    {
        "name": "District of Columbia",
        "route": "/elections/election-results/district-of-columbia-2020",
    },
    {"name": "Florida", "route": "/elections/election-results/florida-2020"},
    {"name": "Georgia", "route": "/elections/election-results/georgia-2020"},
    {"name": "Hawaii", "route": "/elections/election-results/hawaii-2020"},
    {"name": "Idaho", "route": "/elections/election-results/idaho-2020"},
    {"name": "Illinois", "route": "/elections/election-results/illinois-2020"},
    {"name": "Indiana", "route": "/elections/election-results/indiana-2020"},
    {"name": "Iowa", "route": "/elections/election-results/iowa-2020"},
    {"name": "Kansas", "route": "/elections/election-results/kansas-2020"},
    {"name": "Kentucky", "route": "/elections/election-results/kentucky-2020"},
    {"name": "Louisiana", "route": "/elections/election-results/louisiana-2020"},
    {"name": "Maine", "route": "/elections/election-results/maine-2020"},
    {"name": "Maryland", "route": "/elections/election-results/maryland-2020"},
    {"name": "Massachusetts", "route": "/elections/election-results/massachusetts-2020"},
    {"name": "Michigan", "route": "/elections/election-results/michigan-2020"},
    {"name": "Minnesota", "route": "/elections/election-results/minnesota-2020"},
    {"name": "Mississippi", "route": "/elections/election-results/mississippi-2020"},
    {"name": "Missouri", "route": "/elections/election-results/missouri-2020"},
    {"name": "Montana", "route": "/elections/election-results/montana-2020"},
    {"name": "Nebraska", "route": "/elections/election-results/nebraska-2020"},
    {"name": "Nevada", "route": "/elections/election-results/nevada-2020"},
    {"name": "New Hampshire", "route": "/elections/election-results/new-hampshire-2020"},
    {"name": "New Jersey", "route": "/elections/election-results/new-jersey-2020"},
    {"name": "New Mexico", "route": "/elections/election-results/new-mexico-2020"},
    {"name": "New York", "route": "/elections/election-results/new-york-2020"},
    {"name": "North Carolina", "route": "/elections/election-results/north-carolina-2020"},
    {"name": "North Dakota", "route": "/elections/election-results/north-dakota-2020"},
    {"name": "Ohio", "route": "/elections/election-results/ohio-2020"},
    {"name": "Oklahoma", "route": "/elections/election-results/oklahoma-2020"},
    {"name": "Oregon", "route": "/elections/election-results/oregon-2020"},
    {"name": "Pennsylvania", "route": "/elections/election-results/pennsylvania-2020"},
    {"name": "Rhode Island", "route": "/elections/election-results/rhode-island-2020"},
    {"name": "South Carolina", "route": "/elections/election-results/south-carolina-2020"},
    {"name": "South Dakota", "route": "/elections/election-results/south-dakota-2020"},
    {"name": "Tennessee", "route": "/elections/election-results/tennessee-2020"},
    {"name": "Texas", "route": "/elections/election-results/texas-2020"},
    {"name": "Utah", "route": "/elections/election-results/utah-2020"},
    {"name": "Vermont", "route": "/elections/election-results/vermont-2020"},
    {"name": "Virginia", "route": "/elections/election-results/virginia-2020"},
    {"name": "Washington", "route": "/elections/election-results/washington-2020"},
    {"name": "West Virginia", "route": "/elections/election-results/west-virginia-2020"},
    {"name": "Wisconsin", "route": "/elections/election-results/wisconsin-2020"},
    {"name": "Wyoming", "route": "/elections/election-results/wyoming-2020"},
]


def main(limit: int = 1):
    for index, state_dict in enumerate(links):
        state_name = state_dict["name"]
        url = f"https://www.washingtonpost.com/{state_dict['route']}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "html.parser")
        state_data = json.loads(soup.find(id="__NEXT_DATA__").text)
        precinct_subunits = {}
        presidential_race_id = None
        county_votes = {}
        candidate_map = {}
        for race in state_data["props"]["pageProps"]["config"]["races"]:
            if "President general" in race["name"]:
                presidential_race_id = race["id"]
                candidate_map = {x["id"]: x for x in race["candidates"]}
                precinct_subunits = {x["id"]: {"name": x["name"]} for x in race["map"]["subunits"]}
        for subunit_id, subunit in state_data["props"]["pageProps"]["results"][
            presidential_race_id
        ]["subunits"].items():
            counts_by_candidate = {}
            for candidate_id, count in subunit["counts"].items():
                counts_by_candidate[candidate_map[candidate_id]["name"]] = count
                county_votes[precinct_subunits[subunit_id]["name"]] = counts_by_candidate
        print(county_votes)
        if index + 1 >= limit:
            return


if __name__ == "__main__":
    fire.Fire(main)
