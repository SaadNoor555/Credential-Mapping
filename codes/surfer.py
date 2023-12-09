from XMLParser import XMLParser
from run_adb_commands import AdbCommand
import time

class Surfer:
    def __init__(self, packagename):
        self.packagename = packagename
        self.command_runner = AdbCommand(self.packagename)
        self.hash_set = set()

    def start_app(self):
        self.command_runner.start_app()
        self.command_runner.get_ui_info()
        parser = XMLParser()
        self.initial_screen = parser

    def dfs(self, curParser=None, i=0):
        if curParser==None:
            curParser = self.initial_screen
        self.hash_set.add(curParser.hash)
        # for action in curParser.scrollables:
        #     x1 = (action['bounds']['x0']+action['bounds']['x1'])//2
        #     y1 = action['bounds']['y0']
        #     x2 = x1
        #     y2 = action['bounds']['y1']
        #     y1, y2 = (y1+y2)//4, y2*0.8
        #     print(f'scrolling {x2}, {y2} to {x1}, {y1}')
        #     self.command_runner.swipe_event([x2, y2], [x1, y1])
        #     time.sleep(1)
        #     print(f'scrolling {x1}, {y1} to {x2}, {y2}')
        #     self.command_runner.swipe_event([x1, y1], [x2, y2])
        
        for action in curParser.clickables:
            if 'back' in action['text'].lower() or 'back' in action['content-desc'].lower():
                continue
            x, y = curParser.get_nodes_center(action)
            print(i)
            print(f'clicking {x}, {y}.\nclass: {action["class"]}\ntext: {action["text"]}\ncontent-desc: {action["content-desc"]}')
            self.command_runner.touch_event([x, y])
            time.sleep(2)
            self.command_runner.get_ui_info()
            childParser = XMLParser()
            if childParser.hash not in self.hash_set:
                self.dfs(childParser, i+1)
        self.command_runner.key_press_event('back')

if __name__=='__main__':
    package_name = 'com.google.android.contacts'
    surfer = Surfer(package_name)
    surfer.start_app()
    surfer.dfs()
