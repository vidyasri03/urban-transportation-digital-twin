import networkx as nx


# ---------------------------------------------------
# DYNAMIC TRAFFIC ASSIGNMENT
# ---------------------------------------------------
def recompute_network_loads(G):

    # ----------------------------------------
    # RESET LOADS
    # ----------------------------------------
    for node in G.nodes():

        if G.nodes[node].get(
            "status"
        ) != "failed":

            G.nodes[node]["load"] = 0


    # ----------------------------------------
    # ACTIVE NODES ONLY
    # ----------------------------------------
    active_nodes = [

        node for node in G.nodes()

        if G.nodes[node].get(
            "status"
        ) != "failed"
    ]


    # limit for performance
    sampled_nodes = active_nodes[:200]


    # ----------------------------------------
    # SHORTEST PATH TRAFFIC FLOW
    # ----------------------------------------
    for source in sampled_nodes:

        for target in sampled_nodes:

            if source == target:
                continue

            try:

                path = nx.shortest_path(

                    G,

                    source=source,

                    target=target
                )

                # --------------------------------
                # TRAFFIC CONTRIBUTION
                # --------------------------------
                for node in path:

                    if G.nodes[node].get(
                        "status"
                    ) == "failed":

                        continue

                    G.nodes[node]["load"] += 1

            except:
                continue


    # ----------------------------------------
    # NORMALIZE LOADS
    # ----------------------------------------
    max_load = max(

        G.nodes[node]["load"]

        for node in active_nodes
    )


    if max_load == 0:
        max_load = 1


    for node in active_nodes:

        capacity = G.nodes[node].get(
            "capacity",
            1
        )

        normalized = \
            G.nodes[node]["load"] / max_load

        G.nodes[node]["load"] = \
            normalized * capacity


    # ----------------------------------------
    # UPDATE STATUS
    # ----------------------------------------
    for node in active_nodes:

        load = G.nodes[node]["load"]

        capacity = G.nodes[node]["capacity"]

        if load >= capacity:

            G.nodes[node]["status"] = \
                "failed"

        elif load >= 0.7 * capacity:

            G.nodes[node]["status"] = \
                "congested"

        else:

            G.nodes[node]["status"] = \
                "active"


    return G