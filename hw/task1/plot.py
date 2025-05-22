import matplotlib.pyplot as plt
import os
import math


def extract_metrics_from_file(file_path):
    ipc = None
    mpki = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            if 'CPU 0 cumulative IPC:' in line:
                parts = line.split()
                ipc = float(parts[4])
                
            elif 'CPU 0 Branch Prediction Accuracy:' in line:
                parts = line.split()
                mpki = float(parts[7])

    return {
        'ipc': ipc,
        'mpki': mpki,
    }


def extract_metrics(dir_names, file_names):
    res = {}
    for dir_name in dir_names:
        res[dir_name] = {'ipc': [], 'mpki': []}
        for file_name in file_names:
            filepath = os.path.join(dir_name, (file_name + '.txt'))
            metrics = extract_metrics_from_file(filepath)
            res[dir_name]['ipc'].append(metrics['ipc'])
            res[dir_name]['mpki'].append(metrics['mpki'])
    return res
            

if __name__ == '__main__':

    dir_names = ['bimodal', 'markov', 'markov_proba']

    file_names = ['600', '602', '603', '605', '607', '619', '620', '621', '623', '625', '627', '628', '631', '638', '641', '644', '648', '649']

    all_metrics = extract_metrics(dir_names, file_names)

    gmean_metrics = {dir_name: {'ipc': 1, 'mpki': 1} for dir_name in dir_names}

    fig, ax = plt.subplots(figsize=(10, 5))
    for dir_name in dir_names:
        ax.scatter(list(map(int, file_names)), all_metrics[dir_name]['ipc'], label=dir_name, s=5)
    ax.grid()
    ax.legend()
    ax.set_title('IPC')
    ax.set_xlabel('Trace id')
    ax.set_ylabel('log IPC')
    ax.set_ylim(-5, 5)
    plt.savefig('plot.png', dpi=300)

    for dir_name in dir_names:
        dir_metrics = all_metrics[dir_name]
        for ipc, mpki in zip(dir_metrics['ipc'], dir_metrics['mpki']):
            gmean_metrics[dir_name]['ipc'] *= ipc
            gmean_metrics[dir_name]['mpki'] *= mpki
        n_measures = len(all_metrics[dir_name]['ipc'])
        gmean_metrics[dir_name]['ipc'] **= (1 / n_measures)
        gmean_metrics[dir_name]['mpki'] **= (1 / n_measures)
        print(f"Dir <{dir_name}>\nIPC GMEAN: {gmean_metrics[dir_name]['ipc']}\nMPKI GMEAN: {gmean_metrics[dir_name]['mpki']}\n")
