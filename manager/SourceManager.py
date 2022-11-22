from PIL import Image, ImageDraw, ImageFont

class SourceManager:
    def __init__(self):
        self.idle_src = ["idle1.png", "idle2.png","idle3.png","idle4.png","idle5.png","idle6.png","idle7.png","idle8.png"]
        self.jump_src = ["jump1.png", "jump2.png","jump3.png","jump4.png","jump5.png","jump6.png","jump7.png","jump8.png", "jump9.png", "jump10.png", "jump11.png", "jump12.png"]

    def importIdel(self):
        assets = []
        for src in self.idle_src:
            assets.append(Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/"+src).resize((50,50)))
        return assets

    def importJump(self):
        assets = []
        for src in self.jump_src:
            assets.append(Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/"+src).resize((50,50)))
        return assets