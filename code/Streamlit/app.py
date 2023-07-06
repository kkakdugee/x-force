# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():

    # Title of the web app
    st.title('Welcome!')

    # Create a sidebar with a selection box
with st.sidebar:
    option = st.selectbox(
            'Select from below::', 
            ['Update Database by Search', 
             'Visualization by Term', 
             'Remove Duplicates', 
             'Wipe Database'])
    st.button("test")

    # Display the selected option
    # st.write(f'You selected: {option}')
    
    # Add functions for each option
    if option == 'Update Database by Search':
        # Add your function to update database
        st.write('This will update the database for a search term.')
    
    elif option == 'Visualization by Term':
        # Add your function to do visualizations
        st.write('This will show visualizations.')
    
    elif option == 'Remove Duplicates':
        # Add your function to clean duplicates
        st.write('This will clean duplicates from the database.')
    
    elif option == 'Wipe Database':
        # Add your function to wipe the database
        st.write('This will wipe the database.')
    










if __name__ == "__main__":
    #st.set_page_config(page_title="NLP Data Visualization", layout="wide")
    main()
