import logging
import datetime
import sqlite3
from flask import Flask, jsonify

# Configure logging
logger = logging.getLogger(__name__)
logger.handlers = []
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs/api_logs.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Global variables
DB_FILE = './data/data-output/database.db'
app = Flask(__name__)


def get_data_from_db(limit):
    logger.info(f"{current_datetime} get the first 10 products from db ...")
    conn = sqlite3.connect(DB_FILE)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Products ORDER By Product_ID  LIMIT ?", (limit,))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except Exception as e:
            logger.info(f"{current_datetime} error to get products")
            print("Error fetching data from the database:", e)
            return None
    else:
        logger.error(f"{current_datetime} Unable to get connect to database")
        print("Unable to connect to the database")
        return None


@app.route('/read/first-chunck', methods=['GET'])
def get_first_chunk():
    logger.info(f"{current_datetime} Starting Flask App ...") 
    data = get_data_from_db(10)
    if data:
        results = []
        for row in data:
            product = {"Product ID": row[1],
                       "User_ID": row[2],
                       "Product Name": row[3],
                       "Brand": row[4],
                       "Category": row[5],
                       "Color": row[6],
                       "Size": row[7],
                       "Price": row[8],
                       "Rating": row[9]
                       }
            results.append(product)
            response = {
                "status": "success",
                "message": "First 10 products fetched successfully",
                "data": results
            }            
        logger.info(f"{current_datetime} showing the first 10 products") 
        return jsonify(response), 200

    else:
        logger.error(f"{current_datetime} Unable to get connect to database")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


if __name__ == '__main__':
    print("\n==== View the first 10 products ===")
    app.run(host="0.0.0.0", port=5000)
