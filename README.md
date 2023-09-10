#  X-Force NLP Visualizer

##  Table of Contents

1. [Overview](#overview)

2. [Installation Guide](#installation-guide)

3. [User Guide](#user-guide)
  
# Overview
The NLP Research Visualizer is a research assistance tool, aimed to offer a streamlined and efficient way to identify trending topics in scientific and academic research. This tool provides visual analytics of key trends and hot topics in specific research domains by parsing through multiple academic databases.

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

### Step 2: Set your proxies, if necessary
Locate `proxies.txt` in the project root folder and input your proxies. Here is an example below:

![Proxy Config File](./images/readme/Proxy%20Config%20File.png)

_Note: The first line is your HTTP proxy and the second line is your HTTPS proxy._

### Step 3: Run the Executable
Locate the batch file in the root directory of the project (it should be named `run.bat`). Run this file by  double-clicking it. This executable file will set your proxies, verify your Python installation, handle the installation of necessary dependencies automatically, and start the NLP Research Visualizer software tool.

---

# User Guide
This section will guide you through the process of using X-Force NLP Visualizer's features. It provides a detailed walkthrough of updating & analyzing the database, as well as graph configurations and feedback/support tickets.

## Major functions 
1. [Database](#the-database): Allows you to load, configure, and update a database.
2. [Analyzing the Database](#analyzing-the-database): Enables you to analyze the trends in your research domain based on the updated database. 
3. [Graph Configurations](#graph-configurations): Provides various configuration options to customize your trend graphs. 
4. [Feedback/Help](#feedback-help): Offers a feedback system to help improve your user experience and aid in troubleshooting.
 ---

## 1. The Database

1. **Database Preview:** A preview of the current state of your database is displayed.

2. **Selecting & Creating a Database:** This tab allows you to load a pre-existing Database, or create a new Database.

![Database Loading & Preview](./images/readme/Database%20Selection%20Interface.png)

3. **Updating the Database:** This tab allows you to add entries by query to your selected Database.

![Updating the Database](./images/readme/Updating%20Database%20Interface.png)

4. **Filtering the Database:** This tab allows you to filter your selected Database.

![Filtering Database](./images/readme/Filtering%20Database%20Interface.png)

---

## 2. Analyzing the Database

![Analyze DB Interface](./images/readme/Analyze%20Database%20Interface.png)

The "Analyze Database" functionality offers six types of visualizations, each designed to help you better understand the distribution and frequency of specific keywords within your databases. These visualizations include:

1. **Database Summary:** The "Database Summary" generates a graph showing the distribution of articles among the Scopus, arXiv, and both databases.

2. **Keyword Frequency:** The "Keyword Frequency" visualization generates a graph depicting the frequency of your filtered queries from the selected database.

 3. **Publish Frequency:** The "Publish Frequency" visualization creates a graph showing the publishing frequency of your filtered queries from the selected database.

4. **Text Frequency:** The "Text Frequency" visualization generates a graph showing the text frequency (e.g., character/word count of title/abstract) of filtered queries from the selected database.

5. **Network Co-occurrence:** The "Network Co-occurrence" visualization generates a graph that displays the relationships between different keywords or terms based on their co-occurrence within the same documents.

6. **Bubble Map:** The "Bubble Map" visualization generates a graph where data is represented as bubbles or circles. The size of the bubbles typically corresponds to the frequency or importance of a keyword, indicating the density of that term within the dataset.


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

5. **GitHub Token:** Enter your GitHub Personal Access Token. 

Click the "Submit" button to send us your feedback or help request. The tool automatically creates an issue in our GitHub repository for each submitted feedback or help request, allowing us to track and respond to your needs effectively. 

_Note: A GitHub Personal Access Token can be created [here](https://github.com/settings/tokens?type=beta). Under **Repository access**, select **Only select repositories**, and select this repository (x-force). For permissions, please only enable access for **Issues**. For the access level, select **Read and write**._