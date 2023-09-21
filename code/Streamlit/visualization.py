"""
This module contains functions related to data visualization.
"""

import helper
import eda_graphing

def display_image(col, image, caption):
    """
    Display an image within a specified Streamlit column.

    Parameters:
    - col: Streamlit column object for displaying the image.
    - image: Image object to be displayed.
    - caption: Caption for the image.

    Returns:
    None
    """

    with col:
        helper.st.image(image, caption=caption, use_column_width=True)



def analyze_database(col1, col2, session):
    """
    Provides visualization options for analyzing the database.

    Parameters:
    - col1: Streamlit column object for displaying the visualization.
    - col2: Streamlit column object for displaying the visualization options.
    - session: Streamlit's session state.

    Returns:
    None
    """

    # Display visualization options in the second column
    with col2:

        # Check if a database has been selected
        if session.db_selected:

            # Dropdown for selecting the type of visualization
            analyze_option = helper.st.selectbox(
                'Select Visualization',
                ['Database Summary', 'Keyword Frequency', 'Publish Frequency', 'Text Frequency', 'Network Co-Occurence', 'Bubble Map']
            )

            # Button to generate the selected visualization
            if helper.st.button("Submit"):

                # Create an instance of the graphing class
                grapher = eda_graphing.XForce_Grapher()

                # Generate and display the selected visualization
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
            # Display a warning if no database has been selected
            helper.st.warning("Please load a database in the \"Select\" tab before proceeding")


def graph_profiles(col1, col2, session):
    """
    Provides options for customizing graph profiles.

    Parameters:
    - col1: Streamlit column object for displaying graph customization options.
    - col2: Streamlit column object for displaying configuration loading options.
    - session: Streamlit's session state.

    Returns:
    None
    """

    # Display graph customization options in the first column
    with col1:
        
        # Header for the customization section
        helper.st.header('Customize Your Graph')

        # Input for naming the configuration
        config_name = helper.st.text_input("Name your configuration")

        # Subheader for font customization
        helper.st.subheader('Font')
        # Dropdown for selecting font type
        font_type = helper.st.selectbox('Select font type', options=['Arial', 'Times New Roman', 'Calibri'])
        # Slider for selecting font size
        font_size = helper.st.slider('Select font size', min_value=8, max_value=20, value=10)

        # Subheader for figure size customization
        helper.st.subheader('Figure Size')
        # Sliders for selecting figure width and height
        fig_width = helper.st.slider('Select figure width', min_value=3.5, max_value=10.0, value=7.0, step=0.25)
        fig_height = helper.st.slider('Select figure height', min_value=2.75, max_value=10.0, value=3.0, step=0.25)

        # Create a dictionary to store the configuration values
        config = {
            'font.family': font_type,
            'font.size': font_size,
            'figure.figsize': str(fig_width) + ', ' + str(fig_height),
        }

        # Button to save the configuration
        if helper.st.button('Save Configuration'):
            if config_name:
                # Save the configuration to a file
                with open(f'../../configurations/{config_name}.matplotlibrc', 'w') as f:
                    for key, value in config.items():
                        f.write(f'{key}:{value}\n')
                helper.st.success('Configuration saved successfully!')
            else:
                helper.st.error('Please add a Configuration name.')

    # Display configuration loading options in the second column
    with col2:

        # Header for the configuration loading section
        helper.st.header('Load Configuration')
        # File uploader for uploading a configuration file
        config_file = helper.st.file_uploader("Upload Configuration (.rc) File")
        # Default configuration path
        config_default = '../../configurations/default.matplotlibrc'

        # Check if the session state has a custom configuration path
        if session.config_path is None:
            session.config_path = config_default
            using_default = True
        else:
            using_default = False

        # If a configuration file is uploaded, update the session's configuration path
        if config_file is not None:
            config_file_path = helper.os.path.join('../../configurations', config_file.name)
            session.config_path = config_file_path
            using_default = False

        # Display the current configuration being used
        if using_default:
            helper.st.info(f'Currently using default configuration')
        else:
            helper.st.info(f'Currently using configuration from file: {helper.os.path.basename(session.config_path)}')

        # Try to load the selected configuration
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