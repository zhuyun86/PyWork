import os, sys, json, copy
from collections import OrderedDict
import xmltodict

from const import DEFAULT_RESULT

resultKeys = [
    'CenterX', 'CenterY', 'CenterZ', 'True', 'Malign', 'Solid', 'GGO', 'Mixed',
    'Calc'
]


class ToolXml2Json():
    def __init__(self):
        self.jsonData = OrderedDict()
        self.__fileName = 'file.json'

    def xml2json(self, xml_file):
        """read xml, return json data"""
        with open(xml_file) as f:
            xmlDict = xmltodict.parse(f.read())
        nodules = self.jsonData.setdefault('Nodules', OrderedDict())
        root = xmlDict['boost_serialization']
        removeDuplicate = False
        if root.get('sigmaLU_version'):
            nodules['version'] = root['sigmaLU_version']
            if root['sigmaLU_version'] >= '0.5.6':
                removeDuplicate = True
        nodules['count'] = '0'
        nodule_items = nodules.setdefault('item', [])
        origin_items = root.get('Nodules', {}).get('item', [])
        verify_items = root.get('VerifiedNodules', {}).get('item', [])
        missed_items = root.get('MissedNodules', {}).get('item', [])
        if not isinstance(origin_items, list):
            origin_items = [origin_items]
        if not isinstance(verify_items, list):
            verify_items = [verify_items]
        if not isinstance(missed_items, list):
            missed_items = [missed_items]
        for oi in origin_items:
            oi['sourceType'] = oi.pop('SourceType', '0'
                                      if int(oi['Label']) >= 0 else '1')
            vn = {}
            for vi in verify_items:
                if vi['LabelIndex'] == oi['Label']:
                    vn = vi
                    break
            _vn = oi.setdefault('VerifiedNodule', {'labelIndex': oi['Label']})
            for k in resultKeys:
                if k in ['CenterX', 'CenterY', 'CenterZ']:
                    _vn[k] = vn.get(k, '0')
                else:
                    v = vn.get(k, 'false')
                    if v == '0':
                        v = 'false'
                    elif v == '1':
                        v = 'true'
                    _vn[k] = v
            oi = OrderedDict(sorted(oi.items(), key=lambda x: x[0]))

            sliceMask = oi.get('mask', {}).get('sliceMask')
            if sliceMask:
                sliceMask['version'] = sliceMask.pop('item_version', '0')
            else:  # 给没有自动分割的新增结节补充中心坐标
                for k in ['CenterX', 'CenterY', 'CenterZ']:
                    oi[k] = _vn[k]
            nodule_items.append(oi)  # 将item插入json
        for mi in missed_items:  # MissedNodules只有中心坐标
            oi = {'Label': mi['LabelIndex'], 'sourceType': '1'}
            vn = oi.setdefault('VerifiedNodule',
                               {'labelIndex': mi['LabelIndex']})
            for k in resultKeys:
                if k in ['CenterX', 'CenterY', 'CenterZ']:
                    oi[k] = vn[k] = mi.get(k, '0')
                else:
                    v = mi.get(k, 'false')
                    if v == '0':
                        v = 'false'
                    elif v == '1':
                        v = 'true'
                    vn[k] = v
            nodule_items.append(oi)
        addition = root.get('AdditionalDiseases')
        if addition:
            if isinstance(addition, list):
                self.jsonData['AdditionalDiseases'] = addition[-1]
            else:
                self.jsonData['AdditionalDiseases'] = addition
        nodules['count'] = str(len(nodule_items))

        if root.get('BJCHTables_CTResult'):
            self.jsonData['BJCH_CTResult'] = copy.deepcopy(DEFAULT_RESULT)
            for i in range(13):
                table = self.jsonData['BJCH_CTResult']['Table{}'.format(i + 1)]
                for k, v in root.get('BJCHTables_CTResult')['Table{}'.format(
                        i)].items():
                    if v == 'Null':
                        pass
                    else:
                        lst = eval(v)
                        for it in lst:
                            if isinstance(it, tuple):
                                table[k][it[1]] = 'True'
                            else:
                                table[k][-1] = it

    def write(self, filename=None):
        # self._modified = False
        _filename = filename or self.__fileName
        if not _filename:
            return
        self.unparse(self.jsonData, _filename)
        self.__fileName = _filename

    def unparse(self, data, filename):
        with open(filename, 'w') as fp:
            json.dump(data, fp, indent=4)


def ConvertXmlFile(tool, xmlFileName):
    lsFile = os.path.splitext(xmlFileName)
    if lsFile[1] != '.xml':
        return

    jsonFileName = lsFile[0] + '.json'

    tool.xml2json(xmlFileName)
    tool.write(jsonFileName)
    print('Convert {} to {}'.format(xmlFileName, jsonFileName))


def TravDir(tool, rootdir):
    filelist = os.listdir(rootdir)
    for i in range(0, len(filelist)):
        path = os.path.join(rootdir, filelist[i])
        if os.path.isdir(path):
            TravDir(tool, path)
        if os.path.isfile(path):
            ConvertXmlFile(tool, path)
    print('All done!')


if __name__ == '__main__':

    tool = ToolXml2Json()
    path = sys.argv[1]
    if os.path.isdir(path):
        TravDir(tool, path)
    if os.path.isfile(path):
        ConvertXmlFile(tool, path)
