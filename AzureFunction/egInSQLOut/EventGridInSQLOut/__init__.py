import json, os
import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContainerClient


def main(event: func.EventGridEvent, product: func.Out[func.SqlRow]):
    SA_CONNECTION_STRING = os.getenv('SA_CONNECTION_STRING')
    # SQLDB_CONNECTION_STRING = os.getenv('SQLDB_CONNECTION_STRING')
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })
    logging.info('Python EventGrid trigger processed an event: %s', result)

    blob = event.subject.split('/')[-1]
    if not blob.lower().endswith(('.jpg', '.jepg', '.png')):
        logging.info(f'Blob {blob} does not have a valid extension')
        return

    blob_service_client = BlobServiceClient.from_connection_string(conn_str=SA_CONNECTION_STRING)
    source_blob = blob_service_client.get_blob_client(container='upload', blob=blob)
    destination_blob = blob_service_client.get_blob_client(container='persist', blob=blob)
    # destination_blob.upload_blob_from_url(source_url=source_blob.url, overwrite=True)
    destination_blob.start_copy_from_url(source_blob.url)
    # logging (f"copy_dict: {copy_dict}") 
    # if "success" != copy_dict['copy_status']:#destination_blob.get_blob_properties().copy.status:
    #     logging (f"copy {blob} to destination container failed")
    #     return

    if source_blob.exists():
        source_blob.delete_blob(delete_snapshots="include")

    record = {
        "name": blob,
        "container": "persist",
        "folder": "image"      
    }
    logging.info(f'{record}')
    row = func.SqlRow.from_dict(record)
    product.set(row)

