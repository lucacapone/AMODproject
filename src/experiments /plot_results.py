import os
import csv
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 14})  # font grande per relazione


def extract_size(instance_name):
    """ Estrae la dimensione (numero nodi) dal nome dell'istanza. """
    return int(''.join(filter(str.isdigit, instance_name)))


def load_results(csv_path="results/output.csv"):
    instances = []
    greedy_costs = []
    two_opt_costs = []
    sa_costs = []
    improv_2opt = []
    improv_sa = []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            instances.append(row["instance"])
            greedy_costs.append(float(row["greedy_cost"]))
            two_opt_costs.append(float(row["two_opt_cost"]))
            sa_costs.append(float(row["sa_cost"]))
            improv_2opt.append(float(row["improvement_2opt"]))
            improv_sa.append(float(row["improvement_sa"]))

    # ordina per dimensione dell'istanza
    sizes = [extract_size(i) for i in instances]
    order = sorted(range(len(instances)), key=lambda i: sizes[i])

    instances = [instances[i] for i in order]
    greedy_costs = [greedy_costs[i] for i in order]
    two_opt_costs = [two_opt_costs[i] for i in order]
    sa_costs = [sa_costs[i] for i in order]
    improv_2opt = [improv_2opt[i] for i in order]
    improv_sa = [improv_sa[i] for i in order]

    return instances, greedy_costs, two_opt_costs, sa_costs, improv_2opt, improv_sa


def add_labels(x_positions, values):
    """Aggiunge etichette sopra le barre."""
    for x, val in zip(x_positions, values):
        plt.text(x, val + val * 0.01, f"{val:.1f}", ha='center')

def add_labels_bottom(x_positions, values, fontsize=10):
    """
    Aggiunge etichette verticali dalla base della barra.
    """
    for x, val in zip(x_positions, values):
        plt.text(
            x,
            val * 0.02,      # vicino allo zero (base)
            f"{val:.0f}",
            ha='center',
            va='bottom',
            fontsize=fontsize,
            rotation=90      # <<< TESTO VERTICALE
        )



def plot_costs(instances, greedy, two_opt, sa, output_folder="results/figures"):
    os.makedirs(output_folder, exist_ok=True)

    x = range(len(instances))

    plt.figure(figsize=(12, 6))
    width = 0.25

    # disegna barre
    pos_g = [i - width for i in x]
    pos_2 = list(x)
    pos_sa = [i + width for i in x]

    plt.bar(pos_g, greedy, width=width, label="Greedy")
    plt.bar(pos_2, two_opt, width=width, label="2-opt")
    plt.bar(pos_sa, sa, width=width, label="SA")

    # aggiungi valori numerici
    add_labels_bottom(pos_g, greedy)
    add_labels_bottom(pos_2, two_opt)
    add_labels_bottom(pos_sa, sa)

    plt.xticks(list(x), instances, rotation=45)
    plt.ylabel("Costo tour")
    plt.title("Confronto costi: Greedy vs 2-opt vs SA")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(output_folder, "confronto_costi.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvato grafico costi in: {out_path}")


def plot_improvements(instances, improv_2opt, improv_sa, greedy, output_folder="results/figures"):
    os.makedirs(output_folder, exist_ok=True)

    perc_2opt = [100 * (imp / g) for imp, g in zip(improv_2opt, greedy)]
    perc_sa = [100 * (imp / g) for imp, g in zip(improv_sa, greedy)]

    x = range(len(instances))
    width = 0.25

    plt.figure(figsize=(12, 6))

    pos_2 = [i - width/2 for i in x]
    pos_sa = [i + width/2 for i in x]

    plt.bar(pos_2, perc_2opt, width=width, label="2-opt vs Greedy")
    plt.bar(pos_sa, perc_sa, width=width, label="SA vs Greedy")

    # numeri sopra barre
    add_labels(pos_2, perc_2opt)
    add_labels(pos_sa, perc_sa)

    plt.xticks(list(x), instances, rotation=45)
    plt.ylabel("Miglioramento [%] rispetto a Greedy")
    plt.title("Miglioramento percentuale: 2-opt e SA")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(output_folder, "miglioramento_percentuale.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvato grafico miglioramento in: {out_path}")

def plot_absolute_reduction(instances, greedy, sa, output_folder="results/figures"):
    """
    Plotta la riduzione assoluta del costo ottenuta da SA rispetto a Greedy.
    """
    os.makedirs(output_folder, exist_ok=True)

    reduction = [g - s for g, s in zip(greedy, sa)]

    x = range(len(instances))

    plt.figure(figsize=(12, 6))
    plt.bar(x, reduction, color="purple", alpha=0.8)

    # Etichette numeriche sopra le barre
    for i, val in enumerate(reduction):
        plt.text(i, val + val * 0.01, f"{val:.1f}", ha="center")

    plt.xticks(x, instances, rotation=45)
    plt.ylabel("Riduzione assoluta del costo")
    plt.title("Riduzione del costo: Greedy → SA")
    plt.tight_layout()

    out_path = os.path.join(output_folder, "riduzione_assoluta.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvato grafico riduzione assoluta in: {out_path}")

def plot_gap_mtz(instances, gap_greedy, gap_two_opt, gap_sa, output_folder="results/figures"):
    import matplotlib.pyplot as plt
    import os

    os.makedirs(output_folder, exist_ok=True)

    x = range(len(instances))
    width = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar([i - width for i in x], gap_greedy, width=width, label="Greedy gap (%)")
    plt.bar(x, gap_two_opt, width=width, label="2-opt gap (%)")
    plt.bar([i + width for i in x], gap_sa, width=width, label="SA gap (%)")

    plt.xticks(list(x), instances, rotation=45)
    plt.ylabel("Gap % rispetto all’ottimo MTZ")
    plt.title("Confronto gap percentuale: Greedy / 2-opt / SA vs MTZ")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(output_folder, "gap_vs_mtz.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Salvato grafico gap MTZ in: {out_path}")

def plot_times(instances, t_greedy, t_two_opt, t_sa, t_mtz, output_folder="results/figures"):
    import matplotlib.pyplot as plt
    import os

    os.makedirs(output_folder, exist_ok=True)

    x = range(len(instances))
    width = 0.2

    plt.figure(figsize=(10, 6))

    plt.bar([i - width*1.5 for i in x], t_greedy, width=width, label="Greedy")
    plt.bar([i - width/2 for i in x], t_two_opt, width=width, label="2-opt")
    plt.bar([i + width/2 for i in x], t_sa, width=width, label="SA")
    plt.bar([i + width*1.5 for i in x], t_mtz, width=width, label="MTZ (Gurobi)")

    plt.xticks(list(x), instances, rotation=45)
    plt.ylabel("Tempo di esecuzione [s] (scala log)")
    plt.title("Confronto tempi: Greedy vs 2-opt vs SA vs MTZ")
    plt.yscale("log")  # << SCALA LOGARITMICA IMPORTANTE
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(output_folder, "tempi_confronto.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Salvato grafico tempi in: {out_path}")


def main():
    csv_path = "results/output.csv"
    if not os.path.exists(csv_path):
        print(f"File {csv_path} non trovato. Esegui prima run_all.py.")
        return

    import csv
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)

        instances = []
        greedy = []
        two_opt = []
        sa = []
        mtz = []

        gap_g = []
        gap_2 = []
        gap_sa = []

        # NUOVE LISTE PER I TEMPI
        t_greedy = []
        t_two_opt = []
        t_sa_list = []
        t_mtz = []

        for row in reader:
            instances.append(row["instance"])

            greedy.append(float(row["greedy_cost"]))
            two_opt.append(float(row["two_opt_cost"]))
            sa.append(float(row["sa_cost"]))
            mtz.append(float(row["mtz_cost"]))

            gap_g.append(float(row["gap_greedy"]))
            gap_2.append(float(row["gap_two_opt"]))
            gap_sa.append(float(row["gap_sa"]))

            # --- NUOVO: lettura tempi ---
            t_greedy.append(float(row["t_greedy"]))
            t_two_opt.append(float(row["t_two_opt"]))
            t_sa_list.append(float(row["t_sa"]))
            t_mtz.append(float(row["mtz_time"]))

    # grafici già esistenti
    plot_costs(instances, greedy, two_opt, sa)
    plot_improvements(instances, gap_2, gap_sa, greedy)
    plot_gap_mtz(instances, gap_g, gap_2, gap_sa)

    # --- NUOVO: grafico dei tempi ---
    plot_absolute_reduction(instances, greedy, sa)
    plot_times(instances, t_greedy, t_two_opt, t_sa_list, t_mtz)



if __name__ == "__main__":
    main()
