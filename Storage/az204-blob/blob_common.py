from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.storage.blob import BlobServiceClient 
from azure.storage.blob.changefeed import ChangeFeedClient
import os, time

SOURCE_FILE = 'blob_common.py'

class CommonBlobSamples(object):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    def blob_snapshots(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(container=self.container_name)
        try:
            # container_client = blob_service_client.create_container(name=self.container_name)
            container_client.create_container()
        except ResourceExistsError:
            pass
        
        # upload a blob to the container    
        with open(SOURCE_FILE, 'rb') as data:
            container_client.upload_blob(name="my_blob", data=data, overwrite=True)

        # Get a BlobClient for a specific blob
        blob_client = container_client.get_blob_client(blob="my_blob")
        
        # [START create_blob_snapshot]
        #Create a read-only snapshot of the blob at this point of time
        snapshot_blob = blob_client.create_snapshot() # metadata={'time': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}
        print(snapshot_blob)
        # print(snapshot_blob.values())
        #Get the snapshot ID
        print(snapshot_blob.get('snapshot'))
        # [END create_blob_snapshot]


    def delete_snapshot(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(container=self.container_name)
        try:
            container_client.create_container()
        except ResourceExistsError:
            pass
        
        blob_client = container_client.get_blob_client(blob="my_blob")
        blob_client.delete_blob(delete_snapshots="only")


    def delete_blobs(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(container=self.container_name)
        try:
            container_client.create_container()
        except ResourceExistsError:
            pass
        
        myblobs = container_client.list_blobs(name_starts_with="my_blob")
        # print(list(myblobs))
        container_client.delete_blobs(*myblobs)
    
    def delete_container(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(container=self.container_name)
        try:
            container_client.delete_container()
        except ResourceExistsError:
            pass

    
    def changeFeed(self):
        # blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        # container_client = blob_service_client.get_container_client(container=self.container_name)
        # try:
        #     # container_client = blob_service_client.create_container(name=self.container_name)
        #     container_client.create_container()
        # except ResourceExistsError:
        #     pass
        
        changeFeedClient = ChangeFeedClient.from_connection_string(conn_str=self.connection_string)
        changeFeeds = changeFeedClient.list_changes()
        for event in changeFeeds:
            print(event)

if __name__ == '__main__':
    sample = CommonBlobSamples()
    sample.blob_snapshots()
    time.sleep(5)
    print("delete snapshots")
    sample.delete_snapshot()
    time.sleep(5)
    print("delete the blobs")
    sample.delete_blobs()
    time.sleep(20)
    print("list change feed")
    sample.changeFeed()
    print("delete the container")
    sample.delete_container()