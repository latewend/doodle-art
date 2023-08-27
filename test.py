import numpy as np
from PIL import Image, ImageOps

from normxcorr2 import normxcorr2


def main():
# print("what")
    img = Image.open("images/image.jpeg")
    # print("what")
    s1 = Image.open("images/s1.png")
    s2 = Image.open("images/s2.png")
    s3 = Image.open("images/s3.png")
    s4 = Image.open("images/s4.png")
    s5 = Image.open("images/s5.png")
    s6 = Image.open("images/s6.png")
    s7 = Image.open("images/s7.png")
    s8 = Image.open("images/s8.png")
    img3 = Image.open("images/test18.png")
    # print("what")
    r1 = normxcorr2(np.array(s1.getchannel(0)), np.array(img.getchannel(0)),"same")
    r2 = normxcorr2(np.array(s2.getchannel(0)), np.array(img.getchannel(0)),"same")
    r3 = normxcorr2(np.array(s3.getchannel(0)), np.array(img.getchannel(0)),"same")
    r4 = normxcorr2(np.array(s4.getchannel(0)), np.array(img.getchannel(0)),"same")
    r5 = normxcorr2(np.array(s5.getchannel(0)), np.array(img.getchannel(0)),"same")
    r6 = normxcorr2(np.array(s6.getchannel(0)), np.array(img.getchannel(0)),"same")
    r7 = normxcorr2(np.array(s7.getchannel(0)), np.array(img.getchannel(0)),"same")
    r8 = normxcorr2(np.array(s8.getchannel(0)), np.array(img.getchannel(0)),"same")


    res2 = normxcorr2(np.array(img3.getchannel(0)), np.array(img.getchannel(0)))

    # te = np.max(a)
    # print(te)


    # for c in a:
    #     print(c)
    test = Image.fromarray(np.uint8((np.clip(r1,0,1))*255))


    test.show()


def assemble(scores, items, og,count,thresh=0.3, length=1):
    imgsize = og.size
    order = []
    lastcorners = None


    while True:
        
        cmax = -1
        rcmax = -1
        maxLoc = 0
        for i,a in enumerate(scores):
            tmax = np.max(a) * (1 - (count[i//36]/(sum(count) + 1) ))
            if tmax > cmax:
                cmax = tmax
                rcmax = np.max(a)
                maxLoc = i
        if cmax < thresh:
            break
        if(len(order) % 100 == 0 ):
            print(len(order),cmax)

        loc = np.where(scores[maxLoc] == rcmax)
        csize = items[maxLoc].size
        corners = [np.clip(loc[1][0] - csize[1]//2 ,0,imgsize[0]),
                   np.clip(loc[1][0] +  csize[1]//2,0,imgsize[0]),
                   np.clip(loc[0][0] - csize[0]//2  ,0,imgsize[1]),
                   np.clip(loc[0][0] + csize[0]//2 ,0,imgsize[1])]

        for i in range(0,len(items)):
            maskMe(scores[i*length:i*length+length],
                   items[i].size,
                   imgsize,corners)
        # maskMe(scores,
        #     items[0].size,
        #     imgsize,corners)
            
        order.append((maxLoc,(loc[1][0] - csize[0]//2),(loc[0][0] - csize[1]//2) ))
        count[maxLoc//36] += 1

        # test = Image.fromarray(np.uint8((np.clip(scores[0],0,1))*255))
        # test.show()
        
        if corners == lastcorners:
            print(corners,loc,csize)
            break
        lastcorners = corners
    return (order,count)




def maskMe(t,ogsize,imgsize,mcorners):
    # sx = np.clip(mcorners[0] - ogsize[0] ,0,imgsize[0])
    # ex = np.clip(mcorners[1] + ogsize[0] ,0,imgsize[0])
    # sy = np.clip(mcorners[2] - ogsize[1] ,0,imgsize[1])
    # ey = np.clip(mcorners[3] + ogsize[1] ,0,imgsize[1])

    sx = np.clip(mcorners[0]  ,0,imgsize[0])
    ex = np.clip(mcorners[1]  ,0,imgsize[0])
    sy = np.clip(mcorners[2]  ,0,imgsize[1])
    ey = np.clip(mcorners[3]  ,0,imgsize[1])
    for a in t:
        a[sy:ey,sx:ex] = -1


# myimages = [s1,s2,s3,s4,s5,s6,s7,s8]

# p = (assemble([r1,r2,r3,r4,r5,r6,r7,r8], myimages, img))

# test = Image.fromarray(np.uint8((np.clip(r1,0,1))*255))

# print(np.max(r1))
# test.show()


# newimage = Image.new('RGB', img.size,(255, 255, 255))
# print(len(p))

# for a in p:
#     newimage.paste(myimages[a[0]],[a[1],a[2]])

# newimage.show()





