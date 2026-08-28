import random

from src.metrics.network_metrics import (
    compute_all_metrics
)


# ---------------------------------------------------
# REPAIR SINGLE NODE
# ---------------------------------------------------
def repair_node(G, node):

    capacity = G.nodes[node].get(
        "capacity",
        1
    )

    # repaired node restored
    # with moderate utilization
    G.nodes[node]["load"] = \
        0.5 * capacity

    G.nodes[node]["status"] = \
        "active"


# ---------------------------------------------------
# RANDOM RECOVERY ORDER
# ---------------------------------------------------
def get_random_order(
    G,
    failed_nodes
):

    failed_nodes = list(
        failed_nodes
    )

    random.shuffle(
        failed_nodes
    )

    return failed_nodes


# ---------------------------------------------------
# LOAD-BASED RECOVERY ORDER
# ---------------------------------------------------
def get_load_based_order(
    G,
    failed_nodes
):

    failed_nodes = list(
        failed_nodes
    )

    failed_nodes.sort(

        key=lambda node:
            G.nodes[node].get(
                "load",
                0
            ),

        reverse=True
    )

    return failed_nodes


# ---------------------------------------------------
# CENTRALITY-BASED RECOVERY ORDER
# ---------------------------------------------------
def get_centrality_order(
    G,
    failed_nodes
):

    failed_nodes = list(
        failed_nodes
    )

    failed_nodes.sort(

        key=lambda node:
            G.nodes[node].get(
                "importance_score",
                0
            ),

        reverse=True
    )

    return failed_nodes


# ---------------------------------------------------
# UPDATE STATUS
# ---------------------------------------------------
def update_status(
    G,
    node
):

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

        G.nodes[node][
            "status"
        ] = "active"


# ---------------------------------------------------
# TIME-STEP RECOVERY SIMULATION
# ---------------------------------------------------
def simulate_recovery_process(

    G,

    failed_nodes,

    recovery_type,

    original_nodes
):

    # ----------------------------------------
    # STRATEGY-SPECIFIC REPAIR CAPACITY
    # ----------------------------------------
    if recovery_type == "random":

        step_size = 3

    elif recovery_type == "load":

        step_size = 5

    else:

        # centrality recovery
        step_size = 8

    # ----------------------------------------
    # COPY GRAPH
    # ----------------------------------------
    G_recovery = G.copy()

    # ----------------------------------------
    # FAILED SET
    # ----------------------------------------
    remaining_failed = set(
        failed_nodes
    )

    # ----------------------------------------
    # RECOVERY HISTORY
    # ----------------------------------------
    history = []

    step = 0

    # ----------------------------------------
    # RECOVERY LOOP
    # ----------------------------------------
    while remaining_failed:

        # ----------------------------------------
        # SELECT RECOVERY ORDER
        # ----------------------------------------
        if recovery_type == "random":

            recovery_order = \
                get_random_order(
                    G_recovery,
                    remaining_failed
                )

        elif recovery_type == "load":

            recovery_order = \
                get_load_based_order(
                    G_recovery,
                    remaining_failed
                )

        else:

            recovery_order = \
                get_centrality_order(
                    G_recovery,
                    remaining_failed
                )

        # ----------------------------------------
        # CURRENT RECOVERY BATCH
        # ----------------------------------------
        current_batch = recovery_order[
            :step_size
        ]

        # ----------------------------------------
        # REPAIR CURRENT STEP
        # ----------------------------------------
        for node in current_batch:

            repair_node(
                G_recovery,
                node
            )

            remaining_failed.discard(
                node
            )

        # ----------------------------------------
        # LOCALIZED STABILIZATION
        # ----------------------------------------
        for repaired_node in current_batch:

            neighbors = list(
                G_recovery.neighbors(
                    repaired_node
                )
            )

            for neighbor in neighbors:

                # skip failed nodes
                if G_recovery.nodes[
                    neighbor
                ].get(
                    "status"
                ) == "failed":

                    continue

                neighbor_load = \
                    G_recovery.nodes[
                        neighbor
                    ].get(
                        "load",
                        0
                    )

                # --------------------------------
                # STRATEGY-SPECIFIC STABILIZATION
                # --------------------------------
                if recovery_type == "random":

                    reduction_factor = 0.04

                elif recovery_type == "load":

                    reduction_factor = 0.08

                else:

                    # centrality recovery
                    reduction_factor = 0.14

                reduction = \
                    reduction_factor * neighbor_load

                # apply reduction
                G_recovery.nodes[
                    neighbor
                ]["load"] -= reduction

                # prevent negative load
                if G_recovery.nodes[
                    neighbor
                ]["load"] < 0:

                    G_recovery.nodes[
                        neighbor
                    ]["load"] = 0

                # --------------------------------
                # STATUS UPDATE
                # --------------------------------
                update_status(
                    G_recovery,
                    neighbor
                )

            # update repaired node
            update_status(
                G_recovery,
                repaired_node
            )

        # ----------------------------------------
        # CREATE TEMP METRICS GRAPH
        # ----------------------------------------
        G_metrics = G_recovery.copy()

        remove_nodes = []

        for node in G_metrics.nodes():

            if G_metrics.nodes[node].get(
                "status"
            ) == "failed":

                remove_nodes.append(
                    node
                )

        G_metrics.remove_nodes_from(
            remove_nodes
        )

        # ----------------------------------------
        # COMPUTE METRICS
        # ----------------------------------------
        metrics = compute_all_metrics(

            G_metrics,

            original_nodes
        )

        # ----------------------------------------
        # NODE SNAPSHOT
        # ----------------------------------------
        snapshot_nodes = []

        for node in G_recovery.nodes():

            if (
                "x" not in G_recovery.nodes[node]
                or
                "y" not in G_recovery.nodes[node]
            ):
                continue

            snapshot_nodes.append({

                "id":
                    str(node),

                "lat":
                    float(
                        G_recovery.nodes[node]["y"]
                    ),

                "lon":
                    float(
                        G_recovery.nodes[node]["x"]
                    ),

                "status":
                    G_recovery.nodes[node].get(
                        "status",
                        "active"
                    ),

                "load":
                    float(
                        G_recovery.nodes[node].get(
                            "load",
                            0
                        )
                    ),

                "capacity":
                    float(
                        G_recovery.nodes[node].get(
                            "capacity",
                            1
                        )
                    )
            })

        # ----------------------------------------
        # STORE HISTORY
        # ----------------------------------------
        history.append({

            "step":
                step,

            "remaining_failed":
                len(
                    remaining_failed
                ),

            "resilience":
                metrics[
                    "ResilienceScore"
                ],

            "efficiency":
                metrics[
                    "Efficiency"
                ],

            "connectivity_loss":
                metrics[
                    "ConnectivityLoss"
                ],

            "nodes":
                snapshot_nodes
        })

        step += 1

    return history