def compute_critical_nodes(G, top_k=10):

    critical_nodes = []

    for node in G.nodes():

        # ---------------- CENTRALITIES ----------------
        betweenness = G.nodes[node].get(
            "betweenness_centrality", 0
        )

        eigenvector = G.nodes[node].get(
            "eigenvector_centrality", 0
        )

        # ---------------- LOAD UTILIZATION ----------------
        load = G.nodes[node].get("load", 0)

        capacity = G.nodes[node].get("capacity", 1)

        utilization = load / capacity if capacity > 0 else 0

        # ---------------- CRITICALITY SCORE ----------------
        criticality_score = (
            0.4 * betweenness +
            0.3 * eigenvector +
            0.3 * utilization
        )

        critical_nodes.append({
            "id": str(node),

            "criticality_score": criticality_score,

            "betweenness": betweenness,

            "eigenvector": eigenvector,

            "utilization": utilization,

            "load": load,

            "capacity": capacity,

            "status": G.nodes[node].get(
                "status",
                "active"
            )
        })

    # ---------------- SORT ----------------
    critical_nodes = sorted(
        critical_nodes,
        key=lambda x: x["criticality_score"],
        reverse=True
    )

    return critical_nodes[:top_k]