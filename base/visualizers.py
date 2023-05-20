from warnings import warn
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

class Sketcher:
    def __init__(self, base_vars:list):
        self.base_vars = base_vars
        self.vars = {}

        for v in self.base_vars:
            self.vars[v.name] = v
        self.expns = []
        self.graph = nx.DiGraph()
        
    def perform_ops(self, operations_dict: dict):
        self.operations_dict = operations_dict
        
        for var, (a, b, fun) in operations_dict.items():
            # print(a, b, fun)
            if a not in self.vars:
                self.vars[a.name] = a
            if b is not None:
                if b not in self.vars:
                    self.vars[b.name] = b
            
            if b is not None:                
                temp = fun(a, b)
            else:
                temp = fun(a)

            temp.name = var[1]
            
            self.expns.append(temp)
        
        self.vars[self.expns[-1].name] = self.expns[-1]
        # print(self.vars)
        
    def create_network(self):
        for i, v in self.operations_dict.items():
            x, y, _ = v
            u1idx = x.name
            if y is not None:
                u2idx = y.name
            # adder = len(self.base_vars)
            self.graph.add_edge(u1idx, i[1])
            if y is not None:
                self.graph.add_edge(u2idx, i[1])
            
    def plot(self, show=True, save=True, filename=None):
        if not show and not save:
            warn("Both save and show are False !! By default plot will be saved")
            save = True
        if save and filename is None:
            warn("Any previous values will be overwritten, Its recommended to name the file")
        
        M = self.graph.number_of_edges()
        node_sizes = [3 + 10 * i for i in range(len(self.graph))]
        seed=42
        pos = nx.spring_layout(self.graph, seed=seed)
        edge_colors = range(2, M + 2)
        edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
        cmap = plt.cm.plasma

        plt.figure(figsize=(12, 12))
        nodes = nx.draw_networkx_nodes(self.graph, pos, node_size=1000, node_color="indigo")
        edges = nx.draw_networkx_edges(
            self.graph,
            pos,
            node_size=node_sizes,
            arrowstyle="->",
            arrowsize=10,
            edge_color=edge_colors,
            edge_cmap=cmap,
            width=2,
        )

        for i in range(M):
            edges[i].set_alpha(edge_alphas[i])
            
        pc = mpl.collections.PatchCollection(edges, cmap=cmap)
        pc.set_array(edge_colors)
        plt.colorbar(pc)

        labels = {}
        for name, var in self.vars.items():
            if 'const' in name:
                labels[name] = f"{var.value}"        
            labels[name] = fr"${name}$"
            
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=22, font_color="whitesmoke")

        ax = plt.gca()
        ax.set_axis_off()
        if save and filename is None:
            plt.savefig('outputs/comp_graph.png')
        elif save:
            plt.savefig('outputs/' + filename + '.png')
        if show:
            plt.show()
    
    def visualize(self, operations_dict: dict, show=True, save=True, filename=None):
        self.perform_ops(operations_dict)
        self.create_network()
        self.plot(show, save, filename)