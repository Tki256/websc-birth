import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from utils import scrape_day_page
from datetime import datetime


st.title("Birth")
# 誕生日の入力エリアを作成
birthday = st.date_input(
    "Enter your birthday",
    value=datetime(2000, 1, 1),
    min_value=datetime(1900, 1, 1),
    max_value=datetime.today()
)

text, url = scrape_day_page(birthday.month, birthday.day)
st.text(text)
response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)