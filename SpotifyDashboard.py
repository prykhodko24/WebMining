# %% Importing crucial libabaries
pip install plotly-express
pip install pandas openpyxl
pip install streamlit
import streamlit as st 
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import base64
import os
from pathlib import Path

# %%
path = Path(__file__).parent
# Use file protocol to load the image
image_url = f"file://{os.path.join(str(path), 'Spotify-logo.png')}"

print(path)
print(image_url)
# set page confguration with image
st.set_page_config(page_title="Spotify dashboard", page_icon=image_url, layout="wide")
# %%
custom_css = """
    <style>
        .css-1okhskf {
            text-align: center;
            font-size: 22px !important;
        }
    </style>
"""
# %%
# Display the title with custom CSS
st.markdown(custom_css, unsafe_allow_html=True)
st.title("Spotify Dashboard")
# %%
st.write("""
    Welcome to the Spotify Dashboard!
     
    Spotify is a leading global music streaming platform that offers users access to an extensive library of songs, albums, and playlists from various genres and artists. With its user-friendly interface and personalized recommendations, Spotify revolutionizes the way people discover, enjoy, and share music. The platform supports both free and premium subscription models, providing users with a seamless and immersive audio streaming experience across multiple devices.
    
    Here, you can analyze and explore Spotify data. 
    
     If you want to dive into details, please select a section from the sidebar on the left.
""")

# %% Spotify gif
file_path = os.path.join(str(path), 'giphy.gif')
image_url = f"file://{os.path.join(str(path), 'Spotify-logo.png')}"
file_ = open(file_path, "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; height: 100vh;">'
    f'   <h1 style="font-size: 48px; margin-bottom: 10px;"> </h1>'
    f'   <img src="data:image/gif;base64,{data_url}" alt="spotify gif" style="width: 20%; margin-bottom: 5px;">'
    f'</div>',
    unsafe_allow_html=True,
)
# %%
st.sidebar.success("Select a section above")
# %%
