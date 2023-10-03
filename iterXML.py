import xml.etree.ElementTree as ET

xml_file = r"dataset\xmls\formUI.xml"

tree = ET.parse(xml_file)
root = tree.getroot()
# print([elem.tag for elem in root.iter()])
for elem in root.iter():
    if elem.getchildren()!=[]:
        print(elem.getchildren())
    # print(ET.tostring(elem, encoding='utf8').decode('utf8'))
    # print(ET.tostring(elem, encoding='utf8').decode('utf8'))
    # print(elem.tag)
    # break
    # if elem.tag == 'class':
    #     print(ET.tostring(elem, encoding='utf8').decode('utf8'))
print(root)

def dfs(root):
    print(root.attrib)
    print('************')
    for child in root.getchildren():
        dfs(child)

# dfs(root)
# print(help(root))
# def process_menu(menu):
#     print('Processing: {}'.format(menu.get('display')))
#     for item in menu.getchildren():
#         if (item.tag != "menu"):
#             print(item)
#         else:
#             process_menu(item)

# for menu in root.iter("menu"):
#     process_menu(menu)