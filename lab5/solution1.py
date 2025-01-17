import networkx as nx
import matplotlib.pyplot as plt


def draw_network_from_gml(file_path):
    G = nx.read_gml(file_path)
    plt.figure(figsize=(10, 10))
    pos = nx.kamada_kawai_layout(G)
    plt.title('Dolphin Network Visualization (Kamada-Kawai layout)', fontsize=25)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='orange', font_size=10, font_color='black',
            edge_color='blue', width=2)
    plt.show()


if  __name__ == "__main__":
    file_path = 'network_part_1/dolphins.gml'
    draw_network_from_gml(file_path)
