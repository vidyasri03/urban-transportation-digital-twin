import sys
import os
import copy

# Fix import path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.load_network import load_or_download_graph, print_graph_info
from src.preprocessing.node_attributes import compute_node_attributes
from src.preprocessing.dynamic_load import apply_dynamic_load

from src.simulation.failure_selection import critical_node_failure
from src.simulation.cascade import run_cascade

from src.metrics.network_metrics import compute_all_metrics

from src.recovery.strategies import (
    random_repair,
    high_load_repair,
    critical_node_repair
)


# -------------------------------
# PRINT METRICS
# -------------------------------
def print_metrics(title, metrics):
    print(f"\n--- {title} ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")


# -------------------------------
# RESILIENCE INDEX
# -------------------------------
def resilience_index(metrics, original_lcc):
    lcc_ratio = metrics["LCC"] / original_lcc if original_lcc else 0
    efficiency = metrics["Efficiency"]
    loss = metrics["ConnectivityLoss"]

    return round(
        (0.4 * efficiency) +
        (0.4 * lcc_ratio) +
        (0.2 * (1 - loss)),
        4
    )


# -------------------------------
# MAIN
# -------------------------------
def main():
    print("\n===== DIGITAL TWIN SIMULATION START =====\n")

    # STEP 1: Load graph
    G = load_or_download_graph()
    print_graph_info(G)

    # STEP 2: Assign attributes
    G = compute_node_attributes(G)

    # STEP 2.1: Dynamic load
    G = apply_dynamic_load(G, time_of_day="peak")

    original_nodes = len(G.nodes())

    # -------------------------------
    # BEFORE FAILURE
    # -------------------------------
    before_metrics = compute_all_metrics(G, original_nodes)
    print_metrics("BEFORE FAILURE", before_metrics)

    original_lcc = before_metrics["LCC"]

    # -------------------------------
    # STEP 3: FAILURE + CASCADE
    # -------------------------------
    initial_nodes = critical_node_failure(G, k=1)
    print("\nInitial Failed Node:", initial_nodes)

    G, failed_nodes = run_cascade(G, initial_nodes)

    # -------------------------------
    # AFTER CASCADE
    # -------------------------------
    after_metrics = compute_all_metrics(G, original_nodes)
    print_metrics("AFTER CASCADE", after_metrics)

    print("\nTotal Failed Nodes:", len(failed_nodes))

    # -------------------------------
    # STEP 5: RECOVERY
    # -------------------------------
    print("\n===== RECOVERY PHASE =====")

    G_cascade = copy.deepcopy(G)

    # 1. RANDOM REPAIR
    G_random = copy.deepcopy(G_cascade)
    G_random = random_repair(G_random, failed_nodes, k=150)
    random_metrics = compute_all_metrics(G_random, original_nodes)
    print_metrics("AFTER RANDOM REPAIR", random_metrics)

    # 2. HIGH LOAD REPAIR
    G_high = copy.deepcopy(G_cascade)
    G_high = high_load_repair(G_high, failed_nodes, k=10)
    high_metrics = compute_all_metrics(G_high, original_nodes)
    print_metrics("AFTER HIGH LOAD REPAIR", high_metrics)

    # 3. CRITICAL NODE REPAIR
    G_critical = copy.deepcopy(G_cascade)
    G_critical = critical_node_repair(G_critical, failed_nodes, k=10)
    critical_metrics = compute_all_metrics(G_critical, original_nodes)
    print_metrics("AFTER CRITICAL NODE REPAIR", critical_metrics)

    # -------------------------------
    # RESILIENCE COMPARISON
    # -------------------------------
    print("\n===== RESILIENCE SCORES =====")

    print("Random Repair:",
          resilience_index(random_metrics, original_lcc))

    print("High Load Repair:",
          resilience_index(high_metrics, original_lcc))

    print("Critical Node Repair:",
          resilience_index(critical_metrics, original_lcc))

    print("\n===== SIMULATION END =====\n")


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()