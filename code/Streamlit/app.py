#----------------------------------------------------
# TODO
#----------------------------------------------------
# ?

#----------------------------------------------------
# Imports Checking
#----------------------------------------------------
import sys
sys.path.append("../code/Modules")
import arxiv
import scopus
import helper
import eda_graphing

#----------------------------------------------------
# Graphing Class
#----------------------------------------------------
def display_database(col1, key):

    df = helper.pd.read_csv('../data/complete_db.csv')

    max_rows = df.shape[0]

    rows_to_display = helper.st.sidebar.slider("Select the number of rows to display", 1, max_rows, value= (max_rows // 2), key=key)
    
    with col1:
        helper.st.dataframe(df.head(rows_to_display), height=800)


def update_database(col1, col2):

    display_database(col1, "db_slider")

    update_option = helper.st.selectbox(
        'Update from:',
        ['arXiv', 'Scopus', 'ALL']
    )

    query_input = col2.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)").strip()
    queries = [i.strip() for i in query_input.split(",")]

    additional_param_input = col2.text_input("Additional Parameters: Max Paper Retrieval and Reporting Changes (y/n). (Ex. 76, n) Leave blank for Default (25, y)").strip()
    additional_param = [i.strip() for i in additional_param_input.split(",")]


    if col2.button("Submit"):

        status = helper.st.empty()

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

            helper.time.sleep(2.5)
            status.empty()

            display_database(col1, "db_slider")

        elif query_blank:

            status.write("Please input a query.")
        
        elif not valid_additional_params:

            status.write("Invalid Additional Parameters. Please try again.")

    helper.st.write("")
    helper.st.write("")

    if col2.button("Remove Duplicates from Database"):

        status = helper.st.empty()

        status.write("Removing duplicate entries from Database...")
        helper.remove_dupes()
        status.write("Succesfully removed duplicate entries from Database!")
                
        helper.time.sleep(2.5)
        status.empty()

        display_database(col1, "db_slider")

    if col2.button("Wipe Database"):

        status = helper.st.empty()

        status.write("Are you sure? This action cannot be undone.")

        yes_or_no = helper.st.columns([1,1])

        if yes_or_no[0].button("Yes"):
            status.write("Wiping Database...")
        if yes_or_no[1].button("No"):
            status.write("")
            
        status.empty()

        display_database(col1, "db_slider")
    

def analyze_database(col1, col2):

    analyze_option = helper.st.selectbox(
        'Select Visualization',
        ['Database Summary', 'Keyword Frequency', 'Publish Frequency', 'Text Frequency']
    )

    grapher = eda_graphing.XForce_Grapher() 

    db_option = "ALL"

    if analyze_option != "Database Summary":

        db_option = helper.st.selectbox(
            'From:',
            ['arXiv', 'Scopus', 'ALL']
        )

    if db_option != "ALL":
        db_option = db_option.lower()

    if analyze_option == "Database Summary":
        with col1:
            helper.st.image(grapher.graph_db_summary(), caption="Database Summary", use_column_width=True)

    elif analyze_option == "Keyword Frequency":

        query_input = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)").replace(" ", "")
        queries = [i.strip() for i in query_input.split(",")]

        if query_input != "":
            with col1:
                helper.st.image(grapher.graph_keyword_freq(queries=queries, sources=[db_option]), caption="Keyword Frequency", use_column_width=True)
                
    elif analyze_option == "Publish Frequency":

        query_input = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)").strip()
        queries = [i.strip() for i in query_input.split(",")]

        if query_input != "":
            with col1: 
                helper.st.image(grapher.graph_pub_freq(queries=queries, sources=[db_option]), caption="Publish Frequency", use_column_width=True)

    elif analyze_option == "Text Frequency":

        query_input = col2.text_input("Queries (Ex. ALL) (Ex. radiation,metamaterials,etc)").strip()
        queries = [i.strip() for i in query_input.split(",")]

        if query_input != "":
            with col1:
                helper.st.image(grapher.graph_text_freq(queries=queries, sources=[db_option]), caption="Text Frequency", use_column_width=True)


def load_matplotlib_style():
    # Ensure default session state values
    if 'matplotlib_style' not in helper.st.session_state:
        helper.st.session_state['matplotlib_style'] = {}

    # Apply style to Matplotlib
    helper.plt.rcParams.update(helper.st.session_state['matplotlib_style'])


def graph_profiles(col1, col2):

    with col1:
        helper.st.header('Customize Your Graph')

        config_name = helper.st.text_input("Name your configuration", value="custom")

        helper.st.subheader('Font')
        font_type = helper.st.selectbox('Select font type', options=['Arial', 'Times New Roman', 'Calibri'])
        font_size = helper.st.slider('Select font size', min_value=8, max_value=20, value=10)

        helper.st.subheader('Figure Size')
        fig_width = helper.st.slider('Select figure width', min_value=3.5, max_value=10.0, value=7.0, step=0.25)
        fig_height = helper.st.slider('Select figure height', min_value=2.75, max_value=10.0, value=3.0, step=0.25)


        config = {
            'font.family': font_type,
            'font.size': font_size,
            'figure.figsize': str(fig_width) + ', ' + str(fig_height),
        }

        if helper.st.button('Save Configuration'):
            if config_name:
                with open(f'../configurations/{config_name}.matplotlibrc', 'w') as f:
                    for key, value in config.items():
                        f.write(f'{key}:{value}\n')

                # Save the style to session state
                helper.st.session_state['matplotlib_style'] = config
                helper.st.success('Configuration saved successfully!')
            else:
                helper.st.error('Please add a Configuration name.')

    with col2:

        helper.st.header('Load Configuration')
        config_file = helper.st.file_uploader("Upload Configuration (.rc) File")
        config_default = '../configurations/default.matplotlibrc'  # Default configuration

        # Initialize the session_state
        if "config_file_path" not in helper.st.session_state:
            helper.st.session_state.config_file_path = config_default
            helper.st.session_state.default_config_shown = False

        if config_file is not None:
            config_file_path = helper.os.path.join('../configurations', config_file.name)
            with open(config_file_path, 'wb') as f:
                f.write(config_file.getbuffer())
            helper.st.session_state.config_file_path = config_file_path

        if helper.st.session_state.config_file_path == config_default and not helper.st.session_state.default_config_shown:
            helper.st.session_state.default_config_shown = True
        elif helper.st.session_state.config_file_path != config_default:
            helper.st.session_state.default_config_shown = False

        if helper.st.session_state.default_config_shown:
            helper.st.info(f'Currently using default configuration')
        else:
            helper.st.info(f'Currently using configuration from file: {helper.st.session_state.config_file_path}')

        try:
            helper.plt.style.use(helper.st.session_state.config_file_path)
            helper.st.success('Configuration loaded successfully!')
        except IOError:
            helper.st.error(f'Could not find the style file {helper.st.session_state.config_file_path} in the configurations directory.')

        # Display the configurations
        with open(helper.st.session_state.config_file_path, 'r') as f:
            config_content = f.read()

        file_details = {}
        for line in config_content.split('\n'):
            if line and ':' in line:
                key, value = line.split(':')
                file_details[key] = value
        helper.st.write(file_details)

def feedback_help(col1):

    with col1.form(key="my_feedback"):

        helper.st.write("Please fill out this form")
        name = helper.st.text_input(label="Name:")
        email = helper.st.text_input(label="Email:")
        issue_type = helper.st.selectbox("Select Type:", options=["Help", "Feedback"])
        feedback = helper.st.text_area(label="Describe your suggestion/needed assistance:")
        submit = helper.st.form_submit_button(label="Submit")

        if submit:
            helper.st.write(f"Thank you, {name}! We will get back to you shortly.")

            token = 'github token'

            url = 'https://api.github.com/repos/kkakdugee/x-force/issues'  
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github+json',  
            }
            data = {
                'title': f'Feedback from {name}',
                'body': feedback,
            }

            token = 'github token'

            url = 'https://api.github.com/repos/kkakdugee/x-force/issues'  
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github+json',  
            }
            data = {
                'title': f'Feedback from {name}',
                'body': feedback,
            }

            response = helper.requests.post(url, headers=headers, json=data)


def main():

    # Title of the web app
    helper.st.title('X-Force NLP Visualizer')

    # Create a sidebar with a selection box
    with helper.st.sidebar:

        option = helper.st.selectbox(
                'Select from below:', 
                ['Update Database', 'Analyze Database', 'Graph Configurations', 'Feedback / Help'])

        if option == 'Update Database':
            helper.st.write('This option will enable you to update the Database.')

        elif option == 'Analyze Database':
            load_matplotlib_style()
            helper.st.write('This option will enable you to view visualizations of the Database.')

        elif option == 'Graph Configurations':
            load_matplotlib_style()
            helper.st.write('This option will enable you to configure your graphs.')

        elif option == 'Feedback / Help':
            helper.st.write('Suggestions or Bugs.')

    # Create multiple columns in main panel
    col1, col2 = helper.st.columns([3,1]) 


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
    helper.st.set_page_config(page_title="NDV", layout="wide")
    main()
