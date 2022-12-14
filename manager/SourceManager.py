from PIL import Image, ImageDraw, ImageFont

#애니메이션을 위한 이미지들을 한번에 import 합니다.
#시간이 오래 걸리는 작업이기 때문에 매 루프에서 하는 게 아닌 시작과 동시에 한번만 호출됩니다.
class SourceManager:
    def __init__(self):
        self.idle_src = ["idle1.png", "idle2.png","idle3.png","idle4.png","idle5.png","idle6.png","idle7.png","idle8.png"]
        self.jump_src = ["jump1.png", "jump2.png","jump3.png","jump4.png","jump5.png","jump6.png","jump7.png","jump8.png", "jump9.png", "jump10.png", "jump11.png", "jump12.png"]
        self.dust_src = ["FX001_01.png", "FX001_02.png", "FX001_03.png", "FX001_04.png", "FX001_05.png"]

    def importIdel(self):
        assets = []
        for src in self.idle_src:
            assets.append(Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/"+src).resize((30,30)))
        return assets

    def importJump(self):
        assets = []
        for src in self.jump_src:
            assets.append(Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/"+src).resize((30,30)))
        return assets

    def importDust(self):
        assets = []
        for src in self.dust_src:
            assets.append(Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/"+src)
                          .resize((30,30))
                          .convert("RGBA"))
        return assets
