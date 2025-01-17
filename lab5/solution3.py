import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

def erdos_renyi_gnl(N, L):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    edges = set()
    while len(edges) < L:
        u, v = random.sample(range(N), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    G.add_edges_from(edges)
    return G

def calculate_properties(G):
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

    return degree_distribution, average_degree, clustering_coeffs, average_clustering_coeff, lengths, diameter, average_path_length

def plot_properties(degree_distribution, clustering_coeffs, path_lengths):
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
N = 100
L = 200
G = erdos_renyi_gnl(N, L)
degree_distribution, average_degree, clustering_coeffs, average_clustering_coeff, path_lengths, diameter, average_path_length = calculate_properties(G)

print(f"Average Degree: {average_degree}")
print(f"Average Clustering Coefficient: {average_clustering_coeff}")
print(f"Diameter: {diameter}")
print(f"Average Path Length: {average_path_length}")

plot_properties(degree_distribution, clustering_coeffs, path_lengths)
def erdos_renyi_gnp(N, p):
    return nx.erdos_renyi_graph(N, p)

# Example usage for Erdős-Rényi-Gilbert Model
N = 100
p = 0.05
G_gnp = erdos_renyi_gnp(N, p)
degree_distribution_gnp, average_degree_gnp, clustering_coeffs_gnp, average_clustering_coeff_gnp, path_lengths_gnp, diameter_gnp, average_path_length_gnp = calculate_properties(G_gnp)

print(f"Average Degree (Gnp): {average_degree_gnp}")
print(f"Average Clustering Coefficient (Gnp): {average_clustering_coeff_gnp}")
print(f"Diameter (Gnp): {diameter_gnp}")
print(f"Average Path Length (Gnp): {average_path_length_gnp}")

plot_properties(degree_distribution_gnp, clustering_coeffs_gnp, path_lengths_gnp)
def watts_strogatz(N, k, beta):
    return nx.watts_strogatz_graph(N, k, beta)

# Example usage for Watts-Strogatz Model
N = 100
k = 4
beta = 0.1
G_ws = watts_strogatz(N, k, beta)
degree_distribution_ws, average_degree_ws, clustering_coeffs_ws, average_clustering_coeff_ws, path_lengths_ws, diameter_ws, average_path_length_ws = calculate_properties(G_ws)

print(f"Average Degree (WS): {average_degree_ws}")
print(f"Average Clustering Coefficient (WS): {average_clustering_coeff_ws}")
print(f"Diameter (WS): {diameter_ws}")
print(f"Average Path Length (WS): {average_path_length_ws}")

plot_properties(degree_distribution_ws, clustering_coeffs_ws, path_lengths_ws)