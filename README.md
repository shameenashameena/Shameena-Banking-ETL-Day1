# Azure Banking Data Engineering Project — Day 1 & Day 2

## Project Overview
This project focuses on building an **end-to-end Azure Data Pipeline** for banking data.  
- **Day 1:** File ingestion using Blob Storage and Event Grid, sending metadata to a Storage Queue.  
- **Day 2:** Processing queue messages, validating data, and storing in Cosmos DB (NoSQL) as the transformation layer.


## Storage Containers

| Container | Description |
|-----------|-------------|
| `raw` | Incoming files uploaded by users |
| `processed` | Files after validation/processing |
| `bronze` | Raw data for transformation (Day 2) |

## Day 1 — Ingestion Layer

### Stpes
1. i have uploaded atm, upi and customer files to `raw` container.
   <img width="1366" height="678" alt="Screenshot (1138)" src="https://github.com/user-attachments/assets/ef87bb35-55a1-485f-b675-19a59af7c4fc" />

2. Event Grid detects upload.
   <img width="1366" height="690" alt="Screenshot (1141)" src="https://github.com/user-attachments/assets/117148d5-a582-4ac8-a7cb-e890ebb6ffe8" />

3. Event Grid triggers Azure Function.
   <img width="1365" height="646" alt="Screenshot 2025-12-05 110836" src="https://github.com/user-attachments/assets/3ac5d11f-bb83-44d4-a7e4-3e9a5c54315c" />

4. Function extracts:
   - Blob URL
   - Timestamp
  
     <img width="1362" height="551" alt="Screenshot 2025-12-05 105919" src="https://github.com/user-attachments/assets/d5a241b1-a924-4bfc-b842-5175d1fc1ecd" />

5. Function sends metadata to Azure Queue for Day 2 processing.


## Day 2 — Trasformation Layer

| Service | Purpose |
|--------|---------|
| **Blob Storage** | Stores raw data (`raw`, `upi`, `customer`) and processed layers (`bronze`) |
| **Event Grid** | Detects new blobs in raw containers and triggers the function |
| **Service Bus Queue** | Receives metadata messages from Event Grid trigger |
| **Azure Function (Queue Trigger)** | Processes messages from Service Bus Queue |
| **Cosmos DB** | Stores validated and enriched data in BankDB containers |


1. **Raw Data Upload:**  
   - Files uploaded into `raw` container (raw, upi, customer datasets).
  <img width="1365" height="648" alt="Screenshot 2025-12-06 105315" src="https://github.com/user-attachments/assets/41b3f8a3-0f8f-420f-8d47-81dc247220cd" />


2. **Event Grid Trigger:**  
   - Detects new blob upload in raw containers.
   - Sends metadata to **Service Bus Queue**

3. **Queue Trigger Azure Function:**  
   - Listens to messages in Service Bus Queue.
   - Downloads the corresponding blob from raw container.
  <img width="1366" height="768" alt="Screenshot (1154)" src="https://github.com/user-attachments/assets/f5d8460a-2540-4f21-bc7e-ffa0996225c1" />

  <img width="1365" height="608" alt="Screenshot 2025-12-06 105303" src="https://github.com/user-attachments/assets/e739e44b-59e5-49ee-a0e6-28f5c5dd52c6" />
      
4. **Cosmos DB Storage:**  
   - Database created: `BankDB`.
   - Containers created inside BankDB for storing processed banking data.
  <img width="1366" height="673" alt="Screenshot (1163)" src="https://github.com/user-attachments/assets/c4af3d91-464c-44c3-83b2-400b1e64d437" />

  <img width="1366" height="724" alt="Screenshot (1165)" src="https://github.com/user-attachments/assets/18d8433e-9730-4aca-a47c-0f072a9c7cd2" />





