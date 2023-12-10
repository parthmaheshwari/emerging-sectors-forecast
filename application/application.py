import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

retraining_flag = True

# Title and subtitle
st.write("""
# Analysing Funding Flows in Private Markets Using Academic Signals
#### This application is an in-depth exploration of the work we have done as a team.
"""
)
