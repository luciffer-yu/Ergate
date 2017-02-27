from xlutils.copy import copy
from Utility import GlobalVar
import xlrd
import xlwt
import os

def SaveResult(data):
    path = GlobalVar.ret_path
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        origin = book.sheet_by_index(0)
        rows = origin.nrows
        wr = copy(book)
        xls_w =  wr.get_sheet(0)
        for task in data:
            if task:
                for detail in task[2]:
                    xls_w.write(rows, 0, task[0])
                    xls_w.write(rows, 1, task[1])
                    xls_w.write(rows, 2,  detail[0])
                    xls_w.write(rows, 3,  detail[1])
                    rows += 1
        wr.save(path)
    else:
        book = xlwt.Workbook()
        sheet = book.add_sheet('data', cell_overwrite_ok=False)
        sheet.write(0, 0, 'target')
        sheet.write(0, 1, 'domain')
        sheet.write(0, 2, 'level')
        sheet.write(0, 3, 'vulnerable')
        row = 1
        for task in data:
            for detail in task[2]:
                sheet.write(row, 0, task[0])
                sheet.write(row, 1, task[1])
                sheet.write(row, 2,  detail[0])
                sheet.write(row, 3,  detail[1])
                row += 1
        book.save(path)

class OutputFile:
    def __init__(self, file):
        self.file = file

    def write_university(self, data):
        fp = xlwt.Workbook()
        for province in data:
            row = 0
            sheet = fp.add_sheet(province, cell_overwrite_ok=False)
            for univers in data[province]:
                sheet.write(row, 0, univers)
                sheet.write(row, 1, data[province][univers])
                row += 1
        fp.save(self.file)
