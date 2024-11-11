from watchdog.observers import Observer
from  watchdog.events import  PatternMatchingEventHandler
from threading import Timer
from subprocess import Popen




class Runner:
    __proc =None
    __handler_func = None


    @staticmethod
    def run():
        Runner.__proc = Popen(['python' , "main.py"])

    @staticmethod 
    def hadnle_file_modifed(event):
        if(Runner.__proc !=None):
            Runner.__proc.kill()

        if(Runner.__handler_func!=None):
            Runner.__handler_func.cancel()

        Runner.__handler_func = Timer(0.5 , Runner.run)
        Runner.__handler_func.start()




Runner.run()

file_watcher = Observer()

file_modified_event_handler = PatternMatchingEventHandler(patterns=["./*.py"] , ignore_patterns=['./reloadable.py'])

file_modified_event_handler.on_modified = Runner.hadnle_file_modifed

file_watcher.schedule(file_modified_event_handler , "." , recursive= True)
file_watcher.start()



try:
    while file_watcher.is_alive():
        file_watcher.join(1)
except KeyboardInterrupt:
    file_watcher.stop()


file_watcher.join()




