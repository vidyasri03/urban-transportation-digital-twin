import networkx as nx


def compute_node_attributes(G):

    print("Assigning research-grade node capacities...")

    for node in G.nodes():

        # ---------------- CENTRALITIES ----------------
        degree = G.nodes[node].get(
            "degree_centrality", 0
        )

        betweenness = G.nodes[node].get(
            "betweenness_centrality", 0
        )

        eigenvector = G.nodes[node].get(
            "eigenvector_centrality", 0
        )

        # ---------------- CAPACITY MODEL ----------------
        # weighted importance score

        importance = (
            0.3 * degree +
            0.5 * betweenness +
            0.2 * eigenvector
        )

        # scale capacity
        capacity = 50 + (importance * 5000)

        # minimum protection
        capacity = max(capacity, 50)

        # ---------------- STORE ----------------
        G.nodes[node]["importance_score"] = importance

        G.nodes[node]["capacity"] = capacity

        G.nodes[node]["status"] = "active"

    print("Capacity assignment completed.")

    return G