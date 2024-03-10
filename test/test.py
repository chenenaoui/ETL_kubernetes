import unittest
import os
import sys
import sqlite3
import logging
import datetime

# Configure logging
logging.getLogger().handlers = []
logging.basicConfig(filename='./logs/test_logs.log', level=logging.INFO)
logger = logging.getLogger(__name__)
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from src.etl import extract, transform, ingest_products
from src.flask_api import app


class TestETLIntegration(unittest.TestCase):
    def setUp(self):        
        self.csv_files = 'data/test_data/'
        self.database_table_path = 'data/data-output/'

    def test_etl_pipeline(self):

        logger.info(f"{current_datetime} ================= Test ETL ================= ")
        # Test Extract data
        extracted_data = extract(self.csv_files)
        self.assertTrue(all(len(row) == 9 for row in extracted_data))
        logger.info(f"{current_datetime} :Test ETL Pipeline: Extracted data: {extracted_data}")

        # Test Transform data
        transformed_data = transform(extracted_data)
        self.assertTrue(all(len(row) == 9 for row in transformed_data))
        logger.info(f"{current_datetime} :Test ETL Pipeline: Transform data: {transformed_data}")

        # Test Ingest data
        ingest_products(self.database_table_path, transformed_data)
        logger.info(f"{current_datetime} :Test ETL Pipeline: Ingest data: {transformed_data}")

        # Check if the database table has been correctly filled in
        db_file = os.path.join(self.database_table_path, 'database.db')
        self.assertTrue(os.path.exists(db_file))
        logger.info(f"{current_datetime} :Test ETL Pipeline: Database file exists: {os.path.exists(db_file)}")

        # Connect to the Products Table
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        rows = cursor.fetchall()

        # Check for null values in the products table
        for row in rows:
            self.assertIsNotNone(row[1])  # Product_ID
            self.assertIsNotNone(row[2])  # User_ID
            self.assertIsNotNone(row[3])  # Product_Name
            self.assertIsNotNone(row[4])  # Brand
            self.assertIsNotNone(row[5])  # Category
            self.assertIsNotNone(row[6])  # Color
            self.assertIsNotNone(row[7])  # Size
            self.assertIsNotNone(row[8])  # Price
            self.assertIsNotNone(row[9])  # Rating

            # Check if product name is not empty
            self.assertNotEqual(row[3], "")

            # Check if brand is not empty
            self.assertNotEqual(row[3], "")
            
            # Check if categories is not empty
            self.assertNotEqual(row[5], "")

            # Check if price is non-negative
            self.assertGreaterEqual(row[8], 0)
           
            # Check if rating is non-negative
            self.assertGreaterEqual(row[9], 0)
        logger.info(f"{current_datetime} : Test ETL Pipeline: Check Data Quality Done")


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_first_chunck(self):
        logger.info(f"\n {current_datetime} ================= Test Flask App ================= ")
        response = self.app.get('/read/first-chunck')
        data = response.get_json()

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)
        logger.info(f"Test Flask App: Response Status Code: {response.status_code}")

        # Check if the 'status' is 'success'
        self.assertEqual(data['status'], 'success')
        logger.info(f"Test Flask App: status code: {response.status_code}")

        # Check if the 'data' key in the response is a non-empty list
        self.assertTrue(data['data'])
        logger.info(f"Test Flask App: response is a non-empty list: {response.status_code}")


if __name__ == '__main__':
    unittest.main()
