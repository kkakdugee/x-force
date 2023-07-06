# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
sys.path.insert(0, "../code/")
import main as mn

def main():

    # Title of the web app
    st.title('NLP Data Tool')

    # Create a sidebar with a selection box
    with st.sidebar:
        option = st.selectbox(
                'Select from below:', 
                ['Update Database', 'Analyze Database', 'Feedback / Help'])
        if option == 'Update Database':
            # Add your function to update database
            st.write('This option will enable you to update the Database.')

        elif option == 'Analyze Database':
            # Add your function to do visualizations
            st.write('This option will enable you to view visualizations of the Database.')

        elif option == 'Feedback / Help':
            # Add your function to clean duplicates
            st.write('Suggestions or Bugs.')

    # Create multiple columns in main panel
    col1, col2 = st.columns([2,1]) 

    # Create buttons in the right column based on the sidebar selection
    with col2:

        if option == "Feedback / Help":
            col2.subheader("")
        else:
            col2.subheader("Parameters")

        if option == 'Update Database':

            df = pd.DataFrame(
                np.random.randn(1000, 11),
                columns=['source', 'query', 'query_time', 'title', 'journal', 'authors', 'doi', 'published', 'abstract', 'url', 'tags']
            )

            with col1:
                st.write(df)

            update_option = st.selectbox(
                'Update from:',
                ['arXiv', 'Scopus', 'Both']
            )

            query = col2.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)")
            stripped = query.replace(" ", "")

            if stripped != "":
                st.write("TODO")
            if col2.button("Remove Duplicates from Database"):
                mn.option_clean_dupes("")
            if col2.button("Wipe Database"):
                st.write("TODO")
            

        elif option == 'Analyze Database':
            analyze_option = st.selectbox(
                'Select Visualization',
                ['Database Summary', 'Search Frequency', 'Keyword Frequency']
            )

            if analyze_option == "Database Summary":
                with col1:
                    st.image("../images/summary.png", caption="Database Summary", use_column_width=True)
            
            elif analyze_option == "Search Frequency":

                query = col2.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)")

                stripped = query.replace(" ", "")

                if stripped == "radiation":
                    with col1:
                        st.image("../images/radiation_arxiv.png", caption="radiation_arxiv", use_column_width=True)
                elif stripped == "plasmonics":
                    with col1:
                        st.image("../images/plasmonics_arxiv.png", caption="plasmonics_arxiv", use_column_width=True)
                elif stripped == "metamaterials":
                    with col1:
                        st.image("../images/metamaterials_arxiv.png", caption="metalmaterials_arxiv", use_column_width=True)

        elif option == 'Feedback / Help':

            with col1.form(key="my_form"):
                st.write("Fill out this form")
                name = st.text_input(label="Name")
                email = st.text_input(label="Email")
                feedback = st.text_area(label="Any suggestions or help?")
                submit = st.form_submit_button(label="Submit Feedback")

                if submit:
                    st.write(f"Thank you for your feedback, {name}!")
                    # handle feed back here

if __name__ == "__main__":
    st.set_page_config(page_title="NDV", layout="wide")
    main()
