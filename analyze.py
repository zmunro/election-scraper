import json
import sys

import fire


def main(
    state: str = None, min_votes: int = 5_000, by_state: str = "no", candidate: str = "Joe Biden"
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
    if by_state == "yes":
        seen_states = set()
        for i in candidate_by_state_sorted:
            round_perc = round(i[1]["percent_candidate"], 3)
            data_points = [i[0][0], i[0][1], round_perc, i[1]["candidate_votes"]]
            state_name = i[0][0]
            if state_name not in seen_states:
                seen_states.add(state_name)
                print(",".join([str(x) for x in data_points]))

    for i in candidate_by_state_sorted:
        round_perc = round(i[1]["percent_candidate"], 3)
        data_points = [i[0][0], i[0][1], round_perc, i[1]["candidate_votes"]]
        if state is None or i[0][0] == state:
            print(",".join([str(x) for x in data_points]))


if __name__ == "__main__":
    fire.Fire(main)
