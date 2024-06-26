# NYC Motor Vehicle Collisions Web Application

This web application allows users to retrieve and analyze motor vehicle collision data in New York City.

## Setup Instructions

### Prerequisites

- Python 3.8.10
- MySQL database server installed and running.

### Installation Steps

1. Clone the project repository:
   ```bash
   git clone <repository_url>

2. Navigate to the project directory:
   ```bash
   cd <project_directory>
   
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt

The dependencies used in the Flask application are:

1. Flask: A web framework for building web applications in Python.
2. pymysql: A Python MySQL client library for interacting with MySQL databases.
3. csv: A module for reading and writing CSV files.
4. StringIO: A utility class for handling in-memory string buffering, used for creating CSV data in memory.

   ```bash
   pip install Flask
   pip install flask-mysqldb
   pip install --upgrade Flask Werkzeug

### Database Setup
Create a MySQL database named nyccrashes.
Import the provided dataset into the crash table or create a similar table with the specified schema.

### Data Loading Process
The source data for the application was loaded into the MySQL database using Alteryx:
1. Utilized Alteryx to load the source data from a CSV file into the MySQL database.
2. Used the Autofield tool in Alteryx to analyze the data and determine appropriate data types and sizes for the database columns.

### Configuration
Open the app.py file in a text editor.
Modify the mysql_config dictionary to match your MySQL database configuration (host, user, password).

### Running the Application
1. Start the Flask development server:
   ```bash
    python app.py
2. Access the application in your web browser at http://localhost:5000.

### Usage
1. Use the dropdown menu to select a borough.
2. Enter a date or collision ID to filter crash records.
3. Click "View Data" to retrieve and display crash records.
4. Click "Download Data" to download crash records in CSV format.

### Web Application 
<br>
<p align="center">
	<img src="Web Application.png" width='100%'><br><br>
</p>



   
