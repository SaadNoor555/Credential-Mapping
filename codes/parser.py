from XMLTree import XMLTree 

class Parser:
    def __init__(self, file: str) -> None:
        self.filepath = file
        self.tree = XMLTree(filepath=file)

    def traverse(self, strategy='bfs', debug=False):
        self.tree.bfs(debug=debug) if strategy=='bfs' else self.tree.dfs(debug=debug)


if __name__=='__main__':
    filepath = r'F:\spl3\Credential-Mapping\dataset\xmls\formUI.xml'
    tp = Parser(filepath)
    tp.traverse(debug=True, strategy='dfs')