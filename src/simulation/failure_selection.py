import random

import networkx as nx


# ------------------------------------------------
# RANDOM SCATTERED FAILURE
# ------------------------------------------------
def random_failure(G, k):

    nodes = list(G.nodes())

    failed_nodes = random.sample(

        nodes,

        min(
            k,
            len(nodes)
        )
    )

    return failed_nodes


# ------------------------------------------------
# HIGH LOAD FAILURE
# ------------------------------------------------
def high_load_failure(G, k):

    nodes_sorted = sorted(

        G.nodes(),

        key=lambda n:
            G.nodes[n].get(
                "load",
                0
            ),

        reverse=True
    )

    return nodes_sorted[:k]


# ------------------------------------------------
# CLUSTERED CASCADING FAILURE
# ------------------------------------------------
def clustered_failure(

    G,

    k
):

    nodes = list(G.nodes())

    if len(nodes) == 0:

        return []

    # ----------------------------------------
    # START FROM RANDOM HUB
    # ----------------------------------------
    seed = random.choice(nodes)

    failed_nodes = set([seed])

    frontier = [seed]

    # ----------------------------------------
    # BFS-LIKE FAILURE SPREAD
    # ----------------------------------------
    while (

        len(failed_nodes) < k

        and

        frontier
    ):

        current = frontier.pop(0)

        neighbors = list(
            G.neighbors(current)
        )

        random.shuffle(neighbors)

        for neighbor in neighbors:

            if neighbor not in failed_nodes:

                failed_nodes.add(
                    neighbor
                )

                frontier.append(
                    neighbor
                )

            if len(failed_nodes) >= k:

                break

    return list(failed_nodes)


# ------------------------------------------------
# RESEARCH-GRADE TARGETED FAILURE
# ------------------------------------------------
def critical_node_failure(

    G,

    k
):

    scored_nodes = []

    for node in G.nodes():

        betweenness = G.nodes[node].get(

            "betweenness_centrality",

            0
        )

        eigenvector = G.nodes[node].get(

            "eigenvector_centrality",

            0
        )

        load = G.nodes[node].get(
            "load",
            0
        )

        capacity = G.nodes[node].get(

            "capacity",

            1
        )

        utilization = (

            load / capacity

            if capacity > 0

            else 0
        )

        # ----------------------------------------
        # CRITICALITY SCORE
        # ----------------------------------------
        criticality_score = (

            0.45 * betweenness +

            0.30 * eigenvector +

            0.25 * utilization
        )

        scored_nodes.append(

            (
                node,
                criticality_score
            )
        )

    # ----------------------------------------
    # SORT
    # ----------------------------------------
    scored_nodes.sort(

        key=lambda x: x[1],

        reverse=True
    )

    # ----------------------------------------
    # TAKE TOP HUB
    # ----------------------------------------
    if len(scored_nodes) == 0:

        return []

    seed_node = scored_nodes[0][0]

    # ----------------------------------------
    # EXPAND FAILURE AROUND HUB
    # ----------------------------------------
    failed_nodes = set([seed_node])

    frontier = [seed_node]

    while (

        len(failed_nodes) < k

        and

        frontier
    ):

        current = frontier.pop(0)

        neighbors = list(
            G.neighbors(current)
        )

        # prioritize important neighbors
        neighbors.sort(

            key=lambda n:
                G.nodes[n].get(
                    "importance_score",
                    0
                ),

            reverse=True
        )

        for neighbor in neighbors:

            if neighbor not in failed_nodes:

                failed_nodes.add(
                    neighbor
                )

                frontier.append(
                    neighbor
                )

            if len(failed_nodes) >= k:

                break

    return list(failed_nodes)