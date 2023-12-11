from XMLParser import XMLParser
from run_adb_commands import AdbCommand
import time
import json

class Surfer:
    def __init__(self, packagename):
        self.packagename = packagename
        self.command_runner = AdbCommand(self.packagename)
        self.hash_set = set()
        self.relations = {}
        self.state = {}
        self.keymap = {}
        self.visited = set()

    def start_app(self):
        self.command_runner.start_app()
        self.command_runner.get_ui_info()
        time.sleep(0.5)
        parser = XMLParser()
        self.initial_screen = parser
        print(f'hash len {len(self.initial_screen.hash)}')

    def dfs(self, curParser=None, i=0):
        if curParser==None:
            curParser = self.initial_screen
        self.hash_set.add(curParser.hash)
        if curParser.hash not in self.relations.keys():
            self.relations[curParser.hash] = {}
        # for action in curParser.scrollables:
            # x1 = (action['bounds']['x0']+action['bounds']['x1'])//2
            # y1 = action['bounds']['y0']
            # x2 = x1
            # y2 = action['bounds']['y1']
            # y1, y2 = (y1+y2)//4, y2*0.8
            # print(f'scrolling {x2}, {y2} to {x1}, {y1}')
            # self.command_runner.swipe_event([x2, y2], [x1, y1])
            # time.sleep(1)
            # print(f'scrolling {x1}, {y1} to {x2}, {y2}')
            # self.command_runner.swipe_event([x1, y1], [x2, y2])
        if curParser.hash not in self.state.keys():
            self.state[curParser.hash] = {}
            for action in curParser.clickables:
                self.state[curParser.hash][json.dumps(action['bounds'])] = False
        for action in curParser.clickables:
            forbidden = ['close', 'back', 'navigate up', \
                         'sign in', 'sign up']
            flg = False
            for word in forbidden:
                if word in action['text'].lower() or word in action['content-desc'].lower():
                    flg = True
                    break
            if flg:
                continue


            if self.state[curParser.hash][json.dumps(action['bounds'])]:
                print(f'skipping since already clicked before {action["bounds"]}')
                continue
            


            self.command_runner.get_ui_info()
            lastParser = XMLParser()
            if action not in lastParser.clickables:
                print(f'skipping since current layout does not have it {action["bounds"]}')
                self.dfs(lastParser)
                return
        
            self.state[curParser.hash][json.dumps(action['bounds'])] = True
            
            x, y = curParser.get_nodes_center(action)
            print(i)
            print(f'clicking {x}, {y}.\nclass: {action["class"]}\ntext: {action["text"]}\ncontent-desc: {action["content-desc"]}')
            self.command_runner.touch_event([x, y])
            time.sleep(2)
            self.command_runner.get_ui_info()
            childParser = XMLParser()
            self.relations[curParser.hash][childParser.hash] = (x, y) 
            if childParser.hash not in self.hash_set:
                self.dfs(childParser, i+1)
        self.command_runner.get_ui_info()
        curScreen = XMLParser()
        if curScreen.hash!=self.initial_screen.hash:
            print('going back')
            self.command_runner.key_press_event('back')
        else:
            print('not going back since at home')

    def go_to_state(self, stateHash):
        self.command_runner.start_app()
        for coords in self.keymap[stateHash]:
            self.command_runner.touch_event(coords)
            time.sleep(0.5)
        print('state restored')

    def bfs(self, curParser=None):
        if curParser==None:
            curParser = self.initial_screen
        queue = []
        
        self.keymap[curParser.hash] = []
        self.visited.add(curParser.hash)
        queue.append(curParser)
        while len(queue)!=0:
            print('new iteration\n********************')
            topParser = queue[0]
            queue = queue[1:]
            # performing events to go to topParser
            # for coords in self.keymap[topParser.hash]:
            #     self.command_runner.touch_event(coords)
            #     time.sleep(0.5)
            self.go_to_state(topParser.hash)

            for action in topParser.clickables:
                # Starting to do available click actions
                x, y = topParser.get_nodes_center(action)
                print(f'clicking {x}, {y}.\nclass: {action["class"]}\ntext: {action["text"]}\ncontent-desc: {action["content-desc"]}')
                self.command_runner.touch_event([x, y])
                self.command_runner.get_ui_info()
                newParser = XMLParser()
                if newParser.hash!=topParser.hash and newParser.hash not in self.visited:
                    self.keymap[newParser.hash] = self.keymap[topParser.hash][:]
                    self.keymap[newParser.hash].append([x,y])
                    newParser.filter_clickables(topParser)
                    queue.append(newParser)
                    self.visited.add(newParser.hash)
                if 'edittext' in action['class'].lower():
                    print('going back edittext')
                    self.command_runner.key_press_event('back')
                    time.sleep(0.5)
                print(len(newParser.hash))
                if newParser.hash!=topParser.hash:
                    print('going back***')
                    self.command_runner.key_press_event('back')
                    time.sleep(0.5)
                    self.command_runner.get_ui_info()
                    time.sleep(0.5)
                    lastParser = XMLParser()
                    if lastParser.hash!=topParser.hash:
                        print(len(lastParser.hash))
                        print(len(topParser.hash))
                        print('closing as the app did not restore state')
                        self.command_runner.close_all()
                        self.go_to_state(topParser.hash)




if __name__=='__main__':
    package_name = 'com.google.android.contacts'
    surfer = Surfer(package_name)
    surfer.start_app()
    # surfer.dfs()
    surfer.bfs()
