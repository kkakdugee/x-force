#----------------------------------------------------
# Imports Checking
#----------------------------------------------------
import sys
sys.path.append("../../code/Modules")
import arxiv
import scopus
import helper
import eda_graphing
import db_functions

#----------------------------------------------------
# Graphing Class
#----------------------------------------------------

def display_database(col1):

    if 'db_placeholder' not in session:
        session.db_placeholder = col1.empty()

    session.db_placeholder.dataframe(helper.pd.read_csv(session.db_path), height=800)



def select_database(col1):

    uploaded_database = helper.st.file_uploader("Upload a Database:", type="csv")

    if uploaded_database is not None:

        session.db_path = helper.RELATIVE_TO_APP_DATA + uploaded_database.name

        try:

            session.db_manager.select_db(session.db_path)
            session.db_selected = True
            session.db_working = session.db_manager.get_current_working_db()
            helper.st.success(f'Database loaded successfully!')

        except IOError:

            helper.st.error(f'Could not find the database file {session.db_path}.')

    else:

        helper.st.info("Please upload a Database CSV.")


    helper.st.write("")
    helper.st.write("")

    # Creating new Database
    helper.st.write("Create a new Database")
    db_name = helper.st.text_input("Name your Database")

    if helper.st.button("Create new Database"):

        if db_name:

            try:

                session.db_path = session.db_manager.new_db(db_name)
                session.db_manager.select_db(session.db_path)
                session.db_selected = True
                session.db_working = session.db_manager.get_current_working_db()
                helper.st.success(f"Successfully created and loaded {db_name}!")

            except IOError:
                helper.st.error(f"{db_name} is currently reserved. You cannot create, overwrite, or delete a DB with this name.")

    if session.db_path is not None:
        display_database(col1)


def update_database(col1):

    if session.db_selected:

        display_database(col1)

        update_option = helper.st.selectbox(
            'Update from:',
            ['arXiv', 'Scopus', 'ALL']
        )

        query_input = helper.st.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)").strip()
        queries = [i.strip() for i in query_input.split(",")]

        additional_param_input = helper.st.text_input("Additional Parameters: Max Paper Retrieval and Reporting Changes (y/n). (Ex. 76, n) Leave blank for Default (25, y)").strip()
        additional_param = [i.strip() for i in additional_param_input.split(",")]


        if helper.st.button("Submit"):

            status = helper.st.empty()

            valid_additional_params = True

            if len(additional_param) == 1 and additional_param_input == "":
                additional_param = ["25", "y"]

            if len(additional_param) != 2:
                valid_additional_params = False

            max_paper_retrieval = helper.map_yes_no(additional_param[0].strip(), 0)
            reporting_changes = helper.map_yes_no(additional_param[1].strip(), 1)

            if max_paper_retrieval is None or reporting_changes is None:

                valid_additional_params = False


            query_blank = query_input == ""

            if not query_blank and valid_additional_params:

                status.write(f"Pulling data from {update_option}...")


                if update_option == "arXiv" or update_option == "ALL":
                    arxiv.pull_requests(session.db_path, queries, 0, int(max_paper_retrieval), reporting_changes, 1)
                if update_option == "Scopus" or update_option == "ALL":
                    scopus.pull_requests(session.db_path, queries, 0, int(max_paper_retrieval))

                status.write(f"Succesfully obtained {query_input} data from {update_option}!")

                helper.time.sleep(2.5)
                status.empty()

                display_database(col1)

            elif query_blank:

                status.write("Please input a query.")

            elif not valid_additional_params:

                status.write("Invalid Additional Parameters. Please try again.")

        helper.st.write("")
        helper.st.write("")

        if helper.st.button("Remove Duplicates from Database"):

            status = helper.st.empty()

            status.write("Removing duplicate entries from Database...")
            session.db_manager.dedupe_curr_db()
            status.write("Succesfully removed duplicate entries from Database!")

            helper.time.sleep(2.5)
            status.empty()

            display_database(col1)

        if helper.st.button("Wipe Database"):

            status = helper.st.empty()

            helper.st.warning("Are you sure? This action cannot be undone.")

            yes_or_no = helper.st.columns([1,1])

            if yes_or_no[0].button("Yes"):
                session.db_manager.reset_curr_db()
            if yes_or_no[1].button("No"):
                status.write("")

            status.empty()

            display_database(col1)
    else:

        helper.st.warning("Please load a database in the \"Select\" tab before proceeding")

def filter_database(col1):
    
    if session.db_selected:
        
        # Row Filtering
        with helper.st.expander("Row Filters"):
            start_row = helper.st.number_input("Start Row", min_value=0, max_value=len(session.db_working))
            end_row = helper.st.number_input("End Row", min_value=start_row, max_value=len(session.db_working), value=len(session.db_working))
            if helper.st.button("Filter Rows"):
                session.db_manager.filter_curr_rows(start_row, end_row)
                session.db_working = session.db_manager.get_current_working_db()
        
        # Source Filtering
        with helper.st.expander("Source Filters"):
            sources = session.db_working["source"].unique().tolist()
            sources.append("ALL")
            selected_sources = helper.st.multiselect("Select Sources", sources, default=["ALL"])
            if helper.st.button("Filter Sources"):
                session.db_manager.filter_curr_source(selected_sources)
                session.db_working = session.db_manager.get_current_working_db()

        # Query Filtering
        with helper.st.expander("Query Filters"):
            queries = session.db_working["query"].unique().tolist()
            queries.append("ALL")
            selected_queries = helper.st.multiselect("Select Queries", queries, default=["ALL"])
            if helper.st.button("Filter Queries"):
                session.db_manager.filter_curr_query(selected_queries)
                session.db_working = session.db_manager.get_current_working_db()
                
        # Title Filtering
        with helper.st.expander("Title Filters"):
            title_values = helper.st.text_input("Title Values (comma-separated)")
            title_and_or_condition = helper.st.selectbox("Title Condition", ["AND", "OR"], index=0)
            if helper.st.button("Filter Titles"):
                session.db_manager.filter_curr_title(title_values.split(','), 0 if title_and_or_condition == "AND" else 1)
        
        # Abstract Filtering
        with helper.st.expander("Abstract Filters"):
            abstract_values = helper.st.text_input("Abstract Values (comma-separated)")
            abstract_and_or_condition = helper.st.selectbox("Abstract Condition", ["AND", "OR"], index=0)
            if helper.st.button("Filter Abstracts"):
                session.db_manager.filter_curr_abstract(abstract_values.split(','), 0 if abstract_and_or_condition == "AND" else 1)
                session.db_working = session.db_manager.get_current_working_db()
                
        # Author Filtering
        with helper.st.expander("Author Filters"):
            author_values = helper.st.text_input("Author Values (comma-separated)")
            author_and_or_condition = helper.st.selectbox("Author Condition", ["AND", "OR"], index=0)
            if helper.st.button("Filter Authors"):
                session.db_manager.filter_curr_author(author_values.split(','), 0 if author_and_or_condition == "AND" else 1)
                session.db_working = session.db_manager.get_current_working_db()
        
        # Date Filtering
        with helper.st.expander("Date Filters"):
            start_date = helper.st.date_input("Start Date")
            end_date = helper.st.date_input("End Date")
            if helper.st.button("Filter Dates"):
                session.db_manager.filter_curr_date(start_date, end_date)
                session.db_working = session.db_manager.get_current_working_db()
                
        # Sorting
        with helper.st.expander("Sorting Options"):
            sort_on = helper.st.selectbox("Sort On", session.db_working.columns.tolist())
            is_ascending = helper.st.checkbox("Ascending Order")
            if helper.st.button("Sort"):
                session.db_manager.sort_curr_db(sort_on, is_ascending)
                session.db_working = session.db_manager.get_current_working_db()
                
        # Reset Filters and Confirm Changes
        if helper.st.button("Clear Filters"):
            session.db_manager.clear_curr_db_filters()
            session.db_working = session.db_manager.get_current_working_db()
            
        if helper.st.button("Confirm"):
            session.db_manager.confirm_db()
            session.db_working = session.db_manager.get_current_working_db()
        
        display_database(col1)

    else:
        helper.st.warning("Please load a database in the \"Select\" tab before proceeding")

def database(col1, col2):

    with col2:

        tab1, tab2, tab3 = helper.st.tabs(["Select", "Update", "Filter"])

        with tab1:
            select_database(col1)

        with tab2:
            update_database(col1)

        with tab3:
            filter_database(col1)


def display_image(col, image, caption):

    with col:
        helper.st.image(image, caption=caption, use_column_width=True)


def analyze_database(col1, col2):

    with col2:

        if session.db_selected:

            analyze_option = helper.st.selectbox(
                'Select Visualization',
                ['Database Summary', 'Keyword Frequency', 'Publish Frequency', 'Text Frequency', 'Network Co-Occurence', 'Bubble Map']
            )

            if helper.st.button("Submit"):

                grapher = eda_graphing.XForce_Grapher()

                if analyze_option == "Database Summary":
                    display_image(col1, grapher.graph_db_summary(), "Database Summary")
                elif analyze_option == "Keyword Frequency":
                    display_image(col1, grapher.graph_keyword_freq(queries=["ALL"], sources=["ALL"]), "Keyword Frequency")
                elif analyze_option == "Publish Frequency":
                    display_image(col1, grapher.graph_pub_freq(queries=["ALL"], sources=["ALL"]), "Publish Frequency")
                elif analyze_option == "Text Frequency":
                    display_image(col1, grapher.graph_text_freq(queries=["ALL"], sources=["ALL"]), "Text Frequency")
                elif analyze_option == "Network Co-Occurrence":
                    display_image(col1, grapher.graph_network_cooccurence(), "Network Co-Occurrence")
                elif analyze_option == "Bubble Map":
                    display_image(col1, grapher.graph_bubble_map(), "Bubble Map")
        else:

            helper.st.warning("Please load a database in the \"Select\" tab before proceeding")



def graph_profiles(col1, col2):

    with col1:

        helper.st.header('Customize Your Graph')

        config_name = helper.st.text_input("Name your configuration")

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
                with open(f'../../configurations/{config_name}.matplotlibrc', 'w') as f:
                    for key, value in config.items():
                        f.write(f'{key}:{value}\n')

                helper.st.success('Configuration saved successfully!')
            else:
                helper.st.error('Please add a Configuration name.')

    with col2:

        helper.st.header('Load Configuration')
        config_file = helper.st.file_uploader("Upload Configuration (.rc) File")
        config_default = '../../configurations/default.matplotlibrc'  # Default configuration

        # Check if the session state has a custom configuration path
        if session.config_path is None:
            session.config_path = config_default
            using_default = True
        else:
            using_default = False

        if config_file is not None:
            config_file_path = helper.os.path.join('../../configurations', config_file.name)
            session.config_path = config_file_path
            using_default = False

        if using_default:
            helper.st.info(f'Currently using default configuration')
        else:
            helper.st.info(f'Currently using configuration from file: {helper.os.path.basename(session.config_path)}')

        try:
            helper.plt.style.use(session.config_path)
            helper.st.success('Configuration loaded successfully!')
        except IOError:
            helper.st.error(f'Could not find the style file {session.config_path} in the configurations directory.')

        # Display the configurations
        with open(session.config_path, 'r') as f:
            config_content = f.read()
        file_details = {}
        for line in config_content.split('\n'):
            if line and ':' in line:
                key, value = line.split(':')
                file_details[key] = value.strip()  # Removing leading/trailing whitespace
        helper.st.write(file_details)


def feedback_help(col1):

    with col1.form(key="my_feedback"):

        helper.st.write("Please fill out this form")
        name = helper.st.text_input(label="Name:")
        email = helper.st.text_input(label="Email:")
        issue_type = helper.st.selectbox("Select Type:", options=["Help", "Feedback"])
        feedback = helper.st.text_area(label="Describe your suggestion/needed assistance:")
        github_token = helper.st.text_input(label="Please enter your GitHub Token:")
        submit = helper.st.form_submit_button(label="Submit")

        if submit:
            helper.st.write(f"Thank you, {name}! We will get back to you shortly.")

            url = 'https://api.github.com/repos/kkakdugee/x-force/issues'  
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github+json',  
            }
            data = {
                'title': f'{issue_type} from {name}',
                'body': feedback,
            }

            response = helper.requests.post(url, headers=headers, json=data)


def main():

    # Title of the web app
    helper.st.title('NLP Research Visualizer')

    # Create a sidebar with a selection box
    with helper.st.sidebar:

        option = helper.st.selectbox(
                'Select from below:', 
                ['Database', 'Analyze Database', 'Graph Configurations', 'Feedback / Help'])

        if option == 'Configure & Update Database':
            helper.st.write('This option will enable you to make configurations and update your Database.')

        elif option == 'Analyze Database':
            helper.st.write('This option will enable you to view visualizations of the selected Database.')

        elif option == 'Graph Configurations':
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


    if option == 'Database':
        database(col1, col2)

    elif option == 'Analyze Database':
        analyze_database(col1, col2)

    elif option == 'Graph Configurations':
        graph_profiles(col1, col2)

    elif option == 'Feedback / Help':
        feedback_help(col1)


if __name__ == "__main__":

    helper.st.set_page_config(page_title="NLP Research Viz", layout="wide")

    session = helper.st.session_state

    if "db_manager" not in session:
        session.db_manager = db_functions.XForce_Database()
    if "db_path" not in session:
        session.db_path = None
    if "db_selected" not in session:
        session.db_selected = False

    if "config_path" not in session:
        session.config_path = None

    main()
