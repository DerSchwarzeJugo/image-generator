from matplotlib import pyplot as plt
from PIL import Image, ImageChops, ImageFilter


imageBg = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/Backgrounds/020.png"
imageHa = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/HandAcc/016.png"
imageMa = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/MouthAcc/012.png"
imageBo = "/mnt/c/Users/der_p/gimpProjects/FatPlat1/Body/008.png"

bg = Image.open(imageBg)
ha = Image.open(imageHa)
ma = Image.open(imageMa)
bo = Image.open(imageBo)


bg.paste(ha, (0,0), ha)
bg.paste(ma, (0,0), ma)
bg.paste(bo, (0,0), bo)
bg.save("bg.png")

