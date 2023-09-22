#----------------------------------------------------
# Imports
#----------------------------------------------------
import sys
sys.path.append("../../code/Modules")
import helper
import db_functions
from database_operations import database
from visualization import analyze_database, graph_profiles
from feedback import feedback_help

#----------------------------------------------------
# Main Function
#----------------------------------------------------
def main():

    """
    Main function to run the Streamlit app.
    """

    # Set the title of the web app
    helper.st.title('NLP Research Visualizer')

    # Create a sidebar with a selection box for navigation
    with helper.st.sidebar:
        
        option = helper.st.selectbox(
            'Select from below:', 
            ['Database', 'Analyze Database', 'Graph Configurations', 'Feedback / Help']
        )

        # Display descriptions based on the selected option
        if option == 'Configure & Update Database':
            helper.st.write('This option will enable you to make configurations and update your Database.')
        elif option == 'Analyze Database':
            helper.st.write('This option will enable you to view visualizations of the selected Database.')
        elif option == 'Graph Configurations':
            helper.st.write('This option will enable you to configure your graphs.')
        elif option == 'Feedback / Help':
            helper.st.write('Suggestions or Bugs.')

    # Create multiple columns in the main panel for layout
    col1, col2 = helper.st.columns([3,1]) 

    # Create buttons in the right column based on the sidebar selection
    with col2:
        if option == "Graph Configurations" or option == "Feedback / Help":
            col2.subheader("")
        else:
            col2.subheader("Parameters")

    # Call the appropriate function based on the selected option
    if option == 'Database':
        database(col1, col2, session)
    elif option == 'Analyze Database':
        analyze_database(col1, col2, session)
    elif option == 'Graph Configurations':
        graph_profiles(col1, col2, session)
    elif option == 'Feedback / Help':
        feedback_help(col1)

#----------------------------------------------------
# Entry Point
#----------------------------------------------------
if __name__ == "__main__":
    
    # Set Streamlit page configurations
    helper.st.set_page_config(page_title="NLP Research Viz", layout="wide")

    # Initialize global session state
    global session
    session = helper.st.session_state

    # Check and initialize session state variables
    if "db_manager" not in session:
        session.db_manager = db_functions.XForce_Database()
    if "db_path" not in session:
        session.db_path = None
    if "db_selected" not in session:
        session.db_selected = False
    if "config_path" not in session:
        session.config_path = None

    # Run the main function
    main()