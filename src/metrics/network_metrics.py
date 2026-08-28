import networkx as nx


# ------------------------------------------------
# LARGEST CONNECTED COMPONENT
# ------------------------------------------------
def get_lcc_subgraph(G):

    if len(G.nodes()) == 0:

        return None

    G_simple = nx.Graph(G)

    largest_cc = max(

        nx.connected_components(
            G_simple
        ),

        key=len
    )

    return G_simple.subgraph(
        largest_cc
    ).copy()


# ------------------------------------------------
# LCC RATIO
# ------------------------------------------------
def compute_lcc_ratio(

    G,

    original_nodes
):

    if len(G.nodes()) == 0:

        return 0

    lcc_graph = get_lcc_subgraph(G)

    if lcc_graph is None:

        return 0

    return (

        len(lcc_graph.nodes())

        / original_nodes
    )


# ------------------------------------------------
# NETWORK EFFICIENCY
# ------------------------------------------------
def compute_efficiency(G):

    try:

        lcc_graph = get_lcc_subgraph(G)

        if (
            lcc_graph is None
            or
            len(lcc_graph.nodes()) < 2
        ):

            return 0

        # ----------------------------------------
        # AVERAGE SHORTEST PATH
        # ----------------------------------------
        avg_path = nx.average_shortest_path_length(
            lcc_graph
        )

        # ----------------------------------------
        # EFFICIENCY
        # smaller path = higher efficiency
        # ----------------------------------------
        efficiency = 1 / avg_path

        return efficiency

    except:

        return 0


# ------------------------------------------------
# CONNECTIVITY LOSS
# ------------------------------------------------
def compute_connectivity_loss(

    G,

    original_nodes
):

    lcc_ratio = compute_lcc_ratio(

        G,

        original_nodes
    )

    return 1 - lcc_ratio


# ------------------------------------------------
# RESILIENCE SCORE
# ------------------------------------------------
def compute_resilience_score(

    efficiency,

    connectivity_loss
):

    # ----------------------------------------
    # NORMALIZED EFFICIENCY
    # ----------------------------------------
    normalized_efficiency = min(

        1,

        efficiency * 10
    )

    resilience = (

        0.5 * normalized_efficiency +

        0.5 * (
            1 - connectivity_loss
        )
    )

    return resilience * 100


# ------------------------------------------------
# ALL METRICS
# ------------------------------------------------
def compute_all_metrics(

    G,

    original_nodes
):

    efficiency = compute_efficiency(
        G
    )

    connectivity_loss = \
        compute_connectivity_loss(

            G,

            original_nodes
        )

    lcc_ratio = compute_lcc_ratio(

        G,

        original_nodes
    )

    resilience = \
        compute_resilience_score(

            efficiency,

            connectivity_loss
        )

    return {

        "Efficiency":
            efficiency,

        "ConnectivityLoss":
            connectivity_loss,

        "LCC":
            lcc_ratio,

        "ResilienceScore":
            resilience
    }