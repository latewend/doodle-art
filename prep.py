from PIL import Image, ImageOps
import numpy as np


rotations = [x for x in range(10,350,10)]
def getTransformedimges(path):
    img = Image.open(path)
    img = img.convert("RGBA")

    newData = []
    for item in img.getdata():
        if item[0] >= 150 and item[1] >= 150 and item[2] >= 150:
            newData.append((255, 255, 255, 0))
        else:
            r = (1 - item[2])
            newData.append((r,r,r,255))

    img.putdata(newData)
    bb = img.getbbox()
    newimg = img.crop(bb)
    longest = np.clip((np.max([newimg.size]))*0.6,20,100)
    print(longest)
    newimg.thumbnail((longest,longest))

    length = int(np.ceil(np.sqrt(newimg.size[0]*newimg.size[0] + newimg.size[1]*newimg.size[1])))
    new_img = Image.new(newimg.mode, ( length, length), (255, 255, 255,0))
    new_img.paste(newimg,(length//2 - newimg.size[0]//2,length//2 - newimg.size[1]//2))
    images = [new_img]
    for a in rotations:
        images.append(new_img.rotate(a))
    return(img.crop(bb), images)

# test = getTransformedimges("images/test6.jpeg")
# newData = np.array(test[1][0].getchannel(3))

# img = Image.fromarray(np.uint8(newData) , 'L')
# img.show()
# ImageOps.invert(img).save("images/test16.png")
# test[1][0].save("images/test10.png")
