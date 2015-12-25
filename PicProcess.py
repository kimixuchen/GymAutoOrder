from PIL import Image
from StringIO import StringIO

#Constances
BACKCOLOR = 255
TEXTCOLOR = 0
OriImgNum1_Left = 7
OriImgNum1_Upper = 3
OriImgNum1_Right = 16
OriImgNum1_Lower = 16
OriImgNums_Interval = 13
ModelWidth = 9
ModelHeight = 13
Deviation = 50
N = 100000

def Binarized(Picture):
	imgB = Picture.copy()
	Pixels = Picture.load();
	PixelsB = imgB.load();
	(Width, Height) = Picture.size
	Threshold = 140
	for i in xrange(Height):
		for j in xrange(Width):
			if Pixels[j, i] > Threshold:
				PixelsB[j, i] = BACKCOLOR
			else:
				PixelsB[j, i] = TEXTCOLOR
				
	return imgB
	
def getResultFromImage(img):
	imgL = img.convert('L')
		
	imgB = Binarized(imgL)
	nums = getNums(imgB)
	
	return nums
		
def cutNumsFromBimg(infilename):
	left = OriImgNum1_Left
	upper = OriImgNum1_Upper
	right = OriImgNum1_Right
	lower = OriImgNum1_Lower
	interval = OriImgNums_Interval
	img = Image.open(infilename)
	for i in range(0, 4):
		box = (left, upper, right, lower)
		region = img.crop(box)
		region.save('%s%s%d%s' % ('NUMS/', infilename[-5], i, '.jpg'))
		left += interval
		right += interval

def getNums(ImgB):
	left = OriImgNum1_Left
	upper = OriImgNum1_Upper
	PixelsB = ImgB.load()
	nums = ''
	num = 0
	for i in range(0, 4):
		max = 0
		for j in range(0, 10):
			similarity = 0
			imgModel = Image.open('%s%i%s'%('Models/', j, '.jpg'))
			PixelsM = imgModel.load()
			for h in xrange(ModelHeight):
				for w in xrange(ModelWidth):
					if abs(PixelsM[w, h] - PixelsB[left+w, upper+h]) < Deviation:
						similarity+=1
					else:
						similarity-=1
			
			if similarity>max:
				max = similarity
				num = j
			
		left += OriImgNums_Interval
		
		nums = '%s%d' % (nums, num)
		
	return nums

def getResutlFromStr(buffer):
	img = Image.open(StringIO(buffer))
	nums = getResultFromImage(img)
	
	return nums
	
