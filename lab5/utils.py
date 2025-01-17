import tarfile
import json
import matplotlib.pyplot as plt
import numpy as np

def extract_tar_gz(file_path, extract_path='.'):
    """
    Extracts a tar.gz file to the specified directory.

    :param file_path: Path to the tar.gz file.
    :param extract_path: Directory where the contents will be extracted.
    """
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=extract_path)


def load_network_properties(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def print_network_statistics(properties):
    average_degree = properties["average_degree"]
    average_clustering_coeff = properties["average_clustering_coeff"]
    average_path_length = properties["average_path_length"]

    print(f"Average Degree: {average_degree}")
    print(f"Average Clustering Coefficient: {average_clustering_coeff}")
    print(f"Average Path Length: {average_path_length}")


if  __name__ == "__main__":
    algorithms = ['Erdos-Renyi', 'Erdos-Renyid-Gilbert', 'Watts and Strogatz']
    average_degrees = [4.0, 4.8, 4.0]
    average_clustering_coeffs = [0.0646031746031746, 0.05145238095238094, 0.3853333333333333]
    diameters = [8, 6, 10]
    average_path_lengths = [3.2810631229235883, 3.0726, 4.864]
    print(f"{'Algorithm':<10} {'Avg Degree':<12} {'Avg Clustering':<18} {'Diameter':<10} {'Avg Path Length':<15}")
    for i in range(len(algorithms)):
        print(
            f"{algorithms[i]:<10} {average_degrees[i]:<12} {average_clustering_coeffs[i]:<18} {diameters[i]:<10} {average_path_lengths[i]:<15}")
    x = np.arange(len(algorithms))
    width = 0.2
    fig, ax = plt.subplots(figsize=(12, 8))
    bar1 = ax.bar(x - 1.5 * width, average_degrees, width, label='Avg Degree')
    bar2 = ax.bar(x - 0.5 * width, average_clustering_coeffs, width, label='Avg Clustering Coeff')
    bar3 = ax.bar(x + 0.5 * width, diameters, width, label='Diameter')
    bar4 = ax.bar(x + 1.5 * width, average_path_lengths, width, label='Avg Path Length')

    ax.set_xlabel('Algorithm')
    ax.set_ylabel('Values')
    ax.set_title('Comparison of Network Properties')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()

    plt.show()
