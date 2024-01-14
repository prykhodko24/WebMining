# %% Importing crucial libabaries
import streamlit as st 
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import base64
from datetime import datetime
from pathlib import Path
# %% ---- Logo update ----
st.sidebar.success("Select a section above")

path = Path(__file__).parent
# Use file protocol to load the image
logo_path = path / "Spotify-logo.png"

file_path = path / "Country_total - Copy.xlsx"

st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}' alt='Logo' width='100' style='float:left;margin-right:10px;'> **Info**", unsafe_allow_html=True)
# %%
st.write("""
    Thank you for using our dashboard!
     
    This dashboard was cerated by:
    
    Tetiana Prykhodko 48978
    
    Jacek Ziółkowski 40978
    
    Łukasz Gordon 41110
""")

# %%
