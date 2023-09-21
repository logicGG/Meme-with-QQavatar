import os
import time

import requests
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

    def getAvatar(self, qq, size, needClipToCircle: bool = True):
        """
        获取头像
        :param qq: qq号
        :param size: 头像规格
        :param needClipToCircle: 是否转换成圆形，默认为否
        :return: 头像
        """

        if qq.isdigit():
            theQQ = int(qq)
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

    def getDraw(self, playType, qq):
        if playType == 'need':
            resultPath = self.drawNeed(qq)
        elif playType == 'suck':
            resultPath = self.drawSuck(qq)
        elif playType == 'tie':
            resultPath = self.drawTie(qq)
        elif playType == 'bounce':
            resultPath = self.drawBounce(qq)
        else:
            return None
        return resultPath

    def drawNeed(self, qq):
        avatar = self.getAvatar(qq, (113, 113), needClipToCircle=False)
        if avatar is None:
            return None
        frontImage = Image.open(os.path.join(self.drawPath, "need.png"))
        need = Image.new("RGBA", frontImage.size, (255, 255, 255))
        need.paste(avatar, (328, 232), avatar.split()[3])
        need.paste(frontImage, (0, 0), frontImage.split()[3])
        resultPath = os.path.join(self.resultDirPath, "{}.png".format(time.time()))
        need.save(resultPath)
        return resultPath

    def drawSuck(self, qq):
        avatar = self.getAvatar(qq, (300, 300))
        if avatar is None:
            return None
        inhalePath = os.path.join(self.drawPath, "inhale")
        inhaleImages = []
        positions = [(65, 88), (61, 89), (60, 112), (70, 142), (68, 151), (70, 129), (73, 141), (69, 145), (70, 154),
                     (68, 119), (64, 115), (64, 99)]
        sizes = [(162, 151), (167, 146), (165, 120), (151, 90), (151, 84), (149, 109), (145, 94), (151, 89), (149, 76),
                 (152, 118), (160, 121), (161, 140)]
        for i in range(0, 12):
            frontImage = Image.open(os.path.join(inhalePath, "inhale_{}.png".format(i + 1)))
            img = Image.new("RGBA", frontImage.size, (255, 255, 255))
            theAvatar = avatar.resize(sizes[i])
            img.paste(theAvatar, positions[i], theAvatar.split()[3])
            img.paste(frontImage, (0, 0), frontImage.split()[3])
            inhaleImages.append(img)
        resultPath = os.path.join(self.resultDirPath, "{}.gif".format(time.time()))
        inhaleImages[0].save(resultPath, format="GIF", append_images=inhaleImages[1:], save_all=True, duration=60,
                             loop=0)
        return resultPath

    def drawTie(self, qq):
        avatar = self.getAvatar(qq, (300, 300))
        if avatar is None:
            return None
        snugglePath = os.path.join(self.drawPath, "snuggle")
        snuggleImages = []
        positions = [(77, 257), (82, 271), (82, 271), (81, 261), (64, 243)]
        sizes = [(174, 183), (175, 169), (175, 169), (175, 178), (194, 193)]
        for i in range(0, 5):
            frontImage = Image.open(os.path.join(snugglePath, "snuggle_{}.png".format(i + 1)))
            img = Image.new("RGBA", frontImage.size, (255, 255, 255))
            theAvatar = avatar.resize(sizes[i])
            img.paste(theAvatar, positions[i], theAvatar.split()[3])
            img.paste(frontImage, (0, 0), frontImage.split()[3])
            snuggleImages.append(img)
        resultPath = os.path.join(self.resultDirPath, "{}.gif".format(time.time()))
        snuggleImages[0].save(resultPath, format="GIF", append_images=snuggleImages[1:], save_all=True, duration=110,
                              loop=0)
        return resultPath

    def drawBounce(self, qq):
        avatar = self.getAvatar(qq, (100, 100))
        if avatar is None:
            return None
        bouncePath = os.path.join(self.drawPath, "bounce")
        bounceImages = []
        positions = [(103, 51), (103, 46), (101, 10), (101, 27), (103, 46)]
        sizes = [(35, 35), (35, 35), (39, 35), (38, 37), (35, 35)]
        for i in range(0, 5):
            frontImage = Image.open(os.path.join(bouncePath, "bounce_{}.png".format(i + 1)))
            img = Image.new("RGBA", frontImage.size, (255, 255, 255))
            theAvatar = avatar.resize(sizes[i])
            img.paste(theAvatar, positions[i], theAvatar.split()[3])
            img.paste(frontImage, (0, 0), frontImage.split()[3])
            bounceImages.append(img)
        resultPath = os.path.join(self.resultDirPath, "{}.gif".format(time.time()))
        bounceImages[0].save(resultPath, format="GIF", append_images=bounceImages[1:], save_all=True, duration=70,
                             loop=0)
        return resultPath


if __name__ == '__main__':
    tool = MemeTool()
    Image.open(tool.getDraw('bounce','781827926')).show()
