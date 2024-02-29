import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import easyocr
import time
import threading
#import qrcode
#qr_code=qrcode.make('Hello World')
#qr_code.save('QR.png')


st.title('Optical Character Recognizer')

st.markdown (

    '''
    <style>
    [data-testid='stSidebar'][aria-expanded='true']>div:first-child{
        width:350px
    }

    [data-testid='stSidebar'][aria-expanded='false']>div:first-child{
        width:350px
        margin-left:-350px
    }
    </style>
    ''',
    unsafe_allow_html=True,
)


with open('./access.txt', 'r') as f:
    authorized_users = [l for l in f.readlines()][0]
    #print(type(authorized_users))
    f.close()


st.sidebar.markdown('**Upload an Image**')
    
    # upload file
file = st.sidebar.file_uploader('', type=['png', 'jpg', 'jpeg'])
    # load image
if file:
    image = Image.open(file).convert('RGB')
    image_array = np.asarray(image)

    qr_info = decode(image_array)

    for qr in qr_info:

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        img = cv2.rectangle(image_array, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),(0, 255, 0), 3)

        img = cv2.polylines(image_array, [np.array(polygon)], True, (0, 0, 255), 3)
            #print(type(data.decode()))

        if data.decode() == authorized_users:
            cv2.putText(image_array, 'ACCESS GRANTED', (rect.left, rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            st.sidebar.image(img, use_column_width=True)

            st.markdown('Please insert a file')
            file_01 = st.file_uploader('', type=['png', 'jpg'])

            if file_01:
                im = Image.open(file_01).convert('RGB')
                im = np.asarray(im)

                    # instance text detector
                reader = easyocr.Reader(['en'], gpu=False)

                    # detect text on image
                text_ = reader.readtext(im)

                threshold = 0.25
                    # draw bbox and text
                for t_, t in enumerate(text_):
                    #print(t)

                    bbox, text, score = t

                    if score > threshold:
                        cv2.rectangle(im, bbox[0], bbox[2], (0, 255, 0), 5)
                        cv2.putText(im, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

                st.image(im, use_column_width=True)


        else:
            cv2.putText(image_array, 'ACCESS DENIED', (rect.left, rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            st.sidebar.image(img, use_column_width=True)
            

            


    



