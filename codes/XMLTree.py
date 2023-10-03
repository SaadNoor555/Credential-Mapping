import xml.etree.ElementTree as ET

class XMLTree:
    def __init__(self, node=None, filepath:str=None) -> None:
        if filepath != None and node==None:
            tree = ET.parse(filepath)
            node = list(list(tree.getroot())[1])[0]

        self.node = node
        self.attributes = []
        self.children = []
        for x in list(node):
            if x.tag=='children':
                chld = XMLTree(x)
                self.children.append(chld)
            else:
                self.attributes.append(x)

    def dfs(self, debug:str=False, nodes:list=[])->list:
        nodes.append(self)
        if debug:
            print(self.node)
        for child in self.children:
            nodes = child.dfs(debug=debug, nodes=nodes)
        
        return nodes

    def bfs(self, debug:str=False)->list:
        nodes, queue = [], []
        queue.append((0, self))
        while len(queue)!=0:
            cur = queue[0]
            queue = queue[1:]
            nodes.append(cur[1])
            if debug:
                print(cur[0], cur[1].node)
            for child in cur[1].children:
                queue.append((cur[0]+1, child))
        
        return nodes


if __name__=='__main__':
    filepath = r'F:\spl3\Credential-Mapping\dataset\xmls\formUI.xml'
    # tree = ET.parse(filepath)
    # root = tree.getroot()
    # root = XMLTree(root.getchildren()[1].getchildren()[0])
    root = XMLTree(filepath=filepath)
    p = root.bfs(debug=False)
    print(len(p))
