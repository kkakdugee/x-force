#  X-Force NLP Visualizer

##  Table of Contents

1. [Overview](#overview)

2.  [Installation Guide](#installation-guide)

3.  [User Guide](#user-guide)
  
# Overview
The X-Force NLP Visualizer is a research assistance tool, aimed to offer a streamlined and efficient way to identify trending topics in scientific and academic research. This tool provides visual analytics of key trends and hot topics in specific research domains by parsing through multiple academic databases.

#  Installation Guide
  
###  Prerequisites

Before you can use this software, you need to install Python on your computer. If you already have Python installed, you can skip to "**Step 1: Download the Project**".

1. Download the latest version of Python from the official website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/) 
2. Run the installer. In the first screen of the installation wizard, check the box that says "**Add Python to PATH**", then click "**Install Now**".

### Step 1: Download the Project
To utilize X-Force NLP Visualizer, the first step involves obtaining a copy of the project files. This can be achieved in two ways: by cloning the project repository or by downloading and extracting a .zip file of the project. Here are the steps for both methods:

 ***Option 1: Clone the Repository***:
If you have `git` installed on your system, you can clone the repository directly. Cloning a repository creates a local copy of the project on your machine, maintaining the repository structure. To clone the repository, open your terminal or command line interface, navigate to the directory where you want to place the project, and run the following command:

`git clone https://github.com/kkakdugee/x-force.git`

***Option 2: Download the ZIP File***:
If you don't have `git` installed or if you prefer to download the files manually, you can do so by clicking the `Code` button on the repository page and then clicking `Download ZIP`. After downloading the ZIP file, extract its contents into your desired directory. Remember, the directory where you extract or clone the project files will be referred to  as the 'root directory' for the project.

### Step 2: Run the Executable
Locate the batch file in the root directory of the project (it should be named `run.bat`). Run this file by  double-clicking it. This executable file will verify your Python installation, handle the installation of necessary dependencies automatically, and start the X-Force NLP Visualizer software tool.

# User Guide
This section will guide you through the process of using X-Force NLP Visualizer's features. It provides a detailed walkthrough of updating & analyzing the database, as well as graph configurations and feedback/support tickets.

## Major functions 
1. [Updating the Database](#updating-the-database): Allows you to update your database with data from Scopus, arXiv, or both, based on your specified queries. 
2. [Analyzing the Database](#analyzing-the-database): Enables you to analyze the trends in your research domain based on the updated database. 
3. [Graph Configurations](#graph-configurations): Provides various configuration options to customize your trend graphs. 
4. [Feedback/Help](#feedback-help): Offers a feedback system to help improve your user experience and aid in troubleshooting.
 ---
 
## 1. Updating the Database

![Update DB Interface](./images/readme/Updating%20Database%20Interface.png)


1. **Database Preview**: A preview of the current state of your database is displayed. You can control the number of rows shown using the slider at the side of the page.
2.  **Update From**: This dropdown menu allows you to select the source from which the database will be updated. Your options are Scopus, arXiv, or both.
    
3.  **Queries**: This text box allows you to enter your search queries. You should input your queries in a comma-separated list. For example, if you wish to search for papers related to "Artificial Intelligence" and "Machine Learning", you would input "Artificial Intelligence, Machine Learning".
    
4.  **Additional Parameters (optional)**: This field allows you to specify two additional parameters: "Max Paper Retrieval" and "Reporting Changes". Enter these parameters in a comma-separated list.
    
    -   **Max Paper Retrieval**: This parameter sets the maximum number of papers that the database update will retrieve from the selected sources.
    -   **Reporting Changes**: When set to "True", this parameter will generate a report of the changes made during the update process.
5.  **Submit**: Once you have filled in the above parameters as desired, click the "Submit" button to initiate the database update process. The system will then query the selected database(s) based on your input and add relevant articles to your database.
    

Beyond updating the database, X-Force NLP Visualizer also provides options for managing duplicate entries and resetting the database.

### Removing Duplicate Entries from the Database

To ensure the quality and accuracy of your research, it may be necessary to remove any duplicate entries from your database. To do this, click on the "Remove Duplicates from Database" button. The tool will automatically find and remove any duplicate entries.

### Wiping the Database

In some cases, you may need to completely reset your database. To do this, click on the "Wipe Database" button. Please note that this action is irreversible and will permanently delete all entries in your database. Be sure to backup any necessary data before proceeding with this action.

---

## 2. Analyzing the Database

![Analyze DB Interface](./images/readme/Analyze%20Database%20Interface.png)

The "Analyze Database" functionality offers four types of visualizations, each designed to help you better understand the distribution and frequency of specific keywords within your databases. These visualizations include:

1. **Database Summary**: The "Database Summary" generates a graph showing the distribution of articles among the Scopus, arXiv, and both databases.

2. **Keyword Frequency**: The "Keyword Frequency" visualization generates a graph depicting the frequency of your inputted queries from selected databases.
	- **Parameters:**
		-   **From:** Choose from Scopus, arXiv, or both as the source for your graph.
		-   **Queries:** Input your desired search queries. Format these as a comma-separated list. (e.g., "Artificial Intelligence, Machine Learning", "ALL")

 3. **Publish Frequency**: The "Publish Frequency" visualization creates a graph showing the publishing frequency of the inputted queries from selected databases.

	-	**Parameters:** Same as "Keyword Frequency"

4. **Text Frequency**: The "Text Frequency" visualization constructs a graph showing the text frequency (e.g., character/word count of title/abstract) of indicated queries from selected databases.

	-	**Parameters:** Same as "Keyword Frequency"

_Note: For "Keyword Frequency", "Publish Frequency", and "Text Frequency", be sure to select your source and input your queries in the given parameters. Each visualization relies on these inputs to provide accurate and specific results._

---
## 3. Graph Configurations

![Graph Configurations Interface](./images/readme/Graph%20Configurations%20Interface.png)

The "Graph Configurations" functionality allows you to personalize the aesthetics of your visualization graphs. Here's a rundown of the different customization options:

1. **Name Your Configuration:** Specify a custom name for your configuration to easily identify it later.

2. **Font Settings:**
	-   **Font Type:** Select your preferred font type from 'Arial', 'Times New Roman', or 'Calibri'.
	-   **Font Size:** Use the slider to choose the size of your font, with a range from 8 to 20.

3. **Figure Size:**
	-   **Figure Width:** Use the slider to adjust the width of your figure, with a range from 3.5 to 10.0.
	-   **Figure Height:** Use the slider to adjust the height of your figure, with a range from 2.75 to 10.0.

After customizing, click the 'Save Configuration' button. This will save your configuration for later use.

### Load Configuration

The "Load Configuration" option allows you to upload a pre-saved configuration file (`.rc/.matplotlibrc` format). You can also view the details of your current configuration.

1. **Upload Configuration:** Upload a previously saved configuration file.

2. **Current Configuration:** The system will display whether you're using the default configuration or a custom one. You can also view the specific details of your current configuration.

---
## 4. Feedback and Support

![Feedback & Support Interface](./images/readme/Feedback%20%26%20Help%20Interface.png)

The Feedback/Help section contains a simple form for you to fill out.

1. **Name:** Enter your name.

2. **Email:** Enter your email address where we can reach you for follow-up communications.

3. **Select Type:** Use the dropdown menu to select the nature of your communication. You can choose between "Help" if you need assistance with the tool, or "Feedback" if you want to provide comments or suggestions for improvement.

4. **Describe your suggestion/needed assistance:** In this text area, provide a detailed description of your feedback or the help you require. If you're reporting an issue, try to include as much information about what you were doing when the problem occurred and any error messages you saw.

Click the "Submit" button to send us your feedback or help request. The tool automatically creates an issue in our GitHub repository for each submitted feedback or help request, allowing us to track and respond to your needs effectively. 
