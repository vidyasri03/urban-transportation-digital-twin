import os
import osmnx as ox
from src.config import CITY_NAME, NETWORK_TYPE, SIMPLIFY, SAVE_GRAPH_PATH


def load_or_download_graph():
    if os.path.exists(SAVE_GRAPH_PATH):
        print("Loading saved graph...")
        G = ox.load_graphml(SAVE_GRAPH_PATH)
    else:
        print("Downloading graph from OSM...")
        G = ox.graph_from_place(
            CITY_NAME,
            network_type=NETWORK_TYPE,
            simplify=SIMPLIFY
        )

        print("Saving graph...")
        os.makedirs("data", exist_ok=True)
        ox.save_graphml(G, SAVE_GRAPH_PATH)

    return G


def print_graph_info(G):
    print("\n--- Graph Info ---")
    print("Nodes:", len(G.nodes))
    print("Edges:", len(G.edges))
    print("Directed:", G.is_directed())