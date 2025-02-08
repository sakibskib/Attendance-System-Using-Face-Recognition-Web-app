import streamlit as st

from Home import face_rec
st.set_page_config(page_title='Reporting', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='auto')
st.subheader('Reporting log')



#Retrive log data from the redis database
#exract the data from the redis database
name = 'attendance:logs'
def load_logs(name, end=-1):
    logs_list = face_rec.r.lrange(name,start=0,end=end) #extract all the data from the redis database 
    return logs_list


#tabs to show the information
tab1, tab2 = st.tabs(['Registered Data', 'Logs'])

with tab1:
    if st.button('Refresh Data'):
        #Retrive the data from the database
        with st.spinner('Retriving data from the redis database...'):
            redis_face_db = face_rec.retrive_data(name='academy:register')
            st.dataframe(redis_face_db[['Name','Role']])
            st.success('Data retrived successfully')

with tab2:
    if st.button('Refresh logs'):

        st.write(load_logs(name=name))



