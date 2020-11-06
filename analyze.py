import json
import fire


def main(state: str = None, min_votes: int = 5_000):
    with open("output.json", "r") as in_f:
        data = json.load(in_f)
    choice_state = {}
    dem_by_state = {}
    for state_name, state_data in data.items():
        max_percent_dem = 0
        max_county = ""
        max_state = ""
        dem_votes = 0
        max_dem_votes = 0
        for county_name, county_data in state_data.items():
            num_votes = sum(county_data.values())
            dem_votes = county_data["Joe Biden"]
            if num_votes == 0:
                continue
            percent_dem = county_data["Joe Biden"] / num_votes
            if percent_dem > max_percent_dem and num_votes >= min_votes:
                max_county_data = county_data
                max_dem_votes = dem_votes
                max_percent_dem = percent_dem
                max_county = county_name
            if state is not None and state_name == state:
                choice_state[county_name] = {
                    "percent_dem": percent_dem,
                    "county_name": county_name,
                    "dem_votes": dem_votes,
                }
        dem_by_state[state_name] = {
            "max_dem_votes": max_dem_votes,
            "max_percent_dem": max_percent_dem,
            "max_county": max_county,
        }

    if state is not None:
        choice_state_sorted = sorted(
            choice_state.items(), key=lambda x: x[1]["percent_dem"], reverse=True
        )
        for i in choice_state_sorted:
            print(
                f"{i[0]}: percent_dem - {round(i[1]['percent_dem'] * 100)}%, county - {i[1]['county_name']}"
            )
    else:
        sorted_states = sorted(
            dem_by_state.items(), key=lambda x: x[1]["max_percent_dem"], reverse=True
        )
        for i in sorted_states:
            print(
                f"{i[0]}: percent_dem - {round(i[1]['max_percent_dem'] * 100)}%, county - {i[1]['max_county']}"
            )


if __name__ == "__main__":
    fire.Fire(main)
