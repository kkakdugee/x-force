"""
This module contains functions related to database operations.
"""

import helper
import arxiv
import scopus
import db_functions


def display_database(col1, session):

    """
    Displying the CSV database on the application.
    
    Parameters:
    - col1: Streamlit column object for displaying content.
    - session: Streamlit's session state.
    
    Returns:
    None
    """
    
     # Check if a placeholder for the database exists in the session
    if 'db_placeholder' not in session:
        session.db_placeholder = col1.empty()

    # Display the database
    session.db_placeholder.dataframe(helper.pd.read_csv(session.db_path), height=800)

def select_database(col1, session):

    """
    Allows the user to select a database for use in the application.
    
    Parameters:
    - col1: Streamlit column object for displaying content.
    - session: Streamlit's session state.
    
    Returns:
    None
    """

    # Upload a new database
    uploaded_database = helper.st.file_uploader("Upload a Database:", type="csv")

    # If a database is uploaded, load it
    if uploaded_database is not None:
        _load_uploaded_database(uploaded_database, session)
    else:
        helper.st.info("Please upload a Database CSV.")


    helper.st.write("")
    helper.st.write("")

    # Interface for creating a new database
    _create_new_database(session)

    # Display the selected database
    if session.db_path is not None:
        display_database(col1, session)


def update_database(col1, session):
    """
    Allows the user to update the database based on various sources and criteria.
    
    Parameters:
    - col1: Streamlit column object for displaying content.
    - session: Streamlit's session state.
    """

    # Check if a database is selected
    if session.db_selected:

        # Display the current database
        display_database(col1, session)

        # Dropdown for selecting the update source
        update_option = helper.st.selectbox(
            'Update from:',
            ['arXiv', 'Scopus', 'ALL']
        )

        # Input for queries
        query_input = helper.st.text_input("Queries (Ex. radiation) (Ex. radiation,metamaterials,etc)").strip()
        queries = [i.strip() for i in query_input.split(",")]

        # Input for additional parameters
        additional_param_input = helper.st.text_input("Additional Parameters: Max Paper Retrieval and Reporting Changes (y/n). (Ex. 76, n) Leave blank for Default (25, y)").strip()
        additional_param = [i.strip() for i in additional_param_input.split(",")]

        # Validate and process the input parameters
        if helper.st.button("Submit"):

            status = helper.st.empty()

            valid_additional_params = _validate_additional_params(additional_param, additional_param_input)
            query_blank = query_input == ""

            # If parameters are valid, pull data from the selected source
            if not query_blank and valid_additional_params:

                _pull_data(update_option, session, queries, additional_param, status)

            elif query_blank:

                status.write("Please input a query.")

            elif not valid_additional_params:

                status.write("Invalid Additional Parameters. Please try again.")

        helper.st.write("")
        helper.st.write("")

        # Options to remove duplicates and wipe the database
        if helper.st.button("Remove Duplicates from Database"):
            _remove_duplicates_from_database(col1, session)
        if helper.st.button("Wipe Database"):
            _wipe_database(col1, session)
    else:
        helper.st.warning("Please load a database in the \"Select\" tab before proceeding")

def filter_database(col1, session):
    """
    Provides filtering options for the database.
    
    Parameters:
    - col1: Streamlit column object for displaying content.
    - session: Streamlit's session state.
    """

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
        
        display_database(col1, session)

    else:
        helper.st.warning("Please load a database in the \"Select\" tab before proceeding")

def database(col1, col2, session):
    """
    Provides database operations through tabs: Select, Update, and Filter.
    
    Parameters:
    - col1: Streamlit column object for displaying content.
    - col2: Streamlit column object for displaying content.
    - session: Streamlit's session state.

    Returns:
    None
    """

    with col2:

        tab1, tab2, tab3 = helper.st.tabs(["Select", "Update", "Filter"])

        with tab1:
            select_database(col1, session)

        with tab2:
            update_database(col1, session)

        with tab3:
            filter_database(col1, session)


#----------------------------------------------------
# Helper Functions
#----------------------------------------------------

def _load_uploaded_database(uploaded_database, session):

    """
    Loads the uploaded database into the session.

    Parameters:
    - uploaded_database: The uploaded database file.

    Returns:
    None
    """

     # Define the path for the uploaded database
    session.db_path = helper.RELATIVE_TO_APP_DATA + uploaded_database.name
    
    # Try to select and load the database
    try:
        session.db_manager.select_db(session.db_path)
        session.db_selected = True
        session.db_working = session.db_manager.get_current_working_db()
        helper.st.success(f'Database loaded successfully!')
    except IOError:
        helper.st.error(f'Could not find the database file {session.db_path}.')


def _create_new_database(session):

    """
    Provides an interface for creating a new database.
    
    Parameters:
    - session: Streamlit's session state.

    Returns:
    None
    """

    helper.st.write("Create a new Database")

    # Input for naming the new database
    db_name = helper.st.text_input("Name your Database")

    # Button to create the new database
    if helper.st.button("Create new Database"):
        if db_name: # If the name isnt blank/null
            try:
                session.db_path = session.db_manager.new_db(db_name)
                session.db_manager.select_db(session.db_path)
                session.db_selected = True
                session.db_working = session.db_manager.get_current_working_db()
                helper.st.success(f"Successfully created and loaded {db_name}!")
            except IOError:
                helper.st.error(f"{db_name} is currently reserved. You cannot create, overwrite, or delete a DB with this name.")



def _validate_additional_params(additional_param, additional_param_input):
    """
    Validates the additional parameters provided by the user.
    
    Parameters:
    - additional_param: List of additional parameters.
    - additional_param_input: Raw input string of additional parameters.
    
    Returns:
    Boolean indicating if the parameters are valid.
    """

    if len(additional_param) == 1 and additional_param_input == "":
        additional_param = ["25", "y"]

    if len(additional_param) != 2:
        return False

    max_paper_retrieval = helper.map_yes_no(additional_param[0].strip(), 0)
    reporting_changes = helper.map_yes_no(additional_param[1].strip(), 1)

    if max_paper_retrieval is None or reporting_changes is None:
        return False

    return True

def _pull_data(update_option, session, queries, additional_param, status):
    """
    Pulls data from the selected source based on the provided queries and parameters.
    
    Parameters:
    - update_option: Source to pull data from.
    - session: Streamlit's session state.
    - queries: List of queries to search for.
    - additional_param: List of additional parameters.
    - status: Streamlit status object for displaying messages.
    """
    
    status.write(f"Pulling data from {update_option}...")
    max_paper_retrieval = int(additional_param[0])
    reporting_changes = bool(additional_param[1] == 'y')

    if update_option == "arXiv" or update_option == "ALL":
        arxiv.pull_requests(session.db_path, queries, 0, max_paper_retrieval, reporting_changes, 1)
    if update_option == "Scopus" or update_option == "ALL":
        scopus.pull_requests(session.db_path, queries, 0, max_paper_retrieval)

    status.write(f"Succesfully obtained {', '.join(queries)} data from {update_option}!")
    helper.time.sleep(2.5)
    status.empty()

def _remove_duplicates_from_database(col1, session):
    """
    Removes duplicate entries from the database.
    
    Parameters:
    - session: Streamlit's session state.
    - col1: Streamlit column object for displaying content.

    Returns:
    None
    """

    status = helper.st.empty()

    status.write("Removing duplicate entries from Database...")
    session.db_manager.dedupe_curr_db()
    status.write("Succesfully removed duplicate entries from Database!")

    helper.time.sleep(2.5)
    status.empty()

    display_database(col1, session)


def _wipe_database(col1, session):
    """
    Wipes the database after confirming with the user.
    
    Parameters:
    - session: Streamlit's session state.
    - col1: Streamlit column object for displaying content.
    """

    status = helper.st.empty()
    helper.st.warning("Are you sure? This action cannot be undone.")
    yes_or_no = helper.st.columns([1,1])

    if yes_or_no[0].button("Yes"):
        session.db_manager.reset_curr_db()
    if yes_or_no[1].button("No"):
        status.write("")

    status.empty()
    display_database(col1, session)
