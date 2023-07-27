import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 
import time
import os

sys.path.append("../code/Modules")
import arxiv
import scopus
import helper
import eda_graphing

def display_database(col1, key):

    df = pd.read_csv('../data/complete_db.csv')

    max_rows = df.shape[0]

    rows_to_display = st.sidebar.slider("Select the number of rows to display", 1, max_rows, value= (max_rows // 2), key=key)
    
    with col1:
        st.dataframe(df.head(rows_to_display), height=800)


def update_database(col1, col2):

    display_database(col1, "db_slider")

    update_option = st.selectbox(
        'Update from:',
        ['arXiv', 'Scopus', 'ALL']
    )

    query_input = col2.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)").strip()
    queries = [i.strip() for i in query_input.split(",")]

    additional_param_input = col2.text_input("Additional Parameters: Max Paper Retrieval and Reporting Changes (y/n). (Ex. 76, n) Leave blank for Default (25, y)").strip()
    additional_param = [i.strip() for i in additional_param_input.split(",")]


    if col2.button("Submit"):

        status = st.empty()

        valid_additional_params = True

        if len(additional_param) == 1 and additional_param_input == "":
            additional_param = ["0", "25", "y", "y"]
        
        additional_param = [helper.map_yes_no(param, i) for i, param in enumerate(additional_param)]
        valid_additional_params = all(param is not None for param in additional_param)

        query_blank = query_input == ""

        if not query_blank and valid_additional_params:

            status.write(f"Pulling data from {update_option}...")

            if update_option == "arXiv" or update_option == "ALL":
                arxiv.pull_requests(queries, 0, int(additional_param[1]), additional_param[2], 1)
            if update_option == "Scopus" or update_option == "ALL":
                scopus.pull_requests(queries, 0, int(additional_param[1]))
             
            status.write(f"Succesfully obtained {query_input} data from {update_option}!")

            time.sleep(2.5)
            status.empty()

            display_database(col1, "db_slider")

        elif query_blank:

            status.write("Please input a query.")
        
        elif not valid_additional_params:

            status.write("Invalid Additional Parameters. Please try again.")

    st.write("")
    st.write("")

    if col2.button("Remove Duplicates from Database"):

        status = st.empty()

        status.write("Removing duplicate entries from Database...")
        helper.remove_dupes()
        status.write("Succesfully removed duplicate entries from Database!")
                
        time.sleep(2.5)
        status.empty()

        display_database(col1, "db_slider")

    if col2.button("Wipe Database"):

        status = st.empty()

        status.write("Are you sure? This action cannot be undone.")

        yes_or_no = st.columns([1,1])

        if yes_or_no[0].button("Yes"):
            status.write("Wiping Database...")
        if yes_or_no[1].button("No"):
            status.write("")
            
        status.empty()

        display_database(col1, "db_slider")
    

def analyze_database(col1, col2):

    analyze_option = st.selectbox(
        'Select Visualization',
        ['Database Summary', 'Keyword Frequency', 'Publish Frequency', 'Text Frequency']
    )

    grapher = eda_graphing.XForce_Grapher() 

    db_option = "ALL"

    if analyze_option != "Database Summary":

        db_option = st.selectbox(
            'From:',
            ['arXiv', 'Scopus', 'ALL']
        )

    if db_option != "ALL":
        db_option = db_option.lower()

    if analyze_option == "Database Summary":
        with col1:
            st.image(grapher.graph_db_summary(), caption="Database Summary", use_column_width=True)

    elif analyze_option == "Keyword Frequency":

        query_input = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)").replace(" ", "")
        queries = [i.strip() for i in query_input.split(",")]

        if query_input != "":
            with col1:
                st.image(grapher.graph_keyword_freq(queries=queries, sources=[db_option]), caption="Keyword Frequency", use_column_width=True)
                
    elif analyze_option == "Publish Frequency":

        query_input = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)").strip()
        queries = [i.strip() for i in query_input.split(",")]

        if query_input != "":
            with col1: 
                st.image(grapher.graph_pub_freq(queries=queries, sources=[db_option]), caption="Publish Frequency", use_column_width=True)

    elif analyze_option == "Text Frequency":

        query_input = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)").strip()
        queries = [i.strip() for i in query_input.split(",")]

        if query_input != "":
            with col1:
                st.image(grapher.graph_text_freq(queries=queries, sources=[db_option]), caption="Text Frequency", use_column_width=True)


def load_matplotlib_style():
    # Ensure default session state values
    if 'matplotlib_style' not in st.session_state:
        st.session_state['matplotlib_style'] = {}

    # Apply style to Matplotlib
    plt.rcParams.update(st.session_state['matplotlib_style'])


def graph_profiles(col1, col2):

    with col1:
        st.header('Customize Your Graph')

        config_name = st.text_input("Name your configuration", value="custom")

        st.subheader('Font')
        font_type = st.selectbox('Select font type', options=['Arial', 'Times New Roman', 'Calibri'])
        font_size = st.slider('Select font size', min_value=8, max_value=20, value=10)

        st.subheader('Bars')
        bar_color = st.color_picker('Select bar color', '#00F900')
        bar_width = st.slider('Select bar width', min_value=0.5, max_value=5.0, value=2.0, step=0.25)

        st.subheader('Figure Size')
        fig_width = st.slider('Select figure width', min_value=3.5, max_value=10.0, value=7.0, step=0.25)
        fig_height = st.slider('Select figure height', min_value=2.75, max_value=10.0, value=3.0, step=0.25)


        bar_color_rgb = helper.hex_to_rgb(bar_color)

        config = {
            'font.family': font_type,
            'font.size': font_size,
            'lines.color': bar_color_rgb,
            'lines.linewidth': bar_width,
            'figure.figsize': str(fig_width) + ', ' + str(fig_height),
        }

        if st.button('Save Configuration'):
            if config_name:
                with open(f'../configurations/{config_name}.matplotlibrc', 'w') as f:
                    for key, value in config.items():
                        f.write(f'{key}:{value}\n')

                # Save the style to session state
                st.session_state['matplotlib_style'] = config
                st.success('Configuration saved successfully!')
            else:
                st.error('Please add a Configuration name.')

    with col2:

        st.header('Load Configuration')
        config_file = st.file_uploader("Upload Configuration (.rc) File")
        config_default = '../configurations/default.matplotlibrc'  # Default configuration

        # Initialize the session_state
        if "config_file_path" not in st.session_state:
            st.session_state.config_file_path = config_default
            st.session_state.default_config_shown = False

        if config_file is not None:
            config_file_path = os.path.join('../configurations', config_file.name)
            with open(config_file_path, 'wb') as f:
                f.write(config_file.getbuffer())
            st.session_state.config_file_path = config_file_path

        if st.session_state.config_file_path == config_default and not st.session_state.default_config_shown:
            st.session_state.default_config_shown = True
        elif st.session_state.config_file_path != config_default:
            st.session_state.default_config_shown = False

        if st.session_state.default_config_shown:
            st.info(f'Currently using default configuration')
        else:
            st.info(f'Currently using configuration from file: {st.session_state.config_file_path}')

        try:
            plt.style.use(st.session_state.config_file_path)
            st.success('Configuration loaded successfully!')
        except IOError:
            st.error(f'Could not find the style file {st.session_state.config_file_path} in the configurations directory.')

        # Display the configurations
        with open(st.session_state.config_file_path, 'r') as f:
            config_content = f.read()

        file_details = {}
        for line in config_content.split('\n'):
            if line and ':' in line:
                key, value = line.split(':')
                file_details[key] = value
        st.write(file_details)

def feedback_help(col1):

    with col1.form(key="my_feedback"):

        st.write("Please fill out this form")
        name = st.text_input(label="Name:")
        email = st.text_input(label="Email:")
        issue_type = st.selectbox("Select Type:", options=["Help", "Feedback"])
        feedback = st.text_area(label="Describe your suggestion/needed assistance:")
        submit = st.form_submit_button(label="Submit")

        if submit:
            st.write(f"Thank you, {name}! We will get back to you shortly.")
                    # handle feed back here



def main():

    # Title of the web app
    st.title('Team NLP Research & Data Viz')

    # Create a sidebar with a selection box
    with st.sidebar:

        option = st.selectbox(
                'Select from below:', 
                ['Update Database', 'Analyze Database', 'Graph Configurations', 'Feedback / Help'])

        if option == 'Update Database':
            st.write('This option will enable you to update the Database.')

        elif option == 'Analyze Database':
            load_matplotlib_style()
            st.write('This option will enable you to view visualizations of the Database.')

        elif option == 'Graph Configurations':
            load_matplotlib_style()
            st.write('This option will enable you to configure your graphs.')

        elif option == 'Feedback / Help':
            st.write('Suggestions or Bugs.')

    # Create multiple columns in main panel
    col1, col2 = st.columns([3,1]) 


     # Create buttons in the right column based on the sidebar selection
    with col2:

        if option == "Graph Configurations" or option == "Feedback / Help":
            col2.subheader("")
        else:
            col2.subheader("Parameters")

        if option == 'Update Database':
            update_database(col1, col2)

        elif option == 'Analyze Database':
            analyze_database(col1, col2)

        elif option == 'Graph Configurations':
            graph_profiles(col1, col2)

        elif option == 'Feedback / Help':
            feedback_help(col1)


if __name__ == "__main__":
    st.set_page_config(page_title="NDV", layout="wide")
    main()
