import xml.etree.ElementTree as ET
import math

class XMLTree:
    def __init__(self, node=None, filepath:str=None) -> None:
        coord = ['x1', 'y1', 'x2', 'y2']
        idx = 0
        if filepath != None and node==None:
            tree = ET.parse(filepath)
            print(len(tree.getroot()))
            node = list(list(tree.getroot())[0])[0]
            print(node)

        self.node = node
        # self.attributes = []
        self.attributes = {}
        self.children = []
        for x in list(node):
            if x.tag=='children':
                chld = XMLTree(x)
                self.children.append(chld)
            else:
                # self.attributes.append(x)
                key = x.tag
                if x.tag == 'bounds':
                    key = coord[idx]
                    idx += 1
                self.attributes[key] = x.text

    def dfs(self, debug:bool=False, class_text:str='', findRel:bool=False, nodes:list=[], des_nodes:list=[])->list:
        nodes.append(self)
        if debug:
            print(self.attributes)
            x = input()
        
        '''The following part check whether the current node belongs
        to the desired class'''
        try:
            for text in class_text:
                if text in self.attributes['class']:
                    des_nodes.append(self)
                    break
        except:
            pass
        '''
        # OBSOLETE
        if findRel:
            # print('yo')
            self.relations.update(self.findRelations())
        '''
        for child in self.children:
            nodes, des_nodes = child.dfs(debug=debug, nodes=nodes, findRel=findRel, des_nodes=des_nodes)
        
        return nodes, des_nodes

    def bfs(self, debug:bool=False, class_text:list=[], findRel:bool=False)->list:
        nodes, queue, class_valid = [], [], []
        queue.append((0, self))
        while len(queue)!=0:
            cur = queue[0]
            queue = queue[1:]
            nodes.append(cur[1])
            if debug:
                print(cur[0], cur[1].node)
            '''The following part checks for desired classes'''
            try:
                for text in class_text:
                    if text in cur[1].attributes['class']:
                        class_valid.append(cur[1])
                        break
            except:
                pass
            '''
            # OBSOLETE
            if findRel:
                self.relations.update(cur[1].findRelations())
            '''
            for child in cur[1].children:
                queue.append((cur[0]+1, child))
        return nodes, class_valid
    
    def getDistance(self, oth: object):
        c1 = self.getCenter()
        c2 = oth.getCenter()
        return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)

    def getCenter(self):
        return ((int(self.attributes['x1'])+int(self.attributes['x2']))/2,
                (int(self.attributes['y1'])+int(self.attributes['y2']))/2)

    '''
    # OBSOLETE
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
    '''





if __name__=='__main__':
    # r'F:\spl3\Credential-Mapping\dataset\xmls\formUI.xml'
    # r'F:\spl3\Credential-Mapping\codes\window.xml'
    filepath = r'F:\spl3\Credential-Mapping\dataset\xmls\formUI.xml'
    # tree = ET.parse(filepath)
    # root = tree.getroot()
    # root = XMLTree(root.getchildren()[1].getchildren()[0])
    root = XMLTree(filepath=filepath)
    p = root.bfs(debug=False)
    print(len(p))
