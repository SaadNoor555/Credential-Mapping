import xml.etree.ElementTree as ET

class XMLTree:
    def __init__(self, node=None, filepath:str=None) -> None:
        if filepath != None and node==None:
            tree = ET.parse(filepath)
            node = list(list(tree.getroot())[1])[0]

        self.node = node
        # self.attributes = []
        self.attributes = {}
        self.children = []
        self.relations = {}
        for x in list(node):
            if x.tag=='children':
                chld = XMLTree(x)
                self.children.append(chld)
            else:
                # self.attributes.append(x)
                self.attributes[x.tag] = x.text

    def dfs(self, debug:bool=False, findRel:bool=False, nodes:list=[])->list:
        nodes.append(self)
        if debug:
            print(self.attributes)
            x = input()
        if findRel:
            # print('yo')
            self.relations.update(self.findRelations())
        for child in self.children:
            nodes = child.dfs(debug=debug, nodes=nodes, findRel=findRel)
        
        return nodes

    def bfs(self, debug:bool=False, findRel:bool=False)->list:
        nodes, queue = [], []
        queue.append((0, self))
        while len(queue)!=0:
            cur = queue[0]
            queue = queue[1:]
            nodes.append(cur[1])
            if debug:
                print(cur[0], cur[1].node)
            if findRel:
                self.relations.update(cur[1].findRelations())
            for child in cur[1].children:
                queue.append((cur[0]+1, child))
        
        return nodes
    
    def findRelations(self, label_texts:list=['TextView'], input_texts:list=['EditText']):
        label_box_map = {}
        for i in range(len(self.children)):
            try:
                for lbl_txt in label_texts:
                    if lbl_txt in self.children[i].attributes['class']:
                        for inp_txt in input_texts:
                            if inp_txt in self.children[i+1].attributes['class']:
                                label_box_map[self.children[i]] = self.children[i+1]
                                break
                        break
            except:
                continue
        
        return label_box_map





if __name__=='__main__':
    filepath = r'F:\spl3\Credential-Mapping\dataset\xmls\formUI.xml'
    # tree = ET.parse(filepath)
    # root = tree.getroot()
    # root = XMLTree(root.getchildren()[1].getchildren()[0])
    root = XMLTree(filepath=filepath)
    p = root.bfs(debug=False)
    print(len(p))
