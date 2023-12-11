import os
import time

class AdbCommand:
    def __init__(self, packagename='') -> None:
        self.package = packagename
        # self.start_app()

    def swipe_event(self, start, end, duration=50):
        command = f'input swipe {start[0]} {start[1]} \
            {end[0]} {end[1]} {duration}'
        test_adb_shell(command)

    def install_apk(self, apkpath):
        os.system(f'adb install {apkpath}')
        

    def touch_event(self, coord):
        command = f'input tap {coord[0]} {coord[1]}'
        test_adb_shell(command)

    def key_press_event(self, key, longpress=False):
        key_dict = {
            'up': 280,
            'down': 281,
            'left': 282,
            'right': 283,
            'home': 3,
            'back': 4,
            'caps_lock': 115,
            'soft_left': 1,
            'soft_right': 2,
            'dpad_up': 19,
            'dpad_down': 20,
            'dpad_left': 21,
            'dpad_right': 22,
            'dpad_center': 23,
            'volume_up': 24,
            'volume_down': 25,
            'power': 26,
            'clear': 28,
            'space': 62,
            'enter': 66,
            'del': 67,
            'escape': 111,
            'kill_app': 20,
            'recents': 'KEYCODE_APP_SWITCH',
            'delete': 'DEL'
        }
        test_adb_shell(f'input keyevent {key_dict[key]}')

    def type_event(self, message):
        messages = message.split(' ')
        for m in messages:
            test_adb_shell(f'input text {m}')
            self.key_press_event(key='space')


    def run_monkey(self, appname):
        pass
    def start_app(self):
        command = f'am start {self.package}'
        test_adb_shell(command)
        time.sleep(2.5)

    def close_app(self):
        self.key_press_event('home')
        time.sleep(0.5)
        self.key_press_event('recents')
        time.sleep(1)
        self.swipe_event([522, 1647], [522, 90])

    def close_all(self):
        self.key_press_event('recents')
        time.sleep(1.2)
        self.swipe_event([100, 1000], [800, 1000])
        time.sleep(1)
        self.touch_event([215, 1180])
        time.sleep(1)

    def get_ui_info(self, outputfile=''):
        command = f'uiautomator dump'
        test_adb_shell(command)
        self.retrieve_ui_info(localfile=outputfile)

    def retrieve_ui_info(self, outputfile='/sdcard/window_dump.xml', localfile='window.xml'):
        os.system(f'adb pull {outputfile} {localfile}')



def test_adb_shell(command):
    os.system(f'adb shell {command}')


if __name__=='__main__':
    # test_adb_shell('input swipe 100 1000 100 200')
    # test_adb_shell('input keyevent 28')
    # key_press_event('del')


    commander = AdbCommand('com.google.android.contacts')
    commander.get_ui_info()
    # commander.close_all()
    commander.type_event('saad')
    # for i in range(3):
    #     commander.close_app()
    # commander.touch_event([116, 216])

    # commander = AdbCommand()
    # filename = r'F:\spl3\Credential-Mapping\dataset\Daraz_Online_Shopping_App_7.5.1_Apkpure.apk'
    # commander.install_apk(filename)
    # start_app('com.google.android.contacts')