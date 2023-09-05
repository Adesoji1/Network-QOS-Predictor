# app.py

import streamlit as st
import pickle
from geopy.geocoders import Nominatim
from sklearn.preprocessing import LabelEncoder

# Load the trained model and label encoder
model = pickle.load(open('model.pkl', 'rb'))
le_operator = pickle.load(open('le_operator.pkl', 'rb'))

# Function to categorize network quality (as provided in your script)
def categorize_quality(sinr, rsrq, rsrp):
    if sinr > 20 and rsrq > -8:
        return 'Excellent'
    elif -12 < rsrq < -7 and sinr > 20:
        return 'Good'
    elif -12 < rsrq < 0 and 20 >= sinr >= 10:
        return 'Good'
    elif -12 < rsrq < 0 and 10 > sinr >= 2:
        return 'Fair'
    elif -15 < rsrq <= -12 and sinr >= 2:
        return 'Fair'
    elif rsrq < 0 and -5 <= sinr <= 1:
        return 'Usable'
    elif -18 < rsrq <= -15 and sinr >= -5:
        return 'Usable'
    elif rsrq <= -17 and sinr > -6:
        return 'Usable'
    elif rsrq >= -17 and sinr < -5:
        return 'Poor'
    elif rsrq < -17 and sinr < -5:
        return 'Poor'
    elif rsrp < -118 and rsrq <= -15:
        return 'Poor'
    else:
        return 'Unknown'

# Function to predict SINR, RSRQ, RSRP for a given network operator and location
def predict_values(network_operator, location):
    geolocator = Nominatim(user_agent="myGeocoder")
    #geolocator = Nominatim(user_agent="geoapiExercises")
    location_geo = geolocator.geocode(location)
    if network_operator not in le_operator.classes_:
        network_operator = 'others'
    encoded_operator = le_operator.transform([network_operator])
    sinr, rsrq, rsrp = model.predict([[encoded_operator[0], location_geo.longitude, location_geo.latitude]])[0]
    quality = categorize_quality(sinr, rsrq, rsrp)
    return location_geo, sinr, rsrq, rsrp, quality

    return location_geo, sinr, rsrq, rsrp, quality



# Page configurations
st.set_page_config(
    page_title='Mobile Network Qos Predictor ',
    page_icon="Enextgen.png",  # Replace with the path to your company logo
    layout='centered',
    initial_sidebar_state="collapsed"
)



# Feedback section
st.markdown(
    """
    <img src="https://imgs.search.brave.com/IlYmMwAmIysfqcBk9FTuNMDElcxz_1vBX1XAvULyOgo/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTgy/NzkwNzE5L3Bob3Rv/L25pZ2VyaWFuLWZs/YWcuanBnP3M9NjEy/eDYxMiZ3PTAmaz0y/MCZjPTh3YlpYREFm/aE5kS3UweHNSNmtR/em96c2g3c2VjdVo5/dUFzaklMV3F4NTQ9" width="30" height="20"> <img src="https://enextwireless.com/wp-content/uploads/2020/04/logo2.png" width="30" height="20">  
   ### 🤖 We'd love to have your feedback  🗼!
    Mail us at [info@enextgenwireless.com](mailto:info@enextwireless.com) 
    or visit us at [www.enextgenwireless.com](https://www.enextwireless.com/)
    """,
    unsafe_allow_html=True
)




 #Display the company background image (alternative to CSS background)
st.image("url.png", use_column_width=True)



# Display the title
st.title("Mobile Network Qos Predictor")

# Input fields
network_operator = st.selectbox(
    "Network Operator:",
    ["Verizon", "AT&T", "T-Mobile", "Airtel", "Glo", "MTN-Stay_Safe", "Others"]
)
location = st.text_input("Location:", "New York")

if st.button("Predict"):
    location_geo, sinr, rsrq, rsrp, quality = predict_values(network_operator, location)
    
    # Display the prediction
    st.write("Location:", location_geo)
    st.write("SINR:", sinr)
    st.write("RSRQ:", rsrq)
    st.write("RSRP:", rsrp)
    st.write("Network Quality:", quality)


# Copyright notice
st.markdown("© Enextgenwireless 2023", unsafe_allow_html=True)
