import numpy as np
import matplotlib.pyplot as plt
import os
import re
import seaborn as sns
from math import comb

reports_dir = 'reports/'
save_dir = 'images/'


def plot_message_field(field_type: str, label: str):
    direct_data = {}
    epidemic_data = {}

    for filename in os.listdir(reports_dir):
        if filename.endswith("_MessageStatsReport.txt"):
            with open(os.path.join(reports_dir, filename)) as f:
                content = f.read()
                match = re.search(r"_(\d+)_MessageStatsReport", filename)
                nodes = int(match.group(1)) if match else -1
                field_match = re.search(rf"{field_type}:\s+([0-9.]+)", content)
                if not field_match:
                    continue
                value = float(field_match.group(1))

                if "DirectDeliveryKEMRouter" in filename:
                    direct_data[nodes] = value
                elif "EpidemicKEMRouter" in filename:
                    epidemic_data[nodes] = value

    node_counts = sorted(set(direct_data.keys()) & set(epidemic_data.keys()))
    direct_vals = [direct_data[n] for n in node_counts]
    epidemic_vals = [epidemic_data[n] for n in node_counts]

    # Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=node_counts, y=direct_vals, marker='o', label='DirectDeliveryKEM', linewidth=2)
    sns.lineplot(x=node_counts, y=epidemic_vals, marker='s', label='EpidemicKEM', linewidth=2)

    plt.title(f"{label} Comparison")
    plt.xlabel("Number of Nodes")
    plt.ylabel(label)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save plot
    filename = f"{field_type}_comparison.png"
    plt.savefig(os.path.join(save_dir, filename))
    plt.show()