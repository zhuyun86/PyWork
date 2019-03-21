import math
import sys
import os
from openpyxl import load_workbook


def readGeneMutation():
    wb = load_workbook(r'C:\Users\12sigma\Desktop\标注 突变信息.xlsx')
    sheet = wb.get_sheet_by_name("Sheet1")
    for i in range(2, 22): #2-21
        _row = i
        sample = str(sheet[_row][1].value)
        res = ''
        for i, v in enumerate(sheet[_row]): #30-312-333
            if i not in range(30, 334):
                continue
            if v.value == '-' or v.value == 0 or sheet[1][i].value == 'Pathway':
                continue
            res += sheet[1][i].value + ': ' + str(v.value) + '\n'
        with open(sample+'_gene.txt', 'w', encoding='UTF-8') as fw:
            fw.write(res)


dict_table = {'术后抗病毒治疗': 'shkbdzl', '抗病毒治疗': 'kbdzl', '术前肿瘤治疗情况（射频、TACE等）': 'sqzlzlqk', '子灶': 'zz', '包膜': 'bm',
        '坏死': 'hs', '肝外侵犯（写明部位）': 'gwqf', '镜下包膜有无突破': 'jxbmywtp', '镜下多灶性生长': 'jxdzxsz', '镜下子灶': 'jxzz',
        '微血管癌栓': 'wxgas', '肝硬化': 'gyh', '肝炎': 'gy', '肉眼癌栓': 'ryas', '分型': 'fx', '分级': 'fj',
         '术后TACE（注明治疗次数）': 'shtace', '术后抗病毒治疗（注明化疗药物）': 'shkbdzl'}

def readPathologicalFeatures():
    wb = load_workbook(r'C:\Users\12sigma\Desktop\病人信息登记(1).xlsx')
    sheet = wb.get_sheet_by_name("Sheet2")
    for _row in range(2, 20): #2-19
        sample = str(sheet[_row][4].value)
        res = ''
        for i, v in enumerate(sheet[_row]): #0-69
            if i not in [52, 53, 54]:
                if i not in [31, 32, 56, 57]:
                    if i not in range(39, 50):
                        continue
            # if v.value == '无':
            #     continue
            if sheet[1][i].value in dict_table.keys():
                res += dict_table[sheet[1][i].value] + ': ' + str(v.value) + '\n'
            else:
                res += sheet[1][i].value + ': ' + str(v.value) + '\n'
            with open(sample+'_features.txt', 'w', encoding='UTF-8') as fw:
                fw.write(res)

if __name__ == '__main__':

    readPathologicalFeatures()
    readGeneMutation()
