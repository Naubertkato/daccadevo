from qdpy.containers import Grid
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import ast
import warnings
from datetime import datetime
from .DACCADRun import evaluate_timeseries

def get_data(path):
    res = None
    with open(path, "rb") as f:
        res = pickle.load(f)
    return res

def extract_from_individuals(container, func):
    evals = np.array(list(map(func, container)))
    return evals

def get_bests(container, n=5, threshold = None, key = lambda indiv: indiv.fitness[0]):
    """ Return the n best individuals, as sorted by key. If threshold is not None, return all individuals above threshold instead """
    lcontainer = list(container)
    evals = extract_from_individuals(lcontainer, key)
    best_indexes = np.argsort(evals)[::-1]
    if threshold is not None:
        best_indexes = np.nonzero(evals > threshold)[0]
    elif n < len(best_indexes): # if n is above the number of individuals, return everything in order instead
        best_indexes = best_indexes[:n]
    return [lcontainer[b] for b in best_indexes]

def merge_containers(containers):
    # TODO: how to deal with cases where the feature ranges are different, but not automatically updated by add? E.g., results from AURORA
    merged_grid = containers[0]
    if not hasattr(merged_grid,"parents"):
        merged_grid.parents = []
    for i in range(1,len(containers)):
        for indiv in containers[i]:
            merged_grid.add(indiv) # should determine the correct place
    return merged_grid


def get_metric_over_time(dt, metric="qd_score", batch_size= None):
    """Available from iterations: alg_name iteration cont_size evals nb_updated avg std min max ft_min ft_max qd_score elapsed"""
    results = pd.DataFrame(dt[metric].apply(ast.literal_eval))
    if batch_size is None:
        batch_size = dt["evals"].astype("int")
    if not isinstance(batch_size, int) and len(set(batch_size)) > 1:
        warnings.warn("Inconsistent batch_size. If that is NOT expected, it may lead to strange results.")
        warnings.warn("You may force unification by specifying an explicit batch_size in the configs.")
    results["total_eval"] = batch_size*dt["iteration"].astype("int")
    n_plots = 1
    if isinstance(results[metric].iloc[0],list):
        n_plots = len(results[metric].iloc[0])
        results[[f"{metric}_{i}" for i in range(n_plots)]] = results[metric].tolist()
    fig, axs = plt.subplots(n_plots)

    if n_plots > 1:
        for n in range(n_plots):
            sns.lineplot(data=results, x="total_eval", y=f"{metric}_{n}", ax=axs[n])
    elif isinstance(results[metric].iloc[0],list):
        sns.lineplot(data=results, x="total_eval", y=f"{metric}_{0}", ax=axs)
    else:
        sns.lineplot(data=results, x="total_eval", y=metric, ax=axs)
    return fig, axs
    


def evaluate_timeseries_on_bests(container, config, n_best=3, threshold=None, verbose=False, key = lambda indiv: indiv.fitness[0]):
    config["keepTemporaryFiles"] = False
    all_timeseries = []
    labels = []
    print(f"Showing the top {n_best} individuals: (index and fitness)")
    indiv_list = get_bests(container, n=n_best, threshold=threshold, key = key)
    for i in indiv_list:
        ft = i.features
        if len(ft) == 0: # container uses dynamic indexing
            ft = container.get_ind_features(i)
        index = container.index_grid(ft)
        if verbose:
            print(index,i.fitness[0])
        y = evaluate_timeseries(i, config = config)[:,0]
        all_timeseries.append(y)
        labels.append(index)
    return all_timeseries, labels

def plot_bests(time_series, container, labels = None, configs = None, figname = None):
    fig, axs = plt.subplots(figsize=(10.5,5.5), ncols=2, gridspec_kw={'width_ratios': [1,1.25]})

    # Timeseries
    lines = axs[0].plot(np.array(time_series).T)
    for i in range(len(lines)):
        lines[i].set_zorder(len(lines)-i)
    axs[0].set_ylabel("Concentration [nM]")
    axs[0].set_xlabel("Time [min]")
    axs[0].set_title(f"Top {len(time_series)} individuals")
    axs[0].set_box_aspect(1)
    
    # Grid of elites
    feat_x, feat_y = container.features_domain
    fit_min, fit_max = container.fitness_domain[0]
    heat = axs[1].imshow(container.quality_array[...,0].T,origin="lower",interpolation='none', vmin=fit_min, vmax=fit_max,extent=[feat_x[0],feat_x[1],feat_y[0],feat_y[1]])
    axs[1].set_title("Grid of elites")
    if configs is not None and 'features_list' in configs:
        if len(configs['features_list']) > 0:
            axs[1].set_xlabel(configs['features_list'][0])
        else:
            axs[1].set_xlabel("dynamic feature 0")
        if len(configs['features_list']) > 1:
            axs[1].set_ylabel(configs['features_list'][1])
        else:
            axs[1].set_ylabel("dynamic feature 1")
    axs[1].set_box_aspect(1)
    if labels is not None:
        lenx, leny = container.shape
        ft = container.features_domain
        xmin, xmax = ft[0]
        ymin, ymax = ft[1]
        dx = (xmax-xmin)/lenx
        dy = (ymax-ymin)/leny
        for i, l in enumerate(labels):
            axs[1].add_patch(plt.Circle([xmin+(l[0]+0.5)*dx,ymin+(l[1]+0.5)*dy], radius = dx, linewidth=3, edgecolor= lines[i].get_color(), facecolor='none', zorder=len(lines)-i))

    # Color bar
    fitness_label = "fitness"
    if configs is not None and 'fitness_type' in configs:
        fitness_label += f": {configs['fitness_type']}"
    fig.colorbar(heat, ax=axs[1], label = fitness_label, shrink=0.78)
    if labels is not None:
        fig.legend(labels, bbox_to_anchor=(0.5, 0.0), ncols=min(len(labels),5), loc='lower center')
    plt.tight_layout()
    if figname is not None:
        plt.savefig(figname)
    else:
        plt.show()

def default_analysis(evo_data_list, n_best=3, threshold_best = None, verbose = False, merge_data=True):
    containers = []
    iterations = []
    for evo_data in evo_data_list:
        if verbose:
            print(evo_data['iterations'])
        iterations.append(evo_data['iterations'])
        container = evo_data["container"]
        if not isinstance(container, Grid):
            shape = container.shape if hasattr(container,"shape") else (32,) * len(container.features_domain)
            container = container.to_grid(shape)
        containers.append(container)

    dataframe = pd.concat(iterations)
    batch_size = evo_data_list[0]["config"]["algorithms"][evo_data_list[0]["config"]['main_algorithm_name']]["batch_size"]
    fig1, ax1 = get_metric_over_time(dataframe, batch_size= batch_size, metric="max")
    fig2, ax2 = get_metric_over_time(dataframe, batch_size= batch_size)

    if merge_data:
        containers = [merge_containers(containers)]

    for i, c in enumerate(containers):
        config = evo_data_list[i]["config"]
        all_timeseries, labels = evaluate_timeseries_on_bests(c, config, n_best= n_best, threshold=threshold_best, verbose=verbose)
        plot_bests(all_timeseries, c, labels=labels, configs=config)

    
if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Usage:",sys.argv[0],"file_or_directory")
        exit()

    p = Path(sys.argv[1])
    if p.is_dir():
        dt = [get_data(f) for f in p.glob("*.p")]
    else:
        dt = [get_data(p)]
    default_analysis(dt, n_best=3, merge_data=False, verbose=True)
    
