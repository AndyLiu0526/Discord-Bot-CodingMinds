import requests

def get_response(user_input: str) -> str:
    raise NotImplementedError("Code is missing.")

team_number = input("Input team number: ")

robotevents_params = {
    "bearerAuth": ROBOTEVENTS_TOKEN,
    "number": team_number
}
robotevents_teams_result = requests.get("https://www.robotevents.com/api/v2/teams", headers={"Authorization": f"Bearer {ROBOTEVENTS_TOKEN}"}, params=robotevents_params)
robotevents_teams_response = robotevents_teams_result.json()

team_id = robotevents_teams_response["data"][0]["id"]

robotevents_events_result = requests.get(f"https://www.robotevents.com/api/v2/teams/{team_id}/events", headers={"Authorization": f"Bearer {ROBOTEVENTS_TOKEN}"})
robotevents_events_response = robotevents_events_result.json()

number_of_competitions = robotevents_events_response["meta"]["total"]
for i in range(number_of_competitions):
    event_name = robotevents_events_response["data"][i]["name"]
    start_time = robotevents_events_response["data"][i]["start"]
    end_time = robotevents_events_response["data"][i]["end"]
    venue = robotevents_events_response["data"][i]["location"]["venue"]
    address = robotevents_events_response["data"][i]["location"]["address_1"]
    
    i+=1
    