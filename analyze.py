import json
import sys

import fire


def main(
    state: str = None, min_votes: int = 5_000, by_state: str = "yes", candidate: str = "Joe Biden"
):
    candidates = set()
    with open("output.json", "r") as in_f:
        data = json.load(in_f)
    candidate_by_state = {}
    for state_name, state_data in data.items():
        for county_name, county_data in state_data.items():
            num_votes = sum(county_data.values())

            if candidate not in county_data.keys() or num_votes == 0:
                continue

            candidate_votes = county_data[candidate]

            candidates = candidates.union(set(county_data.keys()))
            percent_candidate = county_data[candidate] / num_votes
            if num_votes >= min_votes:
                candidate_by_state[(state_name, county_name)] = {
                    "candidate_votes": candidate_votes,
                    "percent_candidate": percent_candidate,
                    "county": county_name,
                    "state": state_name,
                }

    candidate_by_state_sorted = sorted(
        candidate_by_state.items(), key=lambda x: x[1]["percent_candidate"], reverse=True
    )
    print("state,precinct,percent_candidate,candidate_votes")
    for i in candidate_by_state_sorted:
        if state is None or i[0][0] == state:
            print(
                ",".join(
                    [
                        str(x)
                        for x in [
                            i[0][0],
                            i[0][1],
                            round(100 * i[1]["percent_candidate"]),
                            i[1]["candidate_votes"],
                        ]
                    ]
                )
            )


if __name__ == "__main__":
    fire.Fire(main)
