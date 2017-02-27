import os
import re
import time
import csv
from Utility import ErgateThread

class Awvs(ErgateThread.ErgateThread):
    def __init__(self, exe):
        self.exe = exe
        self.awvscmd=('Save','SaveFolder','SaveLogs','SaveCrawlerData','GenerateReport','ReportFormat','ExportXML')
        if self.__env_check() == False:
            print '[Error]: Awvs command API %s not found' % self.exe
            exit()
        ErgateThread.ErgateThread.__init__(self, self.scan)

    def __env_check(self):
        return os.path.exists(self.exe)

    def scan(self, task):
        if task[1].strip().find('baike') >= 0:
            return
        cmd = self.__config(task)
        self.__call_api(cmd)
        vul_list = self.__log_read(cmd)
        return (task[0], task[1], vul_list)

    def __log_read(self, cmd):
        value = cmd.split(' ')
        vul_list = []
        target = ''
        for i in xrange(len(value)):
            if value[i].find('SaveFolder') >= 0:
                path = value[i+1].strip() + '\\'
                break
        for root,sub_dirs,files in os.walk(path):
            for filename in files:
                if filename.find('.csv') >= 0:
                    target = os.path.join(root, filename)
                    break
        pattern = re.compile('\[(medium|low|high)\]')
        with open(target, 'rb') as csv_file:
            rd = csv.reader(csv_file)
            for line in rd:
                try:
                    vul_level = ''
                    mt = pattern.search(line[3].strip())
                    if mt.group(0).find('[high]') >= 0:
                        vul_level = 'high'
                    if mt.group(0).find('[medium]') >= 0:
                        vul_level = 'medium'
                    if mt.group(0).find('[low]') >= 0:
                        vul_level = 'low'
                    vul_dscript = line[3].strip()[len(mt.group(0)):len(line[3].strip())]
                    vul_list.append((vul_level, vul_dscript))
                except:
                    continue
        return vul_list

    def __call_api(self, cmd):
        try:
            os.system(cmd.encode('GBK'))
        except Exception,e:
            print str(Exception)
            print str(e)
        time.sleep(10)

    def __config(self, task):
        cmd = self.exe + ' /Scan ' + task[1].strip()
        pattern = re.compile('[^=.*]+')
        fp = open(os.getcwd() + '\ScanMethod\Awvs\scan.config')
        for line in fp:
            value = pattern.findall(line)
            if value[0] in self.awvscmd:
                if value[1].strip() == 'True':
                    cmd = cmd + ' /' + value[0]
                else:
                    cmd = cmd + ' /' + value[0]
                    cmd = cmd + ' ' + value[1].strip()
                    if value[0] == 'SaveFolder':
                        cmd = cmd +  '\\' + task[0]
        fp.close()
        return cmd
