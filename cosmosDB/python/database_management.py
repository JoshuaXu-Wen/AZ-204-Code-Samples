import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.offer import ThroughputProperties

import config

# ----------------------------------------------------------------------------------------------------------
# Sample - demonstrates the basic CRUD operations on a Database resource for Azure Cosmos
#
# 1. Query for Database (QueryDatabases)
#
# 2. Create Database (CreateDatabase)
#
# 3. Get a Database by its Id property (ReadDatabase)
#
# 4. List all Database resources on an account (ReadDatabases)
#
# 5. Delete a Database given its Id property (DeleteDatabase)
# ----------------------------------------------------------------------------------------------------------

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

def find_database(client, id):
    print('1. Query for Database')

    databases = list(client.query_databases({
        "query": "SELECT * FROM r WHERE r.id=@id",
        "parameters": [
        { "name": "@id", "value": id}
        ]
    }))

    if len(databases) > 0:
        print(f"Database with id '{id}' was found'")
    else:
        print(f"No database with id '{id}' was found")

def create_database(client, id):
    print("\n2. Create Database")

    try:
        client.create_database(id=id)
        print(f"Database with id '{id}' created")
    
    except exceptions.CosmosResourceExistsError:
        print(f"A Database with id '{id}' already exists")

    # print("\n2.8 Create Database - With auto scale settings")

    # try:
    #     client.create_database(
    #         id=id,
    #         offer_throughput = ThroughputProperties(auto_scale_max_throughput=5000, auto_scale_increment_percent=0)
    #     )
    #     print(f"Database with id '{id}' created")
    # except exceptions.CosmosResourceNotFoundError:
    #     print(f"A Database with id '{id}' already exists")

def read_database(client, id):
    print("\n3. Get a Database by id")

    try:
        database = client.get_database_client(id)
        database.read()
        print(f"Database with id '{id}' was found, it's link is '{database.database_link}.")    
    except exceptions.CosmosResourceNotFoundError:
        print(f"A Database with id '{id}' does not exist")

def list_databases(client):
    print("\n4. List all Databases on an account")
    print('Databases:')
    
    databases = list(client.list_databases())

    if not databases:
        return
    
    for database in databases:
        print(database['id'])
    
def delete_database(client, id):
    print("\n5. Delete Database")

    try:
        client.delete_database(id)
        print(f"Database with id '{id}' was deleted")

    except exceptions.CosmosResourceNotFoundError:
        print(f"A database with id '{id}' does not exist")

def run_sample():
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})
    try:
        # query for a database
        find_database(client=client, id=DATABASE_ID)

        # create a database
        create_database(client, DATABASE_ID)

        # get a database using its id
        read_database(client, DATABASE_ID)

        # list all databases on an account
        list_databases(client)

        # delete database by id
        delete_database(client, DATABASE_ID)

    except exceptions.CosmosHttpResponseError as e:
        print("\nrun_sample has caught an error. {e.message}")
    
    finally:
        print("\nrun_sampl done")

if __name__ == '__main__':
    run_sample()