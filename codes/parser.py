from XMLTree import XMLTree 

class Parser:
    def __init__(self, file: str) -> None:
        self.filepath = file
        self.tree = XMLTree(filepath=file)

    def traverse(self, strategy:str='bfs', debug:bool=False, findRel:bool=False):
        self.tree.bfs(debug=debug, findRel=findRel) if strategy=='bfs'\
              else self.tree.dfs(debug=debug, findRel=findRel)


if __name__=='__main__':
    filepath = r'F:\spl3\Credential-Mapping\dataset\xmls\formUI1.xml'
    tp = Parser(filepath)
    tp.traverse(strategy='bfs', debug=False, findRel=True)
    for key in tp.tree.relations.keys():
        print('label:')
        print(key.attributes)
        print('**********')
        print('field')
        print(tp.tree.relations[key].attributes)