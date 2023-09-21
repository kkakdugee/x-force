"""
This module contains a function related to posting GitHub Issues
"""

import helper

def feedback_help(col1):
    """
    Provides a feedback form for users to submit their feedback or request help.
    Once submitted, the feedback is posted as an issue on a specified GitHub repository.

    Parameters:
    - col1: Streamlit column object for displaying the feedback form.

    Returns:
    None
    """

    # Create a form for feedback within the provided Streamlit column
    with col1.form(key="my_feedback"):

        # Display a message prompting the user to fill out the form
        helper.st.write("Please fill out this form")

        # Collect user's name
        name = helper.st.text_input(label="Name:")

        # Collect user's email
        email = helper.st.text_input(label="Email:")

        # Allow user to select the type of their issue (either Help or Feedback)
        issue_type = helper.st.selectbox("Select Type:", options=["Help", "Feedback"])

        # Collect detailed feedback or description of the help needed
        feedback = helper.st.text_area(label="Describe your suggestion/needed assistance:")

        # Collect user's GitHub token for authentication when posting the issue
        github_token = helper.st.text_input(label="Please enter your GitHub Token:")

        # Provide a submit button for the form
        submit = helper.st.form_submit_button(label="Submit")

        # If the form is submitted
        if submit:
            # Thank the user for their feedback
            helper.st.write(f"Thank you, {name}! We will get back to you shortly.")

            # Define the GitHub API endpoint for creating issues
            url = 'https://api.github.com/repos/kkakdugee/x-force/issues'  
            headers = {
                'Authorization': f'token {github_token}',  # Authenticate using the provided GitHub token
                'Accept': 'application/vnd.github+json',  
            }
            # Define the data for the new issue
            data = {
                'title': f'{issue_type} from {name}',  # Set the issue title based on the user's name and issue type
                'body': feedback,  # Set the issue body to the user's feedback
            }

            # Send a POST request to create the new issue
            response = helper.requests.post(url, headers=headers, json=data)
