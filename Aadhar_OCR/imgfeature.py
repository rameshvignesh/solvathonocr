import cv2
from PIL import Image, ImageEnhance
import face_recognition
import numpy as np

def imgfeat(filename1,filename2):

    img1 = cv2.imread('./unknown/ramesh.PNG',0)
    img2 = cv2.imread(filename1,0)

    orb = cv2.ORB_create(nfeatures=8000)

    kp1,des1 = orb.detectAndCompute(img1,None)
    kp2,des2 = orb.detectAndCompute(img2,None)

    imgkp1 = cv2.drawKeypoints(img1,kp1,None)
    imgkp2 = cv2.drawKeypoints(img2,kp2,None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)

    good = []

    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    print(len(good))

    if len(good) >= 38:
        print("Valid AADHAR CARD")    

        im = Image.open(filename1)
        enhancer = ImageEnhance.Sharpness(im)

        factor = 2
        im_s_1 = enhancer.enhance(factor)
        im_s_1.save('sharpened-image.png', quality=100)

        image = face_recognition.load_image_file('sharpened-image.png')
        face_locations = face_recognition.face_locations(image)

        image_of_find = face_recognition.load_image_file(filename2)
        find_face_encoding = face_recognition.face_encodings(image_of_find)[0]

        for face_location in face_locations:
            top, right, bottom, left = face_location
            topper = top
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.save(f'{top}.jpeg', quality=100)

        topper = str(top) + '.jpeg'
        print(topper)

        im = Image.open(topper)
        enhancer = ImageEnhance.Sharpness(im)

        factor = 2
        im_s_1 = enhancer.enhance(factor)
        im_s_1.save('sharpened-image.png', quality=100)

        unknown_image = face_recognition.load_image_file('sharpened-image.png')
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces(
        [find_face_encoding], unknown_face_encoding,tolerance=0.6)

        if results[0]:
            print('This is Same person')
            return "VALID"
        else:
            print('This is NOT Same person')
            return "INVALID"

    else:
        print("INVALID")
        return "INVALID"

    cv2.waitKey(0)