class Logger:
    def __init__(self, filename='log.txt') -> None:
        self.file = open(filename, 'w')

    def write_line(self, line):
        print(line, file=self.file)