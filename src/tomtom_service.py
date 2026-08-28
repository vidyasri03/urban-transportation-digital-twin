import os
import requests

from dotenv import load_dotenv

load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")


def get_flow_data(lat, lon):
    """
    Fetch real-time traffic flow data
    from TomTom Flow Segment API
    """

    url = (
        "https://api.tomtom.com/traffic/services/4/"
        "flowSegmentData/absolute/10/json"
        f"?key={TOMTOM_API_KEY}"
        f"&point={lat},{lon}"
    )

    try:
        print("Latitude:", lat)
        print("Longitude:", lon)
        response = requests.get(url)

        data = response.json()

        if "flowSegmentData" not in data:

            print("TomTom Response:")
            print(data)

            return None

        flow = data["flowSegmentData"]

        current_speed = flow.get("currentSpeed", 0)
        free_flow_speed = flow.get("freeFlowSpeed", 1)

        # REAL congestion calculation
        congestion_ratio = 1 - (
            current_speed / free_flow_speed
        )

        congestion_ratio = max(0, min(congestion_ratio, 1))

        result = {
            "current_speed": current_speed,
            "free_flow_speed": free_flow_speed,
            "current_travel_time": flow.get(
                "currentTravelTime",
                0
            ),
            "free_flow_travel_time": flow.get(
                "freeFlowTravelTime",
                0
            ),
            "confidence": flow.get("confidence", 0),
            "road_closure": flow.get("roadClosure", False),
            "congestion_ratio": round(congestion_ratio, 2)
        }

        return result

    except Exception as e:

        print("TomTom API Error:", e)

        return None


def get_road_color(congestion_ratio, failed=False):
    """
    Realistic road color logic
    """

    if failed:
        return "#8B0000"  # dark red

    if congestion_ratio < 0.25:
        return "green"

    elif congestion_ratio < 0.50:
        return "yellow"

    elif congestion_ratio < 0.75:
        return "orange"

    else:
        return "red"