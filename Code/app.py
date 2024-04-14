from flask import Flask, jsonify, request, make_response, render_template
import pymysql.cursors
import csv
from io import StringIO

app = Flask(__name__)
 
# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password', #Enter your password here
    'database': 'nyccrashes',
    'cursorclass': pymysql.cursors.DictCursor
}

# Establish connection to MySQL database 
connection = pymysql.connect(**mysql_config)

@app.route('/')
def index():
    """
    Route to render the index.html template.
    Fetches distinct boroughs from the database to populate a dropdown menu.
    """
    with connection.cursor() as cursor:
        sql = 'SELECT DISTINCT BOROUGH FROM crash WHERE BOROUGH IS NOT NULL'
        cursor.execute(sql)
        result = cursor.fetchall()
    # Extract Boroughs from the result
    boroughs = [record['BOROUGH'] for record in result]
    return render_template('index.html', boroughs=boroughs)

@app.route('/api/records', methods=['GET'])
def get_records():
    """
    Route to retrieve crash records based on user-defined parameters.
    Supports filtering by borough, crash date, collision ID, pagination, and CSV download.
    """
    # Extract parameters from the request query string
    borough = request.args.get('borough')
    crash_date = request.args.get('crashDate') 
    collision_id = request.args.get('collisionId')
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=50, type=int)
    download = request.args.get('download')

    # Calculate offset for pagination
    offset = (page - 1) * limit

    with connection.cursor() as cursor:
        # Construct the SQL query based on the provided parameters
        sql = 'SELECT * FROM crash WHERE 1=1'
        params = []

        if borough:
            sql += ' AND BOROUGH = %s'
            params.append(borough)
        if crash_date:
            # Assuming the date format is MM/DD/YYYY
            sql += ' AND CRASH_DATE = %s'
            params.append(crash_date)
        if collision_id:
            sql += ' AND COLLISION_ID = %s'
            params.append(collision_id)
        
        # Add pagination
        sql += ' LIMIT %s OFFSET %s'
        params.extend([limit, offset])

        cursor.execute(sql, params)
        result = cursor.fetchall()

    if download:
        # Convert result to CSV format
        csv_data = StringIO()
        csv_writer = csv.DictWriter(csv_data, fieldnames=result[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(result)
        
        # Create a response with CSV data
        response = make_response(csv_data.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=crash_data.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response
    else:
        return jsonify(result)

@app.route('/api/records/<borough>', methods=['GET'])
def get_records_by_borough(borough):
    """
    Route to retrieve crash records filtered by borough.
    """
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM crash WHERE BOROUGH = %s LIMIT 50'
        cursor.execute(sql, (borough,))
        result = cursor.fetchall()
    return jsonify(result)
 
"""@app.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    download = request.args.get('download', default=None, type=str)

    offset = (page - 1) * limit

    with connection.cursor() as cursor:
        sql = 'SELECT * FROM crash LIMIT %s OFFSET %s'
        cursor.execute(sql, (limit, offset))
        result = cursor.fetchall()

    if download:
        csv_data = StringIO()
        csv_writer = csv.DictWriter(csv_data, fieldnames=result[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(result)
        
        response = make_response(csv_data.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=paginated_crash_data.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response
    else:
        return jsonify(result)"""
    
"""@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM crash WHERE COLLISION_ID = %s'
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
    
    return jsonify(result)"""

"""@app.route('/api/download/all', methods=['GET'])
def download_all_records():
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM crash'
        cursor.execute(sql)
        result = cursor.fetchall()
    
    # Convert result to CSV format
    csv_data = StringIO()
    csv_writer = csv.DictWriter(csv_data, fieldnames=result[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(result)

    # Create a response with CSV data
    response = make_response(csv_data.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=all_crash_data.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response"""
 
if __name__ == '__main__':
    app.run(debug=True)
