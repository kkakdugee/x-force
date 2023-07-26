import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
import time

sys.path.append("../code/Modules/")
import arxiv
import scopus
import helper

def main():

    # Title of the web app
    st.title('Team NLP Research & Data Viz')

    # Create a sidebar with a selection box
    with st.sidebar:

        option = st.selectbox(
                'Select from below:', 
                ['Update Database', 'Analyze Database', 'Feedback / Help'])

        if option == 'Update Database':
            st.write('This option will enable you to update the Database.')

        elif option == 'Analyze Database':
            st.write('This option will enable you to view visualizations of the Database.')

        elif option == 'Feedback / Help':
            st.write('Suggestions or Bugs.')

    # Create multiple columns in main panel
    col1, col2 = st.columns([3,1]) 

    # Create buttons in the right column based on the sidebar selection
    with col2:

        if option == "Feedback / Help":
            col2.subheader("")
        else:
            col2.subheader("Parameters")

        if option == 'Update Database':

            df = pd.read_csv('../data/complete_db.csv')

            max_rows = df.shape[0]

            rows_to_display = st.sidebar.slider("Select the number of rows to display", 1, max_rows, value=10)

            with col1:
                st.dataframe(df.head(rows_to_display))

            update_option = st.selectbox(
                'Update from:',
                ['arXiv', 'Scopus', 'ALL']
            )

            query = col2.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)")
            stripped = [i.strip() for i in query.split(",")]

            if col2.button("Submit"):
                 if stripped != "":

                    status = st.empty()

                    status.write(f"Pulling data from {update_option}...")

                    if update_option == "arXiv" or update_option == "ALL":
                        arxiv.pull_requests(stripped, 0, 25, 1, 1)
                    if update_option == "Scopus" or update_option == "ALL":
                        scopus.pull_requests(stripped, 0, 25)
                    
                    status.write(f"Succesfully obtained {query} data from {update_option}!")

                    time.sleep(2.5)
                    status.empty()

            st.write("")
            st.write("")

            if col2.button("Remove Duplicates from Database"):

                status = st.empty()

                status.write("Removing duplicate entries from Database...")
                helper.remove_dupes()
                status.write("Succesfully removed duplicate entries from Database!")
                
                time.sleep(2.5)
                status.empty()

            if col2.button("Wipe Database"):

                status = st.empty()

                status.write("Are you sure? This action cannot be undone.")

                yes_or_no = st.columns([1,1])

                if yes_or_no[0].button("Yes"):
                    status.write("Wiping Database...")
                if yes_or_no[1].button("No"):
                    status.write("")
            
                status.empty()
            

        elif option == 'Analyze Database':

            analyze_option = st.selectbox(
                'Select Visualization',
                ['Database Summary', 'Keyword Frequency', 'Publish Frequency', 'Text Frequency']
            )

            if analyze_option != "Database Summary":

                db_option = st.selectbox(
                    'From:',
                    ['arXiv', 'Scopus', 'ALL']
                )

            if analyze_option == "Database Summary":
                with col1:
                    st.image("../images/summary.png", caption="Database Summary", use_column_width=True)

            elif analyze_option == "Keyword Frequency":

                query = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)")

                if query == "AI,infrared,photon":
                    with col1:
                        st.image("../images/keyword_freq/keyword_freq_ALL_AI_infrared_photon.png", caption="Keyword Frequency of AI, infrared, photon in all databases", use_column_width=True)
                elif query == "ALL":
                    with col1:
                        st.image("../images/keyword_freq/keyword_freq_ALL_ALL.png", caption="Keyword Frequency of all queries in all databases", use_column_width=True)
                
            elif analyze_option == "Publish Frequency":

                query = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)")

                if query == "ALL":
                    with col1:
                        st.image("../images/pub_freq/pub_freq_arxiv_ALL.png", caption="Publish Frequency of all queries in arXiv", use_column_width=True)
                elif query == "radiation,plasmonics,metamaterials":
                    with col1:
                        st.image("../images/pub_freq/pub_freq_arxiv_radiation_plasmonics_metamaterials.png", caption="Publish Frequency of radiation, plasmonics, metamaterials in arXiv", use_column_width=True)

            elif analyze_option == "Text Frequency":

                query = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)")

                if query == "ALL":
                    with col1:
                        st.image("../images/text_freq/text_freq_ALL_ALL.png", caption="Text Frequency of all queries in all databases", use_column_width=True)
                elif query == "plasmonics,heavy ion":
                    with col1:
                        st.image("../images/text_freq/text_freq_ALL_plasmonics_heavy ion.png", caption="Text Frequency of plasmonics, heavy ion in all databases", use_column_width=True)

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
