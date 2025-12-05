import json
import logging
import azure.functions as func


def main(event: func.EventGridEvent, queue_msg: func.Out[str]):
    logging.info("Processing Event Grid message...")

    # here am extracting the event payload
    event_payload = event.get_json()
    file_location = event_payload.get("url", "Unknown")
    timestamp = str(event.event_time)

    # here i am preparing message for the queue
    enriched_payload = {
        "file_path": file_location,
        "triggered_at": timestamp,
        "status": "checked"
    }

    queue_msg.set(json.dumps(enriched_payload))
    logging.info(f"Message pushed to queue: {enriched_payload}")
