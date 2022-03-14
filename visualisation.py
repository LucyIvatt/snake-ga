import matplotlib.pyplot as plt
import os
from genetic import load_simulation_info
import numpy as np


def graph_plot(ax, generations, data, colour_map, graph_type, iteration_num, experiment_type, plot_std=False, stds=None):
    ax.set_xlabel('Generations')
    ax.set_ylabel('Average of ' + graph_type.capitalize() +
                  ' Fitness over ' + str(iteration_num) + ' iterations')
    for i in range(len(data)):
        if experiment_type == "cx-indpb-final":
            colour = "#9701FF" if i == 1 else "#00C5FF"
        elif experiment_type == "input-final":
            colour = "#20FF00" if i == 1 else "#FF8400"
        else:
            colour = colour_map(1.*data.index(data[i])/len(data))

        gen = generations
        ax.plot(gen, data[i][1], lw=3, label=data[i][0], color=colour)
        if graph_type == "mean" and plot_std:
            ax.fill_between(
                gen, (data[i][1]+stds[i][1]), (data[i][1]-stds[i][1]), color=colour, alpha=.1)

    ax.legend(loc='best', fancybox=True, framealpha=0.5)


def box_plot(ax, input, colour_map, experiment_type):
    labels = [algorithm[0] for algorithm in input]
    data = [algorithm[1] for algorithm in input]
    ax.set_xlabel('Algorithm Parameters')
    ax.set_ylabel('Fitness')
    labels = [label[:11] + "\n" + label[12:] for label in labels]
    box_plots = ax.boxplot(data, patch_artist=True, labels=labels)

    for i, plot in enumerate(box_plots['boxes']):
        if experiment_type == "cx-indpb-final":
            colour = "#9701FF" if i == 1 else "#00C5FF"
        elif experiment_type == "input-final":
            colour = "#20FF00" if i == 1 else "#FF8400"
        else:
            colour = colour_map(1.*data.index(data[i])/len(data))

        plot.set_facecolor(colour)


def initialise_graphs():
    fig = plt.figure(figsize=(14, 10), dpi=80)
    gs = fig.add_gridspec(2, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], sharex=ax1)
    ax3 = fig.add_subplot(gs[1, :])
    fig.set_size_inches(30, 20)
    fig.tight_layout()
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9,
                        top=0.9, wspace=0.1, hspace=0.1)
    return fig, ax1, ax2, ax3


def plot_cxindpb_experiment(type, plot_std=False):
    if type == "final":
        iteration_num = 15
    elif type == "exploration":
        iteration_num = 5

    fig, ax1, ax2, ax3 = initialise_graphs()

    fig.suptitle(
        f"{type.capitalize()} experiment showing the affect of different mutation and crossover probabilities on fitness", fontsize=22)
    save_location = f"sim-outputs//cx-indpb-{type}-experiment"

    averaged_means, averaged_maxes, averaged_stds = ([] for _ in range(3))
    final_generation_averages = []

    pairing_folders = [folder for folder in os.listdir(
        save_location) if os.path.isdir(save_location + "//" + folder)]
    for prob_pairing in pairing_folders:
        iterations = load_simulation_info(save_location + "//" + prob_pairing)

        logbooks = [run[1] for run in iterations]

        means, maxes, stds = ([] for _ in range(3))
        final_averages = []

        for logbook in logbooks:
            means.append(logbook.select("mean"))
            maxes.append(logbook.select("max"))
            stds.append(logbook.select("std"))
            final_averages.append(logbook.select("mean")[-1])

        label = iterations[0][0]
        averaged_means.append((label, np.mean(means, axis=0)))
        averaged_maxes.append((label, np.mean(maxes, axis=0)))
        averaged_stds.append((label, np.mean(stds, axis=0)))
        final_generation_averages.append((label, final_averages))

    ax1.title.set_text("Mean fitness over all generations")
    graph_plot(ax1, logbooks[0].select("gen"), averaged_means, plt.get_cmap(
        "gist_rainbow"), "mean", iteration_num, "cx-indpb-" + type, plot_std, averaged_stds)

    ax2.title.set_text("Max fitness over all generations")
    graph_plot(ax2, logbooks[0].select("gen"), averaged_maxes, plt.get_cmap(
        "gist_rainbow"), "max", iteration_num, "cx-indpb-" + type,)

    ax3.title.set_text(
        "Distribution of average fitness in the final generation for each iteration")
    box_plot(ax3, final_generation_averages, plt.get_cmap(
        "gist_rainbow"), "cx-indpb-" + type,)

    plt.savefig(save_location + f"//cx-indpb-{type}-experiment.png")


def plot_input_experiment(type, plot_std=False):
    if type == "exploration":
        iteration_num = 5
    elif type == "final":
        iteration_num = 15

    fig, ax1, ax2, ax3 = initialise_graphs()

    fig.suptitle(
        f"{type.capitalize()} experiment showing the affect of different neural network inputs on fitness", fontsize=22)
    save_location = f"sim-outputs//input-{type}-experiment"

    averaged_means, averaged_maxes, averaged_stds = ([] for _ in range(3))
    final_generation_averages = []

    pairing_folders = [folder for folder in os.listdir(
        save_location) if os.path.isdir(save_location + "//" + folder)]
    for prob_pairing in pairing_folders:
        iterations = load_simulation_info(
            save_location + "//" + prob_pairing)

        logbooks = [run[1] for run in iterations]

        means, maxes, stds = ([] for _ in range(3))
        final_averages = []

        for logbook in logbooks:
            means.append(logbook.select("mean"))
            maxes.append(logbook.select("max"))
            stds.append(logbook.select("std"))
            final_averages.append(logbook.select("mean")[-1])

        label = iterations[0][0]
        averaged_means.append((label, np.mean(means, axis=0)))
        averaged_maxes.append((label, np.mean(maxes, axis=0)))
        averaged_stds.append((label, np.mean(stds, axis=0)))
        final_generation_averages.append((label, final_averages))

    ax1.title.set_text("Mean fitness over all generations")
    graph_plot(ax1, logbooks[0].select("gen"), averaged_means, plt.get_cmap(
        "gist_rainbow"), "mean", iteration_num, "input-" + type, plot_std, averaged_stds)

    ax2.title.set_text("Max fitness over all generations")
    graph_plot(ax2, logbooks[0].select("gen"), averaged_maxes, plt.get_cmap(
        "gist_rainbow"), "max", iteration_num, "input-" + type,)

    ax3.title.set_text(
        "Distribution of average fitness in the final generation for each iteration")
    box_plot(ax3, final_generation_averages,
             plt.get_cmap("gist_rainbow"), "input-" + type,)

    plt.savefig(save_location + f"//input-{type}-experiment.png")


def plot_final_algorithm(plot_std=False):
    iteration_num = 15

    fig, ax1, ax2, ax3 = initialise_graphs()

    fig.suptitle(
        f"Final Algorithms fitness values over 250 generations", fontsize=22)
    save_location = f"sim-outputs//final-algorithm"

    averaged_means, averaged_maxes, averaged_stds = ([] for _ in range(3))
    final_generation_averages = []

    pairing_folders = [folder for folder in os.listdir(
        save_location) if os.path.isdir(save_location + "//" + folder)]
    for prob_pairing in pairing_folders:
        iterations = load_simulation_info(save_location + "//" + prob_pairing)

        logbooks = [run[1] for run in iterations]

        means, maxes, stds = ([] for _ in range(3))
        final_averages = []

        for logbook in logbooks:
            means.append(logbook.select("mean"))
            maxes.append(logbook.select("max"))
            stds.append(logbook.select("std"))
            final_averages.append(logbook.select("mean")[-1])

        label = iterations[0][0]
        averaged_means.append((label, np.mean(means, axis=0)))
        averaged_maxes.append((label, np.mean(maxes, axis=0)))
        averaged_stds.append((label, np.mean(stds, axis=0)))
        final_generation_averages.append((label, final_averages))

    ax1.title.set_text("Mean fitness over all generations")
    graph_plot(ax1, logbooks[0].select("gen"), averaged_means, plt.get_cmap(
        "gist_rainbow"), "mean", iteration_num, "cx-indpb-" + type, plot_std, averaged_stds)

    ax2.title.set_text("Max fitness over all generations")
    graph_plot(ax2, logbooks[0].select("gen"), averaged_maxes, plt.get_cmap(
        "gist_rainbow"), "max", iteration_num, "cx-indpb-" + type,)

    ax3.title.set_text(
        "Distribution of average fitness in the final generation for each iteration")
    box_plot(ax3, final_generation_averages, plt.get_cmap(
        "gist_rainbow"), "cx-indpb-" + type,)

    plt.savefig(save_location + f"//cx-indpb-{type}-experiment.png")
