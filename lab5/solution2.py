import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

def calculate_degree_distribution(G):
    degrees = [degree for node, degree in G.degree()]
    degree_distribution = np.bincount(degrees) / G.number_of_nodes()
    average_degree = np.mean(degrees)
    return degree_distribution, average_degree

def calculate_clustering_coefficients(G):
    clustering_coeffs = list(nx.clustering(G).values())
    average_clustering_coeff = np.mean(clustering_coeffs)
    return clustering_coeffs, average_clustering_coeff

def calculate_shortest_paths_and_diameter(G):
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
    return lengths, diameter, average_path_length

def analyze_network(directory):
    G = load_facebook_network(directory)

    degree_distribution, average_degree = calculate_degree_distribution(G)
    clustering_coeffs, average_clustering_coeff = calculate_clustering_coefficients(G)
    path_lengths, diameter, average_path_length = calculate_shortest_paths_and_diameter(G)

    print(f"Average Degree: {average_degree}")
    print(f"Average Clustering Coefficient: {average_clustering_coeff}")
    print(f"Diameter: {diameter}")
    print(f"Average Path Length: {average_path_length}")

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(degree_distribution)), degree_distribution, width=0.8, color='skyblue')
    plt.title('Degree Distribution')
    plt.xlabel('Degree')
    plt.ylabel('P(k)')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.hist(clustering_coeffs, bins=10, color='skyblue', edgecolor='black')
    plt.title('Clustering Coefficient Distribution')
    plt.xlabel('Clustering Coefficient')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.hist(path_lengths, bins=20, color='skyblue', edgecolor='black')
    plt.title('Shortest Path Length Distribution')
    plt.xlabel('Path Length')
    plt.ylabel('Frequency')
    plt.show()

# Example usage
directory = 'facebook'
analyze_network(directory)