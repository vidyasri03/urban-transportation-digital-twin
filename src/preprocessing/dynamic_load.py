import random


def apply_dynamic_load(
    G,
    time_of_day="peak"
):

    print(
        f"Applying dynamic load: {time_of_day}"
    )

    # ---------------- TIME FACTOR ----------------
    if time_of_day == "peak":
        traffic_factor = 1.0

    elif time_of_day == "normal":
        traffic_factor = 0.7

    else:
        traffic_factor = 0.5

    # ---------------- LOAD ASSIGNMENT ----------------
    for node in G.nodes():

        capacity = G.nodes[node].get(
            "capacity",
            50
        )

        # ---------------- CENTRALITIES ----------------
        degree = G.nodes[node].get(
            "degree_centrality",
            0
        )

        betweenness = G.nodes[node].get(
            "betweenness_centrality",
            0
        )

        eigenvector = G.nodes[node].get(
            "eigenvector_centrality",
            0
        )

        # ---------------- TRAFFIC ATTRACTIVENESS ----------------
        attractiveness = (
            0.3 * degree +
            0.5 * betweenness +
            0.2 * eigenvector
        )

        # ---------------- BASE UTILIZATION ----------------
        base_utilization = \
            0.3 + (
                attractiveness * 2
            )

        # clamp
        base_utilization = min(
            base_utilization,
            0.85
        )

        # ---------------- RANDOM VARIATION ----------------
        variation = random.uniform(
            0.85,
            1.15
        )

        # ---------------- FINAL LOAD ----------------
        load = (
            capacity *
            base_utilization *
            traffic_factor *
            variation
        )

        G.nodes[node]["load"] = load

        # ---------------- STATUS ----------------
        if load >= capacity:

            G.nodes[node]["status"] = \
                "failed"

        elif load >= 0.7 * capacity:

            G.nodes[node]["status"] = \
                "congested"

        else:

            G.nodes[node]["status"] = \
                "active"

    print(
        "Dynamic load assignment completed."
    )

    return G