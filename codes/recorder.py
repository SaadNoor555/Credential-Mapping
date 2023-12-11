from run_adb_commands import AdbCommand
import time

class Recorder:
    def __init__(self, package) -> None:
        self.commander = AdbCommand(package)
        self.activities = []
        self.add_event('close_all', '',  0.5)

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
        for event in self.activities:
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
                self.commander.type_event(event['coords'])

            time.sleep(event['wait'])
