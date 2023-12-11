import xml.etree.ElementTree as ET
from run_adb_commands import AdbCommand
import time
import math
from sentence_transformers import SentenceTransformer, util
import json
from transformers import pipeline

class XMLParser:
    def __init__(self, filename=r'F:\spl3\Credential-Mapping\codes\window_dump.xml'):
        commander = AdbCommand()
        commander.get_ui_info()
        time.sleep(1)
        self.tree = ET.parse(filename)
        # print(len(tree))
        self.root = self.tree.getroot()
        self.element_maps = []
        self.parse_tree()
        self.get_clickables()
        self.filter_by_class(['ViewGroup'])
        self.get_scrollables()
        self.get_long_clickables()
        self.hash = self.hash_node()
        

    def parse_tree(self):
        attributes = ['class', 'content-desc', 'checkable', 'bounds',\
                    'checked', 'scrollable', 'long-clickable', \
                    'password', 'selected', 'bounds', 'text', 'clickable']
        for node in self.root.iter():
            element = {}
            for key in attributes:
                val = node.get(key)
                if val=='true':
                    val = True
                elif val=='false':
                    val = False
                elif key=='bounds' and val!=None:
                    xs, ys = val[1:-1].split('][')
                    x0, y0 = xs.split(',')
                    x1, y1 = ys.split(',')
                    val = {}
                    val['x0'] = int(x0)
                    val['y0'] = int(y0)
                    val['x1'] = int(x1)
                    val['y1'] = int(y1)

                element[key] = val
            self.element_maps.append(element)

    def find_classes(self, class_texts):
        eligible = []
        for node in self.element_maps:
            for class_text in class_texts:
                try:
                    if class_text in node['class']:
                        eligible.append(node)
                except:
                    pass
        return eligible

    def hash_node(self):
        hash = ''
        # hash = str(len(self.element_maps))
        for node in self.element_maps:
            hash += '\n<'+(node['class'] if node['class']!=None else '')+';'
            hash += (json.dumps(node['bounds']) if node['class']!=None else '')+'>'
        seen = set()
        u_hash = []
        forbidden = ['ImageView', 'FrameLayout']
        for line in hash.splitlines():
            br = False
            for word in forbidden:
                if word in line:
                    br = True
                    break

            if line not in seen and not br:
                seen.add(line)
                u_hash.append(line)
        
        return '\n'.join(u_hash)


    def get_nodes_center(self, node):
        cx = (node['bounds']['x0']+node['bounds']['x1'])//2
        cy = (node['bounds']['y0']+node['bounds']['y1'])//2
        return cx, cy

    def get_nodes_distance(self, node1, node2):
        x1, y1 = self.get_nodes_center(node1)
        x2, y2 = self.get_nodes_center(node2)
        print(x1, x2, y1, y2)
        dis = math.sqrt(((x1-x2)**2)+((y1-y2)**2))
        print(dis)
        return dis

    def find_by_attribute(self, attribute):
        eligible = []
        for node in self.element_maps:
            if node[attribute]:
                eligible.append(node)
        return eligible
    
    def filter_by_class(self, class_list=[]):
        tmp = self.clickables
        for node in tmp:
            for cls in class_list:
                if cls in node['class'] and node['text']=='' and node['content-desc']=='':
                    self.clickables.remove(node)
                    break
    
    def remove_clickable(self, element):
        self.clickables.remove(element)
    
    def remove_scrollable(self, element):
        self.scrollables.remove(element)
    
    def remove_long_clickable(self, element):
        self.long_clickables.remove(element)

    def get_scrollables(self):
        self.scrollables = self.find_by_attribute('scrollable')

    def get_clickables(self):
        self.clickables = self.find_by_attribute('clickable')
    

    def filter_clickables(self, parent):
        new_clickables = []
        for clickable in self.clickables:
            if clickable not in parent.clickables:
                new_clickables.append(clickable)
        
        self.clickables = new_clickables


    def get_long_clickables(self):
        self.get_long_clickables = self.find_by_attribute('long-clickable')
    
    def get_node_height(self, node):
        return math.abs(node['bounds']['y0']-node['bounds']['y1'])
    
    def get_node_width(self, node):
        return math.abs(node['bounds']['x0']-node['bounds']['x1'])

    def map_nodes(self, label_classes=['TextView', 'EditText'], input_classes=['EditText']):
        labels = self.find_classes(label_classes)
        input_boxes = self.find_classes(input_classes)
        input_map = {}
        for label in labels:
            if label['text'] not in input_map.keys():
                input_map[label['text']] = {}
                input_map[label['text']]['dist'] = 9999
            for box in input_boxes:
                print(label['text'])
                cur_dist = self.get_nodes_distance(label, box)
                if cur_dist<input_map[label['text']]['dist']:
                    input_map[label['text']]['node'] = box
                    input_map[label['text']]['dist'] = cur_dist
        return input_map


def test_string_input(xp):
    edit_texts = xp.find_classes(['EditText'])
    commander = AdbCommand()
    for edit_text in edit_texts:
        cx, cy = xp.get_nodes_center(edit_text)
        print(cx, cy)
        commander.touch_event([cx, cy])
        time.sleep(0.5)
        commander.type_event('saad sakib noor')
        commander.get_ui_info('contacts_saad.xml')

def getSimilarity(sen1, sen2, model):
    #Compute embedding for both lists
    embedding_1= model.encode(sen1, convert_to_tensor=True)
    embedding_2 = model.encode(sen2, convert_to_tensor=True)

    return float(util.pytorch_cos_sim(embedding_1, embedding_2))

def test_mapping(model):
    filename = r'G:\SPL3_backend\Final\Credential-Mapping\codes\window_dump.xml'
    commander = AdbCommand()
    commander.get_ui_info()
    xp = XMLParser(filename)
    input_map = xp.map_nodes()
    config_name = r'G:\SPL3_backend\Final\Credential-Mapping\codes\contact_input.json'
    f = open(config_name)
    config_map = json.load(f)
    label_sim_map = {}
    for label in input_map.keys():
        max_dis = 0
        label_sim_map[label] = {}
        for key in config_map.keys():
            similarity = getSimilarity(key, label, model)
            if similarity>max_dis:
                max_dis=similarity
                label_sim_map[label]['text'] = config_map[key]
                label_sim_map[label]['similarity'] = similarity
    
    for key in label_sim_map:
        print(key)
        print(label_sim_map[key]['text'])
        print(label_sim_map[key]['similarity'])
        print(input_map[key]['dist'])
        print('****************************************')
        if label_sim_map[key]['similarity']>=0.4 and input_map[key]['dist']<100:
            cx, cy = xp.get_nodes_center(input_map[key]['node'])
            print(cx, cy)
            commander.touch_event([cx, cy])
            time.sleep(0.5)
            commander.type_event(label_sim_map[key]['text'])
            time.sleep(0.5)
            commander.key_press_event(key='back')


def test_scrolling():
    filename = r'G:\SPL3_backend\Final\Credential-Mapping\codes\window_dump.xml'
    commander = AdbCommand()
    commander.get_ui_info()
    xp = XMLParser(filename)
    scrollable = xp.scrollables
    print(len(scrollable))
    for action in scrollable:
        x1 = (action['bounds']['x0']+action['bounds']['x1'])//2
        y1 = action['bounds']['y0']
        x2 = x1
        y2 = action['bounds']['y1']
        y1, y2 = (y1+y2)//5, y2*0.7
        time.sleep(1)
        commander.swipe_event([x2, y2], [x1, y1])
        time.sleep(1)
        commander.swipe_event([x1, y1], [x2, y2])
        

if __name__=='__main__':
    # filename = r'G:\SPL3_backend\Final\Credential-Mapping\codes\window_dump.xml'
    # xp = XMLParser(filename)
    # model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # test_mapping(model)
    # test_scrolling()
    filename = r'G:\SPL3_backend\Final\Credential-Mapping\codes\window_dump.xml'
    xp = XMLParser(filename)
    print(xp.hash)
    

