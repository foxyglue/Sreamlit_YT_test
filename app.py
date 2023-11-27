import pandas as pd
import pickle
from PIL import Image
import streamlit as slt
import plotly.express as px

px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'reds'

# Gambar bisa dari link atau file local
image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/YouTube_social_white_square_%282017%29.svg/1200px-YouTube_social_white_square_%282017%29.svg.png'
# img = Image.open('Youtube.png')

# Displaying the image in the sidebar
slt.sidebar.image(image_url, caption='youtube')

#buka data pickle
with open("used_data.pickle", 'rb') as f:
    data = pickle.load(f)

#input tanggal
min_date = data['trending_date'].min()
max_date = data['trending_date'].max()
start_date, end_date = slt.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

#input kategori
categories = ['All Categories'] + list(data['category'].value_counts().keys().sort_values())
#membuat daftar categories sebelumnya menjadi list krn sebleumnya blm
category = slt.sidebar.selectbox(label='Kategori', options= categories)

#filter
outputs = data[(data['trending_date'] >= start_date) & 
               (data['trending_date'] <= end_date)]
#output yang dihasilkan direntang waktu start dan end
if category != "All Categories":
    outputs = outputs[outputs['category'] == category]
#Jika category bkn ALl, maka category sesuai yang dipilih

#Visualisasi dgn bar chart
slt.header(":video_camera: Channel")
bar_data = outputs['channel_name'].value_counts().nlargest(10)
fig = px.bar(bar_data, color=bar_data, orientation= 'h', title= f"Channel Terpopuler dari kategori {category}", x = "Ketenaran berdasarkan channnel muncul", y= "Nama Channel")
slt.plotly_chart(fig)

# Visualisasi scatter plot
slt.header(":bulb: Engagement")
col1, col2 = slt.columns(2)
metrics_choice = ['like', 'dislike', 'Comment']
choice_1 = col1.selectbox('Horizontal', options= metrics_choice)
choice_2 = col2.selectbox('Vertical', options=metrics_choice)
fig = px.scatter(outputs, x = choice_1, y= choice_2,
                 size= 'view', hover_name= 'channel_name',
                 hover_data= ['title'], 
                 title= f"Engagement of {choice_1.title()} and {choice_2.title()}")
slt.plotly_chart(fig) #menampilkan chart yang tlh dibuat plotly di streamlit
