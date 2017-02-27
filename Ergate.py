#-*- coding: utf-8 -*-
from optparse import OptionParser
from CrawlPlugin.Navigation360 import GetUniversity
from Log import output
from Utility import GlobalVar
from ScanMethod.Awvs import AwvsScanCtrl
import xlrd
import os

def GetCmdOpt():
    opt = OptionParser('Ergate (Scan and Test Automatic) Version 1.0')
    opt.add_option('-o', '--output', dest = 'out', type = 'string', help = 'The path of output file')
    opt.add_option('-t', '--threads', dest = 'threads', type = 'int', help = 'Number of scan thread')
    opt.add_option('-m', '--method', dest = 'method', type = 'string', help = 'A: Awvs scan;')
    opt.add_option('-p', '--path', dest = 'path', type = 'string', help = 'The path of scan command API')
    option, args = opt.parse_args()
    return option

def drop_completed_task():
    path = GlobalVar.ret_path
    task = []
    if os.path.exists(path):
        with xlrd.open_workbook(path) as xls:
            data = xls.sheet_by_index(0)
            for row in range(1, data.nrows):
                if not data.row_values(row)[0] in task:
                    task.append(data.row_values(row)[0].strip())
    return task

def CollectInfo():
    info = GetUniversity.UniversityInfo(10, 5).start_crawling()
    task_done = drop_completed_task()
    for province in info:
        for univers in info[province]:
            if not univers in task_done:
                GlobalVar.scan_list.put((univers, info[province][univers]), True)
            else:
                print 'drop task ' + univers
    return info

def CreateScan(number, path, method):
    print number
    threads = []
    for i in range(number):
        threads.append(AwvsScanCtrl.Awvs(path))
    return threads

if __name__ == '__main__':
    ret = []
    opt = GetCmdOpt()
    info = CollectInfo()
    output.OutputFile(opt.out).write_university(info)
    threads = CreateScan(opt.threads, opt.path, opt.method)
    while True:
        try:
            ret.append(GlobalVar.ret.get(True, timeout=10))
        except:
            if ret:
                output.SaveResult(ret)
                ret = []
            continue
