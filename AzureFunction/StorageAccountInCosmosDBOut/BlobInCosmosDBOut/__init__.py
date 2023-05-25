import logging

import azure.functions as func
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from azure.cosmos import CosmosClient
from azure.core.exceptions import ResourceExistsError
import os, uuid, time


def main(myblob: func.InputStream, image: func.Out[func.InputStream], outputDocument: func.Out[func.Document]) -> str:
    AZURE_SA_CONNECTION_STRING = os.getenv('MyStorageAccountAppSetting')
    AZURE_COSMOS_CONNECTION_STRING = os.getenv('CosmosDbConnectionString')
    logging.info(f'Python blob trigger function processed blob. \n'
                 f'Name:{myblob.name}\n'
                 f'Blob Size: {myblob.length} bytes')
    
    if not myblob.name.lower().endswith(('.jpg', '.png')):
        logging.info(f'Blob {myblob.name} does not have a valid extension')
        return
    
    blobname = myblob.name.split('/')[-1]
    logging.info(f"blobname is {blobname}")
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_SA_CONNECTION_STRING)
    source_blob = blob_service_client.get_blob_client(container='upload', blob=blobname)
    logging.info(f"####\nsource_url={source_blob.url}\n#####\n")
    destination_container_client = ContainerClient.from_connection_string(AZURE_SA_CONNECTION_STRING, container_name='persist')#blob_service_client.get_container_client(container='persist')
    try:
        destination_container_client.create_container()

    except ResourceExistsError:
        pass

    destination_blob = destination_container_client.get_blob_client(blob=f"image/{blobname}")
    # destination_blob.upload_blob_from_url(source_url=source_blob.url, overwrite=True)
    destination_blob.start_copy_from_url(source_url=source_blob.url)
    logging.info(f'Uploading {myblob.name} to image folder')
    #time.sleep(3)
    source_blob.delete_blob(delete_snapshots="include")
    logging.info(f'deleting {myblob.name} from the upload container')
    cosmos_client = CosmosClient.from_connection_string(conn_str=AZURE_COSMOS_CONNECTION_STRING)
    record = {
        "id" : str(uuid.uuid5(uuid.NAMESPACE_DNS, f"persist/image/{blobname}")),
        "name": blobname,
        "container": "persist",
        "folder": "image"
    }
    outputDocument.set(func.Document.from_dict(record))


    


