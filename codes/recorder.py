from run_adb_commands import AdbCommand
import time
import json
from visualize import UITree
from XMLParser import XMLParser
import os

class Recorder:
    def __init__(self, package) -> None:
        self.commander = AdbCommand(package)
        self.activities = []
        self.add_event('close_all', '',  0.5)
        self.tree = UITree()

    def load_events(self, filename):
        file = open(filename)
        self.activities = json.load(file)

    def add_event(self, type, coords, wait=0.5):
        self.activities.append({'type':type, 'coords':coords, 'wait': wait})

    def play_back(self):
        event_map = {
            'touch': self.commander.touch_event,
            'swipe': self.commander.swipe_event,
            'close_all': self.commander.close_all,
            'close': self.commander.close_app,
            'start': self.commander.start_app
        }
        self.commander.get_ui_info()
        time.sleep(1)
        topParser = XMLParser()
        ss_folder = r'F:\spl3\Credential-Mapping\codes\output_images'
        file_name = topParser.true_hash+'.png'
        file_path = os.path.join(ss_folder, file_name)
        self.tree.add_image_path(topParser.true_hash, file_path)
        self.commander.screenshot(file_path)
        time.sleep(2)
        for event in self.activities:
            curParser = topParser
            print(event)
            if event['type']=='touch':
                self.commander.touch_event(event['coords'])
            
            elif event['type']=='swipe':
                self.commander.swipe_event(event['coords'][0], event['coords'][1])
            
            elif event['type']=='close_all':
                self.commander.close_all()
            
            elif event['type']=='close':
                self.commander.close_app()
            
            elif event['type']=='start':
                self.commander.start_app()
            
            elif event['type']=='type':
                self.commander.key_press_event(event['coords'])

            elif event['type']=='print':
                self.commander.type_event(event['coords'])


            time.sleep(event['wait'])
            self.commander.get_ui_info()
            time.sleep(1)
            topParser = XMLParser()
            ss_folder = r'F:\spl3\Credential-Mapping\codes\output_images'
            file_name = topParser.true_hash+'.png'
            file_path = os.path.join(ss_folder, file_name)
            self.tree.add_image_path(topParser.true_hash, file_path)
            self.commander.screenshot(file_path)
            time.sleep(2)
            self.tree.add_edge(curParser.true_hash, topParser.true_hash)
            

    def save_states(self, filename='run_trace.json'):
        with open(filename, "w") as outfile: 
            json.dump(self.activities, outfile)


if __name__=="__main__":
    recorder = Recorder("com.google.android.contacts")
    event_file = r'F:\spl3\Credential-Mapping\dataset\saved_runs\contacts_saved_run.json'
    recorder.load_events(event_file)
    print(recorder.activities)
    recorder.play_back()
    recorder.tree.make_html_tree()