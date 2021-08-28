import json
from warnings import filterwarnings
import pytesseract #pip install pytesseract 
import cv2 #pip install opencv-python
import numpy as np
import sys
import re
import os
from PIL import Image #pip install Pillow
import ftfy #pip install ftfy
import pan_read
import aadhar_read
import io
from difflib import SequenceMatcher 
from PIL import Image, ImageEnhance
import face_recognition # pip install cmake #pip install face_recognition
import imgfeature
import pullmatch

unicode:any

pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#aadhaar
# filename = "naren.png"
# filename1 = './known/naren.png'
filename = "baranee.png"
filename1 = './known/bro.png'
# filename = "naren.png"
# filename1 = './known/naren.png'
# filename = "ramesh.png"
# filename1 = './known/rame.png'
# filename = "nancy.png"
# filename1 = './known/nanc.png'


#PAN
# filename = "pannar.png"
# filename1 = './known/naren.png'
# filename = "panram.jpg"
# filename1 = './known/rame.png'
# filename = "pannan.png"
# filename1 = './known/nanc.png'
# filename="dummy-pancard.jpg"

#
im = Image.open(filename)
enhancer = ImageEnhance.Sharpness(im)

factor = 1
im_s_1 = enhancer.enhance(factor)
im_s_1.save('sharpened-image.png', quality=100)
# img = cv2.imread('sharpened-image.png')
img = cv2.imread(filename)
img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    

kernel = np.ones((1, 1), np.uint8)    
img = cv2.dilate(img, kernel, iterations=1)    
img = cv2.erode(img, kernel, iterations=1)
img=cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                    # Read image
imS = cv2.resize(img, (960, 540))                # Resize image
cv2.imshow("output", imS)                       # Show image
cv2.waitKey(0)       



var = cv2.Laplacian(img, cv2.CV_64F).var()
# print(var)

if var < 100:
    print("Image is Too Blurry....")
    k= input('Press Enter to Exit.')
    exit(1)



text = pytesseract.image_to_string(img, lang = 'eng')

text_output = open('output.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('output.txt', 'r', encoding='utf-8')
text = file.read()

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)

print(text)


if "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
    data = pan_read.pan_read_data(text)
    scanned=True
    # filename1 = './known/nanc.png'
    # validation1 = pullmatch.imgfeat(filename,filename1)
    # if validation1 == "VALID":
    #     data = pan_read.pan_read_data(text)
    #     scanned=True
    # else:
    #     print("Document validation failed")
    #     exit(0)

elif "male" in text.lower():
   
    validation1 = imgfeature.imgfeat(filename,filename1)
    if validation1 == "VALID":
        data = aadhar_read.adhaar_read_data(text)
        scanned=True
    else:
        print("Document validation failed")
        exit(0)

else:
    print("Can't Indentify the Document Contents")

try:
    
    to_unicode = unicode
except NameError:
    to_unicode = str
if scanned==True:
    with io.open('info.json', 'w', encoding='utf-8') as outfile:
        data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(data))

    with open('info.json', encoding = 'utf-8') as data:
        data_loaded = json.load(data)
else:
    print("Not Properly Scanned. Try Uploading a better quality Image")    

if data_loaded['ID Type'] == 'PAN':
    print("\n---------- PAN Details ----------")
    print("\nPAN Number: ",data_loaded['PAN'])
    print("\nName: ",data_loaded['Name'])
    print("\nFather's Name: ",data_loaded['Father Name'])
    print("\nDate Of Birth: ",data_loaded['Date of Birth'])
    print("\n---------VERIFICATION------------------------")
        
    PAN_Number=  "FHPPB8226J"
    if SequenceMatcher(None, PAN_Number.lower(), data_loaded['PAN'].lower()).ratio()>0.6:
        print("verified")
    else:
        print("Check the user or upload a high quality image")
    print("\n------------------------------------")

elif data_loaded['ID Type'] == 'Adhaar':
    print("\n---------- ADHAAR Details ----------")
    print("\nADHAAR Number: ",data_loaded['Adhaar Number'])
    print("\nName: ",data_loaded['Name'])
    print("\nDate Of Birth: ",data_loaded['Date of Birth'])
    print("\nSex: ",data_loaded['Sex'])
    print("\n------------------------------------")



k = input("\n\nPress Enter To EXIT")
exit(0)



