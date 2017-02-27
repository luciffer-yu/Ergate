from Utility import GlobalVar
import threading
class ErgateThread(threading.Thread):
    def __init__(self, work, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.isRunning = True
        self.work = work
        self.setDaemon(True)
        self.start()

    def run(self):
        while self.isRunning:
            try:
                task = GlobalVar.scan_list.get(True, timeout=5)
                GlobalVar.ret.put(self.work(task), timeout=10)
            except:
                if GlobalVar.scan_list.empty():
                    self.isRunning = False
                continue
