import nonebot
import eins_config

if __name__ == '__main__':
    nonebot.init(eins_config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        './eins/plugins', # 插件文件夹的路径。
        'eins.plugins'
    )
    nonebot.run()