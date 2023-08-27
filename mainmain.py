
import os 
from PIL import Image, ImageOps,ImageFilter
import numpy as np
from test import assemble
from prep import getTransformedimges
from normxcorr2 import normxcorr2










# for a in unPureDoodles:
#     a.show()


def prococess():
    

    rawoGImage = Image.open("images/final1.jpeg")
    oGImage = ImageOps.grayscale(rawoGImage)
    # oGImage = Image.fromarray(np.array(GoGImage.filter(ImageFilter.FIND_EDGES)))
    oGImage.show()
    newimage = Image.new('LA', oGImage.size,(255,255))
    rawDoodles = os.listdir('images/doodles2/')
    unPureDoodles = [] 
    miniDoodles = [] 

    for d in rawDoodles:
        r = getTransformedimges('images/doodles2/'+ d)
        unPureDoodles.append(r[0])
        miniDoodles = [*miniDoodles,*r[1]]
    neededimg = oGImage
    count = [0 for x in unPureDoodles] 

    # Image.fromarray(np.uint8(255 *(np.clip(normxcorr2(np.array(unPureDoodles[0].getchannel(3)), np.array(rawoGImage.getchannel(0)),"same") * -1,0,1)))).show()
    # print()
    # exit()
    thresh = 0.1
    for i in range(5):

        dodSocores = []
        for mdod in miniDoodles:

            dodSocores.append(normxcorr2(np.array(mdod.getchannel(3)), np.array(neededimg.getchannel(0)),"same"))
        
        (p,count) = assemble(dodSocores,miniDoodles,neededimg,count, thresh)
        print(len(p))
        for a in p:
            newimage.paste(miniDoodles[a[0]],[a[1],a[2]],miniDoodles[a[0]] )
        neededimg = Image.fromarray(np.asarray(oGImage) - np.asarray(newimage.getchannel(0)) )
        newimage.show()

        for mind in miniDoodles:
            longest = np.clip((np.max([mind.size]))*0.666,5,150)
            mind.thumbnail((longest,longest))

prococess()