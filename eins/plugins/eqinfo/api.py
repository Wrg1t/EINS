'''
用于获取最新地震情报的脚本

数据源: 
    https://news.ceic.ac.cn
    https://www.jma.go.jp
    https://www3.nhk.or.jp
'''

import requests
import xml.etree.ElementTree as e
from urllib3 import disable_warnings
disable_warnings()


class InfoParser:
    def __init__(self):
        self.ceic_url = 'https://news.ceic.ac.cn/ajax/google'
        self.jma_root_url = 'https://www.jma.go.jp/bosai/quake/data/'
        self.jma_url = 'https://www.jma.go.jp/bosai/quake/data/list.json'
        self.nhk_url = 'https://www3.nhk.or.jp/sokuho/jishin/data/JishinReport.xml'
        self.nhk_root_url = 'https://www3.nhk.or.jp/sokuho/jishin/data/'

    def getJson(self, url):
        max_retries = 0
        content = ''
        
        while max_retries < 3:
            try:
                r = requests.get(url, verify=False, timeout=3)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                content = r.json()
                break
            except:
                max_retries += 1
            
        return content
    
    def getContent(self, url):
        max_retries = 0
        content = ''
        
        while max_retries < 3:
            try:
                r = requests.get(url, verify=False, timeout=3)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                content = r.text
                break
            except:
                max_retries += 1

        return content
    
    @property
    def jma_info(self):
        data = self.getJson(self.jma_url)
        try:
            child = data[0]['json']
            url = self.jma_root_url + child

            data = self.getJson(url)
            coord = data['Body']['Earthquake']['Hypocenter']['Area']['Coordinate']
            coord = self.parseCoord(coord)

            info = {
                'Magnitude': 'M'+data['Body']['Earthquake']['Magnitude'],
                'OriginTime': data['Body']['Earthquake']['OriginTime'][:-6].replace('T', ' ')+' ' + 'JST',
                'ReportedTime': data['Head']['ReportDateTime'][:-6].replace('T', ' ')+' ' + 'JST',
                'Longitude': coord['Longitude'],
                'Latitude': coord['Latitude'],
                'Depth': coord['Depth']+'km',
                'Location': data['Body']['Earthquake']['Hypocenter']['Area']['Name'],
                'Source': 'JMA'
            }
            content = info
        except:
            content = ''

        return content
        
    @property
    def ceic_info(self):
        data = self.getJson(self.ceic_url)
        try:
            info = data[-1]
            info = {
                'Magnitude': 'M'+info['M'],
                'OriginTime': info['O_TIME']+' '+'CST',
                'ReportedTime': info['SAVE_TIME']+' '+'CST',
                'Longitude': info['EPI_LON'],
                'Latitude': info['EPI_LAT'],
                'Depth': info['EPI_DEPTH']+'.0km',
                'Location': info['LOCATION_C'],
                'Source': 'CEIC'
            }
            content = info
        except:
            content = ''
            
        return content
    
    @property
    def nhk_img(self):
        data = self.getContent(self.nhk_url)
        try:
            data = e.fromstring(data)
            url = data[0][0].get("url")
            
            data = self.getContent(url)
            data = e.fromstring(data)
            img_url = self.nhk_root_url + data[1][0].text[5:]
            
            content = img_url
        except:
            content = ''
        
        return content
    
    def getJMA(self):
        return self.jma_info

    def getCEIC(self):
        return self.ceic_info

    def parseCoord(self, coord):
        coord = coord[:-1] + '+' # 将坐标构造成这种形式: "+38.3+141.6-60000+", 以便于进一步解析
        coord_list = []
        data = ''
        flag = 0

        for i in coord:  # 留下"+"或"-"之间的内容, 上方需要在末尾加"+"正是这个原因
            i = str(i)

            if i == '+' or i == '-':
                flag += 1
                i = ''  # 将"+"和"-"都过滤掉

            data += i # 将过滤下的字符逐个拼接为所需字符串
            if flag == 2:
                coord_list.append(data)
                data = ''
                flag = 1

        depth = int(coord_list[2])
        depth /= 1000
        coord_list[2] = str(depth)
        
        coord = {
            'Longitude': coord_list[1],
            'Latitude': coord_list[0],
            'Depth': coord_list[2]
        }
        return coord

if __name__ == '__main__':
    i = InfoParser()
    print(i.nhk_img)