import os
import requests
import time
import random
from PIL import Image, ImageDraw


class MemeTool:

    def __init__(self):
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.drawPath = os.path.join(self.basePath, "draw")
        self.resultDirPath = os.path.join(self.basePath, "result")
        if not os.path.exists(self.resultDirPath):
            os.mkdir(self.resultDirPath)
        self.avatarDirPath = os.path.join(self.drawPath, "avatar")
        if not os.path.exists(self.avatarDirPath):
            os.mkdir(self.avatarDirPath)

    def getAvatar(self, QQ, size, needClipToCircle: bool = True):
        """
        获取头像
        :param QQ: qq号
        :param size: 头像规格
        :param needClipToCircle: 是否转换成圆形，默认为否
        :return: 头像
        """

        if QQ.isdigit():
            theQQ = int(QQ)
        else:
            return None

        url = "http://q1.qlogo.cn/g?b=qq&nk={}&s=640".format(theQQ)
        r = requests.get(url)
        if r.status_code != 200:
            return None
        avatarPath = os.path.join(self.avatarDirPath, "{}.jpg".format(theQQ))
        with open(avatarPath, "wb") as f:
            f.write(r.content)
        avatar = Image.open(avatarPath)
        avatar = avatar.resize(size)
        avatar = avatar.convert("RGBA")
        if needClipToCircle:
            circle = Image.new('L', avatar.size, 0)  # 创建一个黑色正方形画布
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)  # 画一个白色圆形
            avatar.putalpha(circle)  # 白色区域透明可见，黑色区域不可见
        return avatar

    def getNeed(self, QQ):
        avatar = self.getAvatar(QQ, (113, 113), needClipToCircle=False)
        if avatar is None:
            return None
        frontImage = Image.open(os.path.join(self.drawPath, "need.png"))
        need = Image.new("RGBA", frontImage.size, (255, 255, 255))
        need.paste(avatar, (328, 232), avatar.split()[3])
        need.paste(frontImage, (0, 0), frontImage.split()[3])
        resultPath = os.path.join(self.resultDirPath, "{}.png".format(time.time()))
        need.save(resultPath)
        return resultPath


if __name__ == '__main__':
    tool = MemeTool()
    tool.getNeed('781827926').show()
