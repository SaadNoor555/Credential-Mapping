from XMLParser import XMLParser, getSimilarity
from run_adb_commands import AdbCommand
import time
import json
from logger import Logger
from recorder import Recorder
from sentence_transformers import SentenceTransformer
import random
import hashlib
import os
from visualize import UITree

class Surfer:
    def __init__(self, packagename):
        self.packagename = packagename
        self.command_runner = AdbCommand(self.packagename)
        self.hash_set = set()
        self.relations = {}
        self.state = {}
        self.keymap = {}
        self.visited = set()
        self.logger = Logger()
        self.recorder = Recorder(self.packagename)
        self.model = model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.tree = UITree()

    def start_app(self):
        self.command_runner.start_app()
        self.recorder.add_event(type='start', coords='', wait=0)
        self.command_runner.get_ui_info()
        time.sleep(0.5)
        parser = XMLParser()
        self.initial_screen = parser
        log_message = f'hash len {len(self.initial_screen.hash)}'
        print(log_message)
        self.logger.write_line(log_message)

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
                log_msg = f'skipping since already clicked before {action["bounds"]}'
                print(log_msg)
                self.logger.write_line(log_msg)
                continue
            


            self.command_runner.get_ui_info()
            lastParser = XMLParser()
            if action not in lastParser.clickables:
                log_msg = f'skipping since current layout does not have it {action["bounds"]}'
                print(log_msg)
                self.logger.write_line(log_msg)
                self.dfs(lastParser)
                return
        
            self.state[curParser.hash][json.dumps(action['bounds'])] = True
            
            x, y = curParser.get_nodes_center(action)
            # print(i)
            log_msg = f'clicking {x}, {y}.\nclass: {action["class"]}\ntext: {action["text"]}\ncontent-desc: {action["content-desc"]}'
            print(log_msg)
            self.logger.write_line(log_msg)
            self.command_runner.touch_event([x, y])
            self.recorder.add_event('touch', [x,y], 0.2)
            time.sleep(1)
            self.command_runner.get_ui_info()
            childParser = XMLParser()
            self.relations[curParser.hash][childParser.hash] = (x, y) 
            if childParser.hash not in self.hash_set:
                self.dfs(childParser, i+1)
        self.command_runner.get_ui_info()
        curScreen = XMLParser()
        if curScreen.hash!=self.initial_screen.hash:
            log_msg = 'going back'
            print(log_msg)
            self.logger.write_line(log_msg)
            self.command_runner.key_press_event('back')
            self.recorder.add_event('type', 'back', 0.2)
        else:
            log_msg = 'not going back since at home'
            print(log_msg)
            self.logger.write_line(log_msg)

    def go_to_state(self, stateHash):
        self.command_runner.start_app()
        self.recorder.add_event('start', '', 0)
        for coords in self.keymap[stateHash]:
            self.command_runner.touch_event(coords)
            self.recorder.add_event('touch', coords, 0.3)
            time.sleep(0.5)
        log_msg = 'state restored'
        print(log_msg)
        self.logger.write_line(print)
    
    def map_to_config(self, config_name, curParser):
        input_map = curParser.map_nodes()
        # print(input_map)
        f = open(config_name)
        config_map = json.load(f)
        label_sim_map = {}
        for label in input_map.keys():
            max_dis = 0
            label_sim_map[label] = {}
            for key in config_map.keys():
                similarity = getSimilarity(key, label, self.model)
                if similarity > max_dis:
                    max_dis = similarity
                    label_sim_map[label]['text'] = config_map[key]
                    label_sim_map[label]['similarity'] = similarity
        
        # print(label_sim_map)
        
        for key in label_sim_map:
            if label_sim_map[key]['similarity']>=0.4 and input_map[key]['dist']<100:
                cx, cy = curParser.get_nodes_center(input_map[key]['node'])
                print(cx, cy)
                self.command_runner.touch_event([cx, cy])
                self.recorder.add_event('touch', [cx, cy], 1)
                time.sleep(2)
                print(label_sim_map[key]['text'])
                self.command_runner.type_event(label_sim_map[key]['text'])
                self.recorder.add_event('print', label_sim_map[key]['text'], 1)
                time.sleep(2)
                self.command_runner.key_press_event(key='back')
                self.recorder.add_event('type', 'back')

    def bfs(self, curParser=None, config_name=r'G:\SPL3_backend\Final\Credential-Mapping\codes\contact_input.json', time_limit=100):
        start_time = time.time()
        if curParser==None:
            curParser = self.initial_screen
        queue = []
        
        self.keymap[curParser.hash] = []
        self.visited.add(curParser.hash)
        queue.append(curParser)
        while len(queue)!=0:
            log_msg = 'new iteration\n********************'
            print(log_msg)
            topParser = queue[0]
            queue = queue[1:]
            # performing events to go to topParser
            # for coords in self.keymap[topParser.hash]:
            #     self.command_runner.touch_event(coords)
            #     time.sleep(0.5)
            
            self.command_runner.get_ui_info()
            time.sleep(1)
            latestParser = XMLParser()
            if latestParser.hash != topParser.hash:
                self.command_runner.close_all()
                self.recorder.add_event('close_all', '', 0.2)
                self.go_to_state(topParser.hash)
            ss_folder = r'G:\SPL3_backend\Final\Credential-Mapping\codes\output_images'
            file_name = topParser.true_hash+'.png'
            file_path = os.path.join(ss_folder, file_name)
            self.tree.add_image_path(topParser.true_hash, file_path)
            self.command_runner.screenshot(file_path)
            time.sleep(2)
            for action in topParser.scrollables:
                
                x, y = topParser.get_nodes_center(action)
                log_msg = f'scrolling from {x},{y+200} to {x}, {y-200}'
                print(log_msg)
                self.logger.write_line(log_msg)
                self.command_runner.swipe_event((x, y+200), (x, y-200))
                self.recorder.add_event('swipe', [(x, y+200), (x, y-200)], 0.2)
                log_msg = f'scrolling from {x},{y-200} to {x}, {y+200}'
                print(log_msg)
                self.logger.write_line(log_msg)
                self.command_runner.swipe_event((x, y-200), (x, y+200))
                self.recorder.add_event('swipe', [(x, y-200), (x, y+200)], 0.2)

            random.shuffle(topParser.clickables)
            for action in topParser.clickables:
                if 'EditText' in action['class']:
                    self.map_to_config(config_name, topParser)
                    log_msg = f'skipping since edittext'
                    print(log_msg)
                    self.logger.write_line(log_msg)
                    continue
                print(f'time passed: {time.time()-start_time}s')
                if (time.time() - start_time)>time_limit:
                    log_msg = f'time limit of {time_limit}s reached'
                    print(log_msg)
                    self.logger.write_line(log_msg)
                    return
                # Starting to do available click actions
                x, y = topParser.get_nodes_center(action)
                log_msg = f'clicking {x}, {y}.\nclass: {action["class"]}\ntext: {action["text"]}\ncontent-desc: {action["content-desc"]}'
                print(log_msg)
                self.logger.write_line(log_msg)
                self.command_runner.touch_event([x, y])
                self.recorder.add_event('touch', [x, y], 0.2)
                self.command_runner.get_ui_info()
                newParser = XMLParser()
                if newParser.hash!=topParser.hash and newParser.hash not in self.visited:
                    self.keymap[newParser.hash] = self.keymap[topParser.hash][:]
                    self.keymap[newParser.hash].append([x,y])
                    file_name = newParser.true_hash+'.png'
                    file_path = os.path.join(ss_folder, file_name)
                    self.command_runner.screenshot(file_path)

                    time.sleep(2)
                    self.tree.add_image_path(newParser.true_hash, file_path)
                    self.tree.add_edge(topParser.true_hash, newParser.true_hash)
                    newParser.filter_clickables(topParser)
                    queue.append(newParser)
                    self.visited.add(newParser.hash)
                if 'edittext' in action['class'].lower():
                    log_msg = 'going back edittext'
                    print(log_msg)
                    self.logger.write_line(log_msg)
                    self.command_runner.key_press_event('back')
                    self.recorder.add_event('type', 'back', 0.2)
                    time.sleep(0.5)
                log_msg = f'newParser length: {len(newParser.hash)}'
                print(log_msg)
                self.logger.write_line(log_msg)
                if newParser.hash!=topParser.hash:
                    log_msg = 'going back***'
                    print(log_msg)
                    self.logger.write_line(log_msg)
                    self.command_runner.key_press_event('back')
                    self.recorder.add_event('key', 'back', 0.2)
                    time.sleep(0.5)
                    self.command_runner.get_ui_info()
                    time.sleep(0.5)
                    lastParser = XMLParser()
                    if lastParser.hash!=topParser.hash:
                        log_msg = f'lastParser length: {len(lastParser.hash)}'
                        print(log_msg)
                        self.logger.write_line(log_msg)
                        log_msg = f'topParser length: {len(topParser.hash)}'
                        print(log_msg)
                        self.logger.write_line(log_msg)
                        log_msg = 'closing as the app did not restore state'
                        print(log_msg)
                        self.logger.write_line(log_msg)
                        self.command_runner.close_all()
                        self.recorder.add_event('close_all', '')
                        self.go_to_state(topParser.hash)




if __name__=='__main__':
    package_name = 'com.google.android.contacts'
    surfer = Surfer(package_name)
    surfer.logger.write_line(f'Starting app {package_name}')
    surfer.start_app()
    # surfer.dfs()
    surfer.logger.write_line(f'starting traversal using bfs')
    surfer.bfs(time_limit=30)
    print(surfer.recorder.activities)
    surfer.recorder.save_states()
    # surfer.recorder.play_back()
    surfer.tree.make_html_tree()