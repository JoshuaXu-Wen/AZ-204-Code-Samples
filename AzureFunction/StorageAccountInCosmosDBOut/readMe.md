# BlobTrigger - Python

The `BlobTrigger` makes it incredibly easy to react to new Blobs inside of Azure Blob Storage. This sample demonstrates a simple use case of processing data from a given Blob using Python.

## How it works

For a `BlobTrigger` to work, you provide a path which dictates where the blobs are located inside your container, and can also help restrict the types of blobs you wish to return. For instance, you can set the path to `samples/{name}.png` to restrict the trigger to only the samples path and only blobs with ".png" at the end of their name.

## Code Sample 
The code will monitor the blob trigger and if new blob is upload / created in the `upload` container,
1. the Azure function will check if the blob is an image (jpg, png)
2. if the blob is an image, it will be copied to another container `persist` and be kept in the folder of `image`
3. otherwise, no actions
4. after the image being kept in the destination folder, the source blob will be deleted from the `upload` container, and, 
5. wirte a record in the Cosmos DB container with a unique id (partition key) generated from the path of the image.