import networkx as nx
import matplotlib.pyplot as plt

def draw_network_from_gml(file_path):
    # Load the network from the .gml file
    G = nx.read_gml(file_path)

    # Draw the network using a circular layout
    plt.figure(figsize=(10, 10))
    pos = nx.kamada_kawai_layout(G)  # Position nodes using the circular layout
    plt.title('Dolphin Network Visualization (Kamada-Kawai layout)', fontsize=25)

    nx.draw(G, pos, with_labels=True, node_size=500, node_color='orange', font_size=10, font_color='black',
            edge_color='blue', width=2)


    # Set the title before displaying the plot
    plt.show()

# Example usage
file_path = 'network_part_1/dolphins.gml'
draw_network_from_gml(file_path)