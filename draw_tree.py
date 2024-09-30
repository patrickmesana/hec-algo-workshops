import matplotlib.pyplot as plt
import networkx as nx

def draw_tree(input_list):
    G = nx.DiGraph()  # Create a directed graph to represent the tree
    
    # Add nodes and edges to the graph
    for i in range(len(input_list)):
        G.add_node(i, label=input_list[i])
        parent_index = int((i + 1) / 2) - 1
        if parent_index >= 0:  # If the element has a valid parent
            G.add_edge(parent_index, i)

    pos = hierarchy_pos(G, 0)  # Get hierarchical layout of the graph
    labels = nx.get_node_attributes(G, 'label')
    
    # Plot the graph
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color='skyblue', font_size=12, font_weight='bold', arrows=False)
    
    # This line ensures the plot is opened in a separate window
    plt.show()

def hierarchy_pos(G, root):
    """
    Positions nodes in a hierarchy, suitable for a tree.
    Source: https://stackoverflow.com/a/29597209/490906
    """
    pos = _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    if parsed is None:
        parsed = {root}
    else:
        parsed.add(root)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
    if len(children) != 0:
        dx = width / len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos

