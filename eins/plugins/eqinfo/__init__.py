import nonebot
from json import dumps
from .api import InfoParser
from configparser import ConfigParser

config = ConfigParser()
config.read('eins\\plugins\\eqinfo\\config.ini')
gids = eval(config['EINS']['gids'])

@nonebot.scheduler.scheduled_job('interval', seconds = 30)
async def getMessage():
    bot = nonebot.get_bot()
    i = InfoParser()
    latestList = [i.jma_info, i.ceic_info, i.nhk_img]
    storedList = [''] * len(latestList)
    
    for i in range(0, len(latestList)):
        if storedList[i] != latestList[i] and latestList[i] != '':
            storedList[i] = latestList[i]
            info = storedList[i]
            
            if not isinstance(info, dict):
                message = info
            else: # 将数据构造为地图卡片的json格式
                message = {
                        "app": "com.tencent.map",
                        "desc": "地图",
                        "view": "Share",
                        "ver": "0.0.0.1",
                        "prompt": f"地震情报 {info['Magnitude']} {info['Location']}",
                        "appID": "",
                        "sourceName": "",
                        "actionData": "",
                        "actionData_A": "",
                        "sourceUrl": "",
                        "meta": {
                            "Share": {
                                "locSub": f"地震情报 {info['Magnitude']} {info['Depth']} {info['OriginTime']}",
                                "lng": info['Longitude'],
                                "lat": info['Latitude'],
                                "zoom": 8,
                                "locName": f"{info['Magnitude']} {info['Location']}"
                            }
                        },
                        "config": {
                            "forward": True,
                            "autosize": 1
                        },
                        "text": "",
                        "sourceAd": "",
                        "extra": ""
                    }        
        else:
            message = ''
        
        if message and isinstance(info, dict):
            try:
                message = nonebot.MessageSegment.json(dumps(message))
                for gid in gids:
                    await bot.send_group_msg(group_id=gid, message=message)
            except nonebot.CQHttpError:
                pass
            
        if message and isinstance(info, str):
            try:
                message = nonebot.MessageSegment.image(file=message)
                for gid in gids:
                    await bot.send_group_msg(group_id=gid, message=message)
            except nonebot.CQHttpError:
                pass
       
    return ''