# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():

    # Title of the web app
    st.title('NLP Data Tool')

    # Create a sidebar with a selection box
    with st.sidebar:
        option = st.selectbox(
                'Select from below:', 
                ['Update Database', 
                 'Analyze Database', 
                 'Feedback / Help'])

    # Create multiple columns in main panel
    col1, col2, col3 = st.columns([1,2,1]) # adjust as per your needs

    # Display details in the left column based on the sidebar selection
    with col1:
        if option == 'Update Database':
            # Add your function to update database
            st.write('This option will enable you to update the Database.')

        elif option == 'Analyze Database':
            # Add your function to do visualizations
            st.write('This option will enable you to view visualizations of the Database.')

        elif option == 'Feedback / Help':
            # Add your function to clean duplicates
            st.write('Suggestions or Bugs.')

    # Create a random DataFrame
    df = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )

    # Create a matplotlib plot
    fig, ax = plt.subplots(figsize=(6, 4))  # adjust the size as needed
    ax.scatter(df['a'], df['b'], c=df['c'], cmap='viridis')

    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_title('Scatter Plot of random values')

    # Display the DataFrame and the plot in the middle column
    with col2:
        st.pyplot(fig)

    # Create buttons in the right column based on the sidebar selection
    with col3:
        col3.subheader("Parameters")
        if option == 'Update Database':
            update_options = st.selectbox(
                'Update from:',
                ['arXiv',
                'Scopus',
                'Both']
            )
            query = col3.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)")
            if col3.button("Remove Duplicates from Database"):
                st.write("TODO")
            if col3.button("Wipe Database"):
                st.write("TODO")
            

        elif option == 'Analyze Database':
            analyze_options = st.selectbox(
                'Select Visualization',
                ['Database Summary',
                'Search Frequency',
                'Keyword Frequency']
            )

        elif option == 'Feedback / Help':
            if st.button('Submit Feedback'):
                st.write('Feedback submitted.')

if __name__ == "__main__":
    st.set_page_config(page_title="NDV", layout="wide")
    main()
