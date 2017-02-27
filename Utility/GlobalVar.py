import Queue
import os

scan_list = Queue.Queue(20000)
ret = Queue.Queue(20000)
ret_path = os.getcwd() + '\\' + 'Ergate.xls'