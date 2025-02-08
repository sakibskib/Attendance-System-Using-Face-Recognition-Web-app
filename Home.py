import streamlit as st
import face_rec
st.set_page_config(page_title='Attendance System', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='auto')


st.header('Attendance System using Face Recognition')

with st.spinner('Loading Models and Connecting to Redis Db...'):
    import face_rec
st.success('Model loaded successfully')
st.success('Redis Db connected successfully')