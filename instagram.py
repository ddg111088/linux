# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:16:44 2023

@author: HP
"""

import streamlit as st
page_bg_img ="""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://static.wixstatic.com/media/11062b_54784a6f95eb4ec9a18b8f5d0eafac9f~mv2_d_7113_5041_s_4_2.jpg/v1/fill/w_430,h_305,al_c,q_80,usm_0.66_1.00_0.01/11062b_54784a6f95eb4ec9a18b8f5d0eafac9f~mv2_d_7113_5041_s_4_2.jpg");
background-size: cover;
}
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
right : 2rem;
}
[data-testid="stSidebar"]{
background-image: url("https://i.pinimg.com/originals/94/7c/b0/947cb04d01c88eb3da955104657b89a7.jpg");;
background-size: cover;
}
</style>
"""
makr = st.markdown(page_bg_img,unsafe_allow_html=True)
abc = st.sidebar.title("User input")
name = st.sidebar.text_input("Enter word")
date = st.sidebar.date_input("Enter start Date ")
E_date = st.sidebar.date_input("Enter End Date ")
Tweets_Count = st.sidebar.number_input("Ender Number of Days")
