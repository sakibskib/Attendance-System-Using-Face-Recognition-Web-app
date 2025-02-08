import streamlit as st
from Home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

st.set_page_config(page_title='Registration Form',layout='centered')
st.subheader('Registration Form')

## init registration form class
registration_form = face_rec.RegistrationForm()

#step 1 collect person name and role 
#form
person_name = st.text_input(label='Name', placeholder='Enter your name')
role = st.selectbox(label='Select Your Role',options=['Student','Teacher'])

# step 2 collect facial embedding of that person 
def video_callback_fn(frame):
    img = frame.to_ndarray(format="bgr24")
    reg_img, embedding = registration_form.get_embedding(img)

    if embedding is not None:
        with open('face_embedding.txt', mode='ab') as f:
            np.savetxt(f, embedding)



    return av.VideoFrame.from_ndarray(reg_img, format="bgr24")
webrtc_streamer(key="registration", video_frame_callback=video_callback_fn)


#step 3 save the data in redis database

if st.button('Submit'):
    return_val =registration_form.save_data_in_redis_db(person_name,role)
    if return_val == True:
        st.success(f"{person_name} registered successfully")
    elif return_val == 'name_false':
        st.error('Please enter a valid name')
    elif return_val == 'file_false':
        st.error('Please collect facial embedding first')
