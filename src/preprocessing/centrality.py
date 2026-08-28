import networkx as nx


def compute_centrality_measures(G):

    print("Computing centrality measures...")

    # ------------------------------------------------
    # CONVERT GRAPH
    # ------------------------------------------------
    # eigenvector centrality does not work
    # directly on MultiDiGraph

    G_simple = nx.Graph(G)

    # ---------------- DEGREE ----------------
    degree = nx.degree_centrality(
        G_simple
    )

    # ---------------- BETWEENNESS ----------------
    betweenness = nx.betweenness_centrality(
        G_simple,
        normalized=True
    )

    # ---------------- EIGENVECTOR ----------------
    eigenvector = nx.eigenvector_centrality(
        G_simple,
        max_iter=1000
    )

    # ---------------- STORE ----------------
    for node in G.nodes():

        G.nodes[node]["degree_centrality"] = \
            degree.get(node, 0)

        G.nodes[node]["betweenness_centrality"] = \
            betweenness.get(node, 0)

        G.nodes[node]["eigenvector_centrality"] = \
            eigenvector.get(node, 0)

    print("Centrality computation completed.")

    return G