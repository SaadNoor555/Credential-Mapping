from XMLTree import XMLTree 

class Parser:
    def __init__(self, file: str) -> None:
        self.filepath = file
        self.tree = XMLTree(filepath=file)

    '''
    # OBSOLETE
    def traverse(self, strategy:str='bfs', debug:bool=False, findRel:bool=False):
        self.tree.bfs(debug=debug, findRel=findRel) if strategy=='bfs'\
              else self.tree.dfs(debug=debug, findRel=findRel)
    '''

    def findClass(self, class_text:list, strategy='bfs'):
        strat_map = {
            'bfs': self.tree.bfs,
            'dfs': self.tree.dfs
        }
        all, valid = strat_map[strategy](class_text=class_text)
        return valid

'''
# OBSOLETE
def exp1(tp: Parser):
    tp.traverse(strategy='bfs', debug=True, findRel=True)
    for key in tp.tree.relations.keys():
        print('label:')
        print(key.attributes)
        print('**********')
        print('field')
        print(tp.tree.relations[key].attributes)
'''

def exp2(tp: Parser):
    labels = tp.findClass(class_text=['TextView'])
    input_boxes = tp.findClass(class_text=['EditText'])
    # print(len(labels), len(input_boxes))
    # for box in input_boxes:
    #     print(box.getCenter())
    input_map = {}
    for label in labels:
        dist = 9999
        for box in input_boxes:
            cur_dist = label.getDistance(box)
            if cur_dist<dist:
                dist = cur_dist
                input_map[label] = box
    for key in input_map.keys():
        print('label:')
        print(key.attributes)
        print('**************')
        print(input_map[key].attributes)

if __name__=='__main__':
    filepath = r'F:\spl3\Credential-Mapping\dataset\xmls\loginUI.xml'
    tp = Parser(filepath)
    exp2(tp)