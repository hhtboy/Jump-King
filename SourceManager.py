from PIL import Image, ImageDraw, ImageFont

class SourceManager:

    def importSrc():
        assets = []
        asset_src = ["frog-idle-1.png","frog-idle-1.png", "frog-idle-2.png","frog-idle-2.png", "frog-idle-3.png", "frog-idle-3.png","frog-idle-4.png","frog-idle-4.png", "frog-jump-1.png", "frog-fall.png"]
        for src in asset_src:
            assets.append(Image.open(r"/home/kau-esw/Documents/github/Jump-King/assets/"+src))
        return assets