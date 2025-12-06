import json
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import pandas as pd
from io import StringIO


def classify_transaction(file_name):
    """Determine transaction type based on file name"""
    if "atm" in file_name:
        return "ATM"
    if "upi" in file_name:
        return "UPI"
    if "imps" in file_name:
        return "IMPS"
    if "neft" in file_name:
        return "NEFT"
    return "UNKNOWN"


def detect_suspicious(txn):
    """Simple rule-based fraud detection"""
    flags = []
    amount = float(txn.get("Amount", 0))
    txn_type = txn.get("txn_type", "")
    if amount > 50000:
        flags.append("High-value transaction")
    if txn_type == "ATM" and amount > 20000:
        flags.append("Large ATM withdrawal")
    return flags


def main(msg: func.QueueMessage):
    logging.info("Queue Trigger Executed")

    # 1️ Read queue message
    event = json.loads(msg.get_body().decode())
    blob_url = event["blob_url"]

    # 2️ Connect to Blob Storage & Cosmos DB
    storage_conn = func.Context.get_secret("AzureWebJobsStorage")
    cosmos_conn = func.Context.get_secret("COSMOS_URI")

    blob_service = BlobServiceClient.from_connection_string(storage_conn)
    blob_client = blob_service.get_blob_client_from_url(blob_url)

    cosmos = CosmosClient.from_connection_string(cosmos_conn)
    db = cosmos.get_database_client("BankDB")
    container = db.get_container_client("CleanTransactions")

    # 3️ Read file content
    content = blob_client.download_blob().readall().decode()
    file_name = blob_url.lower()

    # 4️ Classify transaction type
    txn_type = classify_transaction(file_name)

    # 5️ Convert to DataFrame & validate schema
    df = pd.read_csv(StringIO(content))
    required_cols = {"TransactionID", "Amount"}
    if not required_cols.issubset(df.columns):
        logging.error("Missing required fields")
        return

    # 6 Process records
    inserted_count = 0
    for _, row in df.iterrows():
        record = row.to_dict()
        record["id"] = record["TransactionID"]         # Cosmos requires 'id'
        record["txn_type"] = txn_type
        record["fraud_flags"] = detect_suspicious(record)

        # Deduplicate
        try:
            container.read_item(record["id"], partition_key=record["id"])
            continue
        except Exception:
            pass

        # Upsert into Cosmos DB
        container.upsert_item(record)
        inserted_count += 1

    logging.info(f" Processed file: {file_name}")
    logging.info(
        f"Inserted {inserted_count} new records into CleanTransactions"
    )
