import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json


def load_facebook_network(directory):
    G = nx.Graph()
    for file_name in os.listdir(directory):
        if file_name.endswith('.edges'):
            edges_file = os.path.join(directory, file_name)
            with open(edges_file, 'r') as f:
                for line in f:
                    node1, node2 = map(int, line.strip().split())
                    G.add_edge(node1, node2)
    return G


def calculate_network_properties(G):
    degrees = [degree for node, degree in G.degree()]
    degree_distribution = np.bincount(degrees) / G.number_of_nodes()
    average_degree = np.mean(degrees)

    clustering_coeffs = list(nx.clustering(G).values())
    average_clustering_coeff = np.mean(clustering_coeffs)

    if nx.is_connected(G):
        path_lengths = dict(nx.all_pairs_shortest_path_length(G))
        lengths = [length for target_dict in path_lengths.values() for length in target_dict.values()]
        diameter = nx.diameter(G)
        average_path_length = np.mean(lengths)
    else:
        lengths = []
        diameters = []
        for component in nx.connected_components(G):
            subgraph = G.subgraph(component)
            path_lengths = dict(nx.all_pairs_shortest_path_length(subgraph))
            lengths.extend([length for target_dict in path_lengths.values() for length in target_dict.values()])
            diameters.append(nx.diameter(subgraph))
        diameter = max(diameters)
        average_path_length = np.mean(lengths)

    return {
        "degree_distribution": degree_distribution.tolist(),
        "average_degree": average_degree,
        "clustering_coeffs": clustering_coeffs,
        "average_clustering_coeff": average_clustering_coeff,
        "path_lengths": lengths,
        "diameter": diameter,
        "average_path_length": average_path_length
    }


def save_network_properties(properties, file_path):
    with open(file_path, 'w') as f:
        json.dump(properties, f)


def load_network_properties(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def plot_properties(properties):
    degree_distribution = properties["degree_distribution"]
    clustering_coeffs = properties["clustering_coeffs"]
    path_lengths = properties["path_lengths"]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(degree_distribution)), degree_distribution, width=0.8, color='skyblue')
    plt.title('Degree Distribution')
    plt.xlabel('Degree')
    plt.ylabel('P(k)')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.hist(clustering_coeffs, bins=10, color='skyblue', edgecolor='black')
    plt.title('Distribution of Clustering Coefficients')
    plt.xlabel('Clustering Coefficient')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.hist(path_lengths, bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of the Shortest Paths')
    plt.xlabel('Path Length')
    plt.ylabel('Frequency')
    plt.show()

if  __name__ == "__main__":
    directory = 'facebook'
    properties_file = 'network_properties.json'

    G = load_facebook_network(directory)
    properties = calculate_network_properties(G)
    save_network_properties(properties, properties_file)

    loaded_properties = load_network_properties(properties_file)
    plot_properties(loaded_properties)