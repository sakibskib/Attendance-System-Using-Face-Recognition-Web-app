import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

st.set_page_config(page_title='Predictions',layout='centered')
st.subheader('Real Time Attendance System')



#Retrive the data from the database
with st.spinner('Retriving data from the redis database...'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)
st.success('Data retrived successfully')
# Real time prediction

#time
waitTime = 60 # time in seconds
setTime = time.time() 
realtimepred = face_rec.RealTimePred() # real time prediction class


#streamlit web rtc 

#call back function
def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array 
    #operations that you can perform on the array
    #flipped = img[::-1,:,:]
    pred_img = realtimepred.face_prediction(img,redis_face_db,'facial_features',['Name','Role'], thresh=0.5)
    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        #realtimepred.reset_dict()
        setTime = time.time() #reset time
        print('Logs saved to redis db')

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")
 

webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback)