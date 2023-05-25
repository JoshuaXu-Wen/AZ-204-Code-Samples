# Introduction

The json file is a piece of logic App code. It is a sample to monitor a container and trigger a copy action when there is a new upload/modify blob in the container.

The code:
1. copy the uploaded/modified blob to a new container
2. based on the file type (images in jpg or png format, or others), the file will be put into differnt folders.
3. if the file is an image file, the logic app will check the first 3 chars (i.e., AKL, CHC) and put the file into the correspond folder:
    * if the file name is AKL001.jpg, it will go to the folder /AKL in the destination container.
4. if the file is not an image file, the file will be sent to the "other" folder in the destination container;
5. at last, the blob in the source container will be delete after all the operations above.   
6. variable, condition control, Express with Dynamic content are used to help starters get familiar with the usage of those elements.

# Notice
* ### change the storage account, container name and other related resources accordingly
* ### assign "Contributor" or "Blob Data Contributor" role at storage account level to the logic app managed identity to allow the logic app manipulating the storage account