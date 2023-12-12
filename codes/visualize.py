import networkx as nx
import matplotlib.pyplot as plt

class UITree:
    def __init__(self) -> None:
        self.tree = nx.Graph()
        self.image_paths = {}
        self.nodes = []

    def add_edge(self, u, v):
        if u not in self.nodes:
            self.nodes.append(u)
        if v not in self.nodes:
            self.nodes.append(v)
        self.tree.add_edge(u, v)

    def add_image_path(self, node, path):
        self.image_paths[node] = path
    
    def draw_tree(self):
        pos = nx.spring_layout(self.tree)
        plt.figure(figsize=(8, 6))

        # Draw nodes with images instead of circles
        for node in self.tree.nodes():
            image = plt.imread(self.image_paths[node])
            plt.imshow(image, extent=[pos[node][0] - 0.05, pos[node][0] + 0.05, pos[node][1] - 0.05, pos[node][1] + 0.05])

        # Draw edges
        nx.draw(self.tree, pos, with_labels=True, node_size=1000, node_color='skyblue')

        plt.axis('off')
        plt.show()
    def make_html_tree(self):
        html_code = "<!DOCTYPE html>\n<html>\n<head>\n<title>Tree Visualization</title>\n</head>\n<body>\n"
        html_code += "<svg width='500' height='500'>\n"

        # Calculate node positions
        level_height = 100
        node_positions = {node: (50 + i * 100, level_height * self.tree.degree[node]) for i, node in enumerate(self.tree.nodes)}

        # Draw edges
        for edge in self.tree.edges():
            html_code += f"<line x1='{node_positions[edge[0]][0]}' y1='{node_positions[edge[0]][1]}' \
                        x2='{node_positions[edge[1]][0]}' y2='{node_positions[edge[1]][1]}' stroke='black' />\n"

        # Draw nodes with images
        for node, image_path in self.image_paths.items():
            html_code += f"<image href='{image_path}' x='{node_positions[node][0] - 50}' \
                        y='{node_positions[node][1] - 50}' height='100' width='100' />\n"

        html_code += "</svg>\n</body>\n</html>"

        # Writing the HTML code to a file
        with open("tree_visualization.html", "w") as file:
            file.write(html_code)

        print("Tree visualization HTML file created: tree_visualization.html")

if __name__=="__main__":
    # Create a sample tree
    tree = nx.Graph()
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4)])

    # You would replace these paths with your image paths
    image_paths = {
        0: r'G:\SPL3_backend\Final\Credential-Mapping\dataset\image\formUI.jpg',
        1: r'G:\SPL3_backend\Final\Credential-Mapping\dataset\image\formUI1.jpg',
        2: r'G:\SPL3_backend\Final\Credential-Mapping\dataset\image\formUI2.jpg',
        3: r'G:\SPL3_backend\Final\Credential-Mapping\dataset\image\loginUI_1.jpg',
        4: r'G:\SPL3_backend\Final\Credential-Mapping\dataset\image\loginUI.jpg',
    }

        # Creating the HTML code for visualization
    html_code = "<!DOCTYPE html>\n<html>\n<head>\n<title>Tree Visualization</title>\n</head>\n<body>\n"
    html_code += "<svg width='500' height='500'>\n"

    # Calculate node positions
    level_height = 100
    node_positions = {node: (50 + node * 100, level_height * tree.degree[node]) for node in tree.nodes}

    # Draw edges
    for edge in tree.edges():
        html_code += f"<line x1='{node_positions[edge[0]][0]}' y1='{node_positions[edge[0]][1]}' \
                    x2='{node_positions[edge[1]][0]}' y2='{node_positions[edge[1]][1]}' stroke='black' />\n"

    # Draw nodes with images
    for node, image_path in image_paths.items():
        html_code += f"<image href='{image_path}' x='{node_positions[node][0] - 50}' \
                    y='{node_positions[node][1] - 50}' height='100' width='100' />\n"

    html_code += "</svg>\n</body>\n</html>"

    # Writing the HTML code to a file
    with open("tree_visualization.html", "w") as file:
        file.write(html_code)

    print("Tree visualization HTML file created: tree_visualization.html")