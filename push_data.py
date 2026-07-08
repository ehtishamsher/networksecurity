import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGO_DB_URL")

ca = certifi.where()


class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):
        try:
            logging.info(f"Reading CSV file from {file_path}")
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info(f"Converted {len(records)} records to JSON format")
            return records
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {e}")
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.records = records
            logging.info("Connecting to MongoDB...")
            self.mongo_client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=ca)
            db = self.mongo_client[database]
            coll = db[collection]

            # Clear existing data first, so re-running the script doesn't create duplicates
            deleted_count = coll.delete_many({}).deleted_count
            logging.info(f"Cleared {deleted_count} existing records from {database}.{collection}")

            coll.insert_many(self.records)
            logging.info(f"Inserted {len(self.records)} records into {database}.{collection}")
            return len(self.records)
        except Exception as e:
            logging.error(f"Error inserting data to MongoDB: {e}")
            raise NetworkSecurityException(e, sys)


if __name__ == '__main__':
    logging.info("Script started")
    FILE_PATH = 'Network_Data/phisingData.csv'
    DATABASE = 'EHTISHAM_NETWORK_SECURITY'
    Collection = 'Network_Data'

    network_obj = NetworkDataExtraction()
    records = network_obj.cv_to_json_convertor(file_path=FILE_PATH)
    print(f"Total {len(records)} records extracted successfully from the file {FILE_PATH}")

    no_of_records = network_obj.insert_data_to_mongodb(records, DATABASE, Collection)
    print(f"Total {no_of_records} records inserted successfully into the database {DATABASE} and collection {Collection}")
    logging.info("Script completed successfully")