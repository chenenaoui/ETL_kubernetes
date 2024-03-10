import os
import csv
import logging
import datetime
import sqlite3

# Configure logging
logger = logging.getLogger(__name__)
logger.handlers = []
logger.setLevel(logging.INFO)
log_file_path = './logs/etl_logs.log'
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def extract(folder_path):
    logger.info(f"{current_datetime} Starting to extract data from CSV files...")
    extracted_data = []
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    for file_name in csv_files:
        logger.info(f"{current_datetime} Extracting file: {file_name}")
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            extracted_data.extend(csv_reader)
    logger.info(f"{current_datetime} Data extraction done! Total files extracted: {len(csv_files)}")
    return extracted_data


def transform(data):
    logger.info(f"{current_datetime} Starting to transform data...")
    transformed_data = []
    for row in data:
        transformed_row = {
            'product_id': int(row[1]),
            'user_id': int(row[0]),
            'product_name': row[2],
            'brand': row[3],
            'category': row[4],
            'price': float(row[5]),
            'rating': round(float(row[6]), 2),
            'color': row[7],
            'size': row[8]
        }
        transformed_data.append(transformed_row)
    logger.info(f"{current_datetime} Data Transformation done !")
    return transformed_data


def ingest_products(database_table_path, data):
    try:
        logger.info(f"{current_datetime} Starting to ingest data...")
        database_table = os.path.join(database_table_path, 'database.db')
        conn = sqlite3.connect(database_table)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Product_ID INTEGER,
                            User_ID INTEGER,
                            Product_Name TEXT,
                            Brand TEXT,
                            Category TEXT,
                            Color TEXT,
                            Size TEXT,
                            Price REAL, 
                            Rating REAL,
                            inserted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        for row in data:
            cursor.execute("SELECT Product_ID FROM Products WHERE Product_ID = ?", (row['product_id'],))
            existing_record = cursor.fetchone()
            if existing_record:
                logger.info(f"Product with ID {row['product_id']} already exists. Updating record...")
                cursor.execute(""" 
                    UPDATE Products
                    SET User_ID = ?, Product_Name = ?, Brand = ?, Category = ?, Price = ?, Rating = ?, Color = ?, Size = ?, Updated_date = CURRENT_TIMESTAMP
                    WHERE Product_ID = ? """, (row['user_id'], row['product_name'], row['brand'], row['category'], 
                                               row['price'], row['rating'], row['color'], row['size'], row['product_id']))
            else:
                logger.info(f"Inserting product with ID {row['product_id']}...")
                cursor.execute(""" 
                    INSERT INTO Products (Product_ID, User_ID, Product_Name, Brand, Category, Price, Rating, Color, Size) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """, 
                               (row['product_id'], row['user_id'], row['product_name'], row['brand'], row['category'], 
                                row['price'], row['rating'], row['color'], row['size']))
        conn.commit()
        conn.close()
        logger.info(f"{current_datetime} Data ingested successfully!")
    except Exception as e:
        logger.error(f"Unable to insert data to SQLite: {e}")
        print("Unable to insert data to SQLite:", e)


def main(folder_path, database_table_path):
    try:
        extracted_data = extract(folder_path)
        transformed_data = transform(extracted_data)
        ingest_products(database_table_path, transformed_data)
    except Exception as e:
        print(f"An error occurred during ETL process: {e}")
        logger.error(f"An error occurred during ETL process: {e}")


if __name__ == "__main__":
    main(folder_path="data/data-source/", database_table_path="data/data-output/")
