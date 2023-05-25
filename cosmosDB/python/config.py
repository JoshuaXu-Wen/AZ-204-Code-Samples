# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://cos-syd-cor-db001.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', '41pTc3Bv3KSKBdGhmchuBebfWo08ywBDfbwVDTvxQlW2iyUtBgVtN1U3B5BczUZqWihvZoNLtp5WACDbuFvBrQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'Items'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
    'tenant_id': os.environ.get('TENANT_ID', '84ff045a-49f1-457c-856f-98ea50ccee00'),
    'client_id': os.environ.get('CLIENT_ID', '[YOUR CLIENT ID]'),
    'client_secret': os.environ.get('CLIENT_SECRET', '[YOUR CLIENT SECRET]'),
}