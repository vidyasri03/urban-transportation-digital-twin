from collections import deque


def run_cascade(G, initial_failed_nodes, max_steps=10):

    failed_nodes = set(initial_failed_nodes)

    queue = deque(initial_failed_nodes)

    step = 0

    while queue and step < max_steps:

        current_failures = len(queue)

        for _ in range(current_failures):

            failed_node = queue.popleft()

            failed_load = G.nodes[failed_node].get(
                "load",
                0
            )

            neighbors = list(
                G.neighbors(failed_node)
            )

            active_neighbors = []

            # ---------------- ACTIVE NEIGHBORS ----------------
            for neighbor in neighbors:

                if G.nodes[neighbor].get(
                    "status"
                ) != "failed":

                    active_neighbors.append(
                        neighbor
                    )

            if not active_neighbors:
                continue

            # ---------------- IMPORTANCE-BASED REDISTRIBUTION ----------------
            total_importance = 0

            for neighbor in active_neighbors:

                total_importance += \
                    G.nodes[neighbor].get(
                        "importance_score",
                        1
                    )

            if total_importance == 0:
                continue

            # ---------------- REDISTRIBUTE LOAD ----------------
            for neighbor in active_neighbors:

                importance = \
                    G.nodes[neighbor].get(
                        "importance_score",
                        1
                    )

                share = (
                    importance /
                    total_importance
                )

                redistributed_load = \
                    failed_load * share

                G.nodes[neighbor]["load"] += \
                    redistributed_load

                # ---------------- FAILURE CHECK ----------------
                capacity = G.nodes[neighbor].get(
                    "capacity",
                    1
                )

                if (
                    G.nodes[neighbor]["load"]
                    >= capacity
                ):

                    if G.nodes[neighbor].get(
                        "status"
                    ) != "failed":

                        G.nodes[neighbor][
                            "status"
                        ] = "failed"

                        failed_nodes.add(
                            neighbor
                        )

                        queue.append(neighbor)

                # ---------------- CONGESTION ----------------
                elif (
                    G.nodes[neighbor]["load"]
                    >= 0.7 * capacity
                ):

                    G.nodes[neighbor][
                        "status"
                    ] = "congested"

        step += 1

    return G, failed_nodes