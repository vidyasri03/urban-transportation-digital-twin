import random
import networkx as nx

from src.load_network import (
    load_or_download_graph
)

from src.preprocessing.centrality import (
    compute_centrality_measures
)

from src.preprocessing.node_attributes import (
    compute_node_attributes
)

from src.preprocessing.dynamic_load import (
    apply_dynamic_load
)

from src.analysis.criticality import (
    compute_critical_nodes
)

from src.simulation.failure_selection import (

    random_failure,

    high_load_failure,

    critical_node_failure
)

from src.simulation.cascade import (
    run_cascade
)

from src.metrics.network_metrics import (
    compute_all_metrics
)

from src.recovery.strategies import (
    simulate_recovery_process
)


# ---------------------------------------------------
# GLOBAL STORAGE
# ---------------------------------------------------
G_BASE = None

LAST_FAILED_GRAPH = None

LAST_FAILED_NODES = None

LAST_ORIGINAL_NODE_COUNT = None

RECOVERY_RESULTS = {}

REPAIR_QUEUE = []


# ---------------------------------------------------
# INITIALIZE GRAPH
# ---------------------------------------------------
def initialize_graph():

    global G_BASE

    if G_BASE is None:

        print(
            "Loading transportation network..."
        )

        G_BASE = load_or_download_graph()

        # ----------------------------------------
        # LARGEST CONNECTED COMPONENT
        # ----------------------------------------
        largest_cc = max(

            nx.connected_components(
                nx.Graph(G_BASE)
            ),

            key=len
        )

        G_BASE = G_BASE.subgraph(
            largest_cc
        ).copy()

        # ----------------------------------------
        # OPTIONAL LIMIT
        # ----------------------------------------
        if len(G_BASE.nodes()) > 1500:

            selected_nodes = list(
                G_BASE.nodes()
            )[:1500]

            G_BASE = G_BASE.subgraph(
                selected_nodes
            ).copy()

            largest_cc = max(

                nx.connected_components(
                    nx.Graph(G_BASE)
                ),

                key=len
            )

            G_BASE = G_BASE.subgraph(
                largest_cc
            ).copy()

        # ----------------------------------------
        # PREPROCESSING
        # ----------------------------------------
        G_BASE = \
            compute_centrality_measures(
                G_BASE
            )

        G_BASE = \
            compute_node_attributes(
                G_BASE
            )

        print(
            "Graph initialization completed."
        )

    return G_BASE.copy()


# ---------------------------------------------------
# APPLY FAILURE
# ---------------------------------------------------
def apply_failure(

    G,

    failure_type,

    fail_ratio=random.uniform(
        0.02,
        0.07
    )
):

    node_count = len(
        G.nodes()
    )

    k = max(

        1,

        int(
            fail_ratio * node_count
        )
    )

    # ----------------------------------------
    # RANDOM FAILURE
    # ----------------------------------------
    if failure_type == "random":

        failed_nodes = \
            random_failure(
                G,
                k
            )

    # ----------------------------------------
    # HIGH LOAD FAILURE
    # ----------------------------------------
    elif failure_type == "high":

        failed_nodes = \
            high_load_failure(
                G,
                k
            )

    # ----------------------------------------
    # TARGETED ATTACK
    # ----------------------------------------
    elif failure_type == "critical":

        failed_nodes = \
            critical_node_failure(
                G,
                k
            )

    else:

        return set()

    # ----------------------------------------
    # APPLY FAILURES
    # ----------------------------------------
    for node in failed_nodes:

        G.nodes[node][
            "status"
        ] = "failed"

        G.nodes[node][
            "load"
        ] *= 1.5

    return set(
        failed_nodes
    )


# ---------------------------------------------------
# UPDATE STATUS
# ---------------------------------------------------
def update_status(G):

    for node in G.nodes():

        load = G.nodes[node].get(
            "load",
            0
        )

        capacity = G.nodes[node].get(
            "capacity",
            1
        )

        if load >= capacity:

            G.nodes[node][
                "status"
            ] = "failed"

        elif load >= 0.7 * capacity:

            G.nodes[node][
                "status"
            ] = "congested"

        else:

            if G.nodes[node].get(
                "status"
            ) != "failed":

                G.nodes[node][
                    "status"
                ] = "active"


# ---------------------------------------------------
# FAILURE SIMULATION
# ---------------------------------------------------
def run_simulation(

    failure_type=None,

    time_of_day="peak"
):

    global LAST_FAILED_GRAPH
    global LAST_FAILED_NODES
    global LAST_ORIGINAL_NODE_COUNT
    global RECOVERY_RESULTS

    # reset old recoveries
    RECOVERY_RESULTS = {}

    # ----------------------------------------
    # INITIALIZE GRAPH
    # ----------------------------------------
    G = initialize_graph()

    original_nodes = len(
        G.nodes()
    )

    # ----------------------------------------
    # APPLY DYNAMIC LOAD
    # ----------------------------------------
    G = apply_dynamic_load(

        G,

        time_of_day=time_of_day
    )

    failed_nodes = set()

    # ----------------------------------------
    # FAILURE + CASCADE
    # ----------------------------------------
    if failure_type != "none":

        failed_nodes = apply_failure(

            G,

            failure_type
        )

        G, failed_nodes = \
            run_cascade(

                G,

                failed_nodes
            )

    # ----------------------------------------
    # UPDATE STATUS
    # ----------------------------------------
    update_status(G)

    # ----------------------------------------
    # STORE CURRENT STATE
    # ----------------------------------------
    LAST_FAILED_GRAPH = G.copy()

    LAST_FAILED_NODES = \
        failed_nodes.copy()

    LAST_ORIGINAL_NODE_COUNT = \
        original_nodes

    # ----------------------------------------
    # ACTIVE GRAPH
    # ----------------------------------------
    active_nodes = []

    for node in G.nodes():

        status = G.nodes[node].get(
            "status",
            "active"
        )

        if status != "failed":

            active_nodes.append(node)

    G_metrics = G.subgraph(
        active_nodes
    ).copy()

    # ----------------------------------------
    # COMPUTE METRICS
    # ----------------------------------------
    metrics = compute_all_metrics(

        G_metrics,

        original_nodes
    )

    # ----------------------------------------
    # CRITICAL NODES
    # ----------------------------------------
    critical_nodes = \
        compute_critical_nodes(
            G
        )

    # ----------------------------------------
    # NODE DATA
    # ----------------------------------------
    node_data = []

    for node in G.nodes():

        if (
            "x" not in G.nodes[node]
            or
            "y" not in G.nodes[node]
        ):
            continue

        node_data.append({

            "id":
                str(node),

            "lat":
                float(
                    G.nodes[node]["y"]
                ),

            "lon":
                float(
                    G.nodes[node]["x"]
                ),

            "status":
                G.nodes[node]["status"],

            "load":
                float(
                    G.nodes[node]["load"]
                ),

            "capacity":
                float(
                    G.nodes[node]["capacity"]
                ),

            "importance":
                float(
                    G.nodes[node].get(
                        "importance_score",
                        0
                    )
                ),

            "betweenness":
                float(
                    G.nodes[node].get(
                        "betweenness_centrality",
                        0
                    )
                ),

            "eigenvector":
                float(
                    G.nodes[node].get(
                        "eigenvector_centrality",
                        0
                    )
                )
        })

    return {

        "nodes":
            node_data,

        "failed_nodes":
            list(failed_nodes),

        "critical_nodes":
            critical_nodes,

        "after_metrics":
            metrics,

        "resilience_score":
            metrics[
                "ResilienceScore"
            ]
    }


# ---------------------------------------------------
# RUN RECOVERY
# ---------------------------------------------------
def run_recovery(
    recovery_type
):

    global LAST_FAILED_GRAPH
    global LAST_FAILED_NODES
    global LAST_ORIGINAL_NODE_COUNT
    global RECOVERY_RESULTS

    if LAST_FAILED_GRAPH is None:

        return {

            "timeline": []
        }

    # ----------------------------------------
    # RUN RECOVERY
    # ----------------------------------------
    history = \
        simulate_recovery_process(

            LAST_FAILED_GRAPH.copy(),

            LAST_FAILED_NODES,

            recovery_type,

            LAST_ORIGINAL_NODE_COUNT
        )

    # ----------------------------------------
    # STORE RESULT
    # ----------------------------------------
    RECOVERY_RESULTS[
        recovery_type
    ] = history

    return {

        "timeline":
            history
    }


# ---------------------------------------------------
# COMPARE RECOVERY STRATEGIES
# ---------------------------------------------------
def compare_recovery_strategies():

    global RECOVERY_RESULTS

    if len(RECOVERY_RESULTS) == 0:

        return {

            "strategies": [],

            "best_strategy":
                None
        }

    comparison = []

    # ----------------------------------------
    # ANALYZE STRATEGIES
    # ----------------------------------------
    for strategy, history in \
        RECOVERY_RESULTS.items():

        if len(history) == 0:

            continue

        avg_resilience = sum(

            step["resilience"]

            for step in history

        ) / len(history)

        avg_connectivity = sum(

            1 - step["connectivity_loss"]

            for step in history

        ) / len(history)

        recovery_steps = len(history)

        final_resilience = \
            history[-1]["resilience"]

        # ------------------------------------
        # PERFORMANCE SCORE
        # ------------------------------------
        score = (

            0.45 * avg_resilience +

            0.30 * avg_connectivity * 100 +

            0.25 * (
                100 / recovery_steps
            )
        )

        comparison.append({

            "strategy":
                strategy,

            "avg_resilience":
                round(
                    avg_resilience,
                    2
                ),

            "avg_connectivity":
                round(
                    avg_connectivity * 100,
                    2
                ),

            "recovery_steps":
                recovery_steps,

            "final_resilience":
                round(
                    final_resilience,
                    2
                ),

            "score":
                round(
                    score,
                    2
                )
        })

    # ----------------------------------------
    # SORT BEST FIRST
    # ----------------------------------------
    comparison.sort(

        key=lambda x: x["score"],

        reverse=True
    )

    best = comparison[0]

    # ----------------------------------------
    # EXPLANATION
    # ----------------------------------------
    if best["strategy"] == "centrality":

        reason = (

            "Fastest backbone restoration "
            "and highest network resilience."
        )

    elif best["strategy"] == "load":

        reason = (

            "Reduced congestion efficiently "
            "during recovery."
        )

    else:

        reason = (

            "Handled localized disruptions "
            "adequately with simple recovery."
        )

    return {

        "strategies":
            comparison,

        "best_strategy":
            best["strategy"],

        "reason":
            reason
    }


# ---------------------------------------------------
# GENERATE REPAIR PRIORITY
# ---------------------------------------------------
def generate_repair_queue():

    global LAST_FAILED_GRAPH
    global LAST_FAILED_NODES
    global REPAIR_QUEUE

    if (
        LAST_FAILED_GRAPH is None
        or
        LAST_FAILED_NODES is None
    ):

        return []

    scored_nodes = []

    for node in LAST_FAILED_NODES:

        importance = \
            LAST_FAILED_GRAPH.nodes[node].get(
                "importance_score",
                0
            )

        load = \
            LAST_FAILED_GRAPH.nodes[node].get(
                "load",
                0
            )

        capacity = \
            LAST_FAILED_GRAPH.nodes[node].get(
                "capacity",
                1
            )

        utilization = (
            load / capacity
            if capacity > 0
            else 0
        )

        priority = (

            0.6 * importance +

            0.4 * utilization
        )

        scored_nodes.append({

            "node":
                str(node),

            "priority":
                round(
                    priority,
                    4
                ),

            "importance":
                round(
                    importance,
                    4
                ),

            "utilization":
                round(
                    utilization,
                    4
                )
        })

    scored_nodes.sort(

        key=lambda x: x["priority"],

        reverse=True
    )

    REPAIR_QUEUE = scored_nodes

    return scored_nodes


# ---------------------------------------------------
# GET LATEST NETWORK STATE
# ---------------------------------------------------
def get_latest_network_state():

    global LAST_FAILED_GRAPH

    if LAST_FAILED_GRAPH is None:

        return {

            "nodes": []
        }

    node_data = []

    for node in LAST_FAILED_GRAPH.nodes():

        if (
            "x" not in LAST_FAILED_GRAPH.nodes[node]
            or
            "y" not in LAST_FAILED_GRAPH.nodes[node]
        ):
            continue

        node_data.append({

            "id":
                str(node),

            "lat":
                float(
                    LAST_FAILED_GRAPH.nodes[node]["y"]
                ),

            "lon":
                float(
                    LAST_FAILED_GRAPH.nodes[node]["x"]
                ),

            "status":
                LAST_FAILED_GRAPH.nodes[node].get(
                    "status",
                    "active"
                ),

            "load":
                float(
                    LAST_FAILED_GRAPH.nodes[node].get(
                        "load",
                        0
                    )
                ),

            "capacity":
                float(
                    LAST_FAILED_GRAPH.nodes[node].get(
                        "capacity",
                        1
                    )
                )
        })

    return {

        "nodes":
            node_data
    }