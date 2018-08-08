import xlrd
import xlwt


def readExcel():
    xlsfile = r"C:\Users\12sigma\Desktop\人工+AI阅片记录表.xlsx"
    book = xlrd.open_workbook(xlsfile)
    sheet0 = book.sheet_by_index(0)
    sheet_name = book.sheet_names()[0]
    print(sheet_name)

    sheet1 = book.sheet_by_name(sheet_name)
    if sheet1 == sheet0:
        print('Equal')
    else:
        print('Not equal')
    nrows = sheet0.nrows
    ncols = sheet0.ncols
    print('(', nrows, ncols, ')')

    cell_value1 = sheet0.cell_value(3, 9)
    print(cell_value1, type(cell_value1))
    if cell_value1 == '':
        print('Empty Str')


def writeExcel():
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    sheet.write(0, 0, 'EnglishName')
    sheet.write(1, 0, 'Marcovaldo')
    txt1 = '中文名字'
    sheet.write(0, 1, txt1)
    txt2 = '马可瓦多'
    sheet.write(1, 1, txt2)
    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'C:\Users\12sigma\Desktop\test1.xls')


if __name__ == '__main__':
    readExcel()

    s1 = b'123sdf'
    print(s1,type(s1))
    print(s1.decode('utf-8'),type(s1.decode('utf-8')))
    # writeExcel()
