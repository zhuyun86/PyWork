import winreg

if __name__ == '__main__':
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU", 0, winreg.KEY_WRITE|winreg.KEY_READ)
        i = 0
        lt = []
        while 1:
            name, value, type = winreg.EnumValue(key, i)
            # value, type = winreg.QueryValueEx(key, "MinimizedStateTabletModeOff")
            lt.append(name)
            i += 1
    except BaseException as e:
        print(e)
    print(lt)
    for v in lt:
        # winreg.DeleteKey(key, v)
        winreg.DeleteValue(key, v)