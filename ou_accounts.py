import argparse
from typing import Dict, Any
import json
import boto3
from botocore.exceptions import ClientError

# Variable JSONtype for Typing
JSONDict = Dict[str, Any]

PARSER = argparse.ArgumentParser()

def _main():
    '''
    Main method prints JSON of all accounts' Id & Name in an AWS Org OU.
    '''

    PARSER.add_argument(
        "--ou",
        type=str,
        required=True,
        help="Id of AWS Org OU. Takes a string"
    )
    #Gather k,v in PARSER
    args = vars(PARSER.parse_args())

    print(accounts_by_ou(ou_id=args['ou']))

def accounts_by_ou(ou_id: str, next_token: str = '', **kwargs) -> JSONDict:
    '''
    Function that utilizes looping with NextToken to gather all accounts in OU
    '''
    
    if 'client' not in locals():
        client = boto3.client('organizations')
    if 'temp_list' not in locals():
        temp_list = []
    if not next_token:
        try:
            accounts = client.list_accounts_for_parent(ParentId=ou_id, MaxResults=20)
        except ClientError as error:
            raise error
    else:
        try:
            accounts = client.list_accounts_for_parent(
                ParentId=ou_id,
                NextToken=next_token,
                MaxResults=20
            )
        except ClientError as error:
            raise error
    for account in accounts['Accounts']:
        temp_list.append(dict(name=account['Name'], account_id=account['Id']))
    if accounts.get('NextToken'):
        accounts_by_ou(ou_id=ou_id, client=client, temp_list=temp_list,
                       next_token=accounts.get('NextToken'))
    return json.dumps(temp_list)

if __name__ == "__main__":
    _main()
