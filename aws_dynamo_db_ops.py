# =========================================================================================
# !/usr/bin/env python3
# Filename: aws_dynamo_db_ops.py
# Description:Accessing dynamo_db
# Author: Bharathkumar Sivakumar <BHARATH SBK @ITSMESBK>
# Python Environment - Python3
# Usage: sdk of aws dynamodb
# ===========================================================================================

# Packages
from boto3.dynamodb.conditions import Key, Attr, And, Or
import logging
import boto3

# IN HOUSE PACKAGES 
from config import *

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                   #BASE MODULE
                   # TABLE CREATION
                   # TABLE INSERTION
                   # TABLE UPDATION
                   # TABLE GET DATA 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
#BASE MODULE 01
def get_dynamo_db_credintials(credintials_json_data):
    try:
        dynamodb_region = str(credintials_json_data["aws_encrypted_credentials"]["region_name"])
        dynamodb = get_aws_service('dynamodb', service_region_name=dynamodb_region)
    except :
        logging.error("Issue in get_dynamo_db_credintials")

#BASE MODULE 02
def get_aws_service(service_name,
                service_type=None,
                service_region_name=None,
                aws_access_key_id=None,
                aws_secret_access_key=None):
    """
    Returns the AWS service details when provided the service name
    :param service_name:
    :return:
    Otherwise can Access by directly call the function and enter the key credentials 
    """

    credentials = credintials_json_data
    if not service_region_name:
        service_region_name = region_name
    try:
        # @TODO: To be removed
        if aws_access_key_id and aws_secret_access_key:
            AWS_ACCESS_KEY_ID = aws_access_key_id
            AWS_ACCESS_KEY_SECRET = aws_secret_access_key
        else:
            AWS_ACCESS_KEY_ID = credentials['aws_encrypted_credentials']['aws_access_key_id']
            AWS_ACCESS_KEY_SECRET = credentials['aws_encrypted_credentials']['aws_secret_access_key']
        credentials = {
            'aws_access_key_id': AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': AWS_ACCESS_KEY_SECRET
        }
    except :
        logging.error("Key data error")

    if service_type == 'client':
        return boto3.client(service_name, service_region_name, **credentials)
    else:
        return boto3.resource(service_name, service_region_name, **credentials)

#TABLE CREATION 

def create_table_dynamodb(dynamodb,
                          table_name,
                          keyschema,
                          attribute_definitions=None,
                          provisioned_throughput=None):
    try:
        # create_table_queryy = """eval(keyschema)

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=eval(keyschema),
            AttributeDefinitions=eval(attribute_definitions),
            ProvisionedThroughput=eval(provisioned_throughput))
        return table
    except :
        logging.error("dynamodb table creation interrupted")

#DELETION 
def delete_dynamodb_data(dynamodb,
                         table_name,
                         keys=None,
                         partition_key=None,
                         partition_type=None,
                         search_key=None,
                         search_value=None):
    try:

        table = dynamodb.Table(table_name)
        if not partition_key:
            partition_key = 'id'
            partition_type = 'int'

        if isinstance(keys, dict):
            table.delete_item(Key=keys)
            logging.info("Deleting item: `{}` from dynamodb table: `{}`".format(
                table_name, keys))

        elif keys == 'all' and not search_key:
            table_items = get_data_dynamodb(dynamodb, table_name)
            if partition_key and partition_type:
                partition_ids = [
                    eval(partition_type)(item[partition_key])
                    for item in get_data_dynamodb(dynamodb, table_name)
                    if item[partition_key]
                ]
            else:
                partition_ids = [
                    item[partition_key]
                    for item in get_data_dynamodb(dynamodb, table_name)
                    if item[partition_key]
                ]
            if partition_ids:
                [
                    table.delete_item(Key={partition_key: id})
                    for id in partition_ids
                ]
                logging.info("Deleted items from `{}` table".format(table))
            else:
                print("No items to delete")
        elif keys == 'all' and partition_key and search_value and search_key and partition_type:
            partition_ids = [
                item[partition_key] for item in get_data_dynamodb(
                    dynamodb,
                    table_name,
                    fieldname=search_key,
                    fieldvalue=search_value,
                    scan_type=True)
            ]
            if partition_ids:
                [
                    table.delete_item(Key={partition_key: id})
                    for id in partition_ids
                ]
                print("Deleted all items from `{}` table".format(table))
            else:
                print("No items to delete")
        elif keys == 'drop':
            logging.warning("Are you sure you want to delete the table: {}".
                           format(table_name))
            logging.warning("Dropping dynamodb table: {}".format(table_name))
            table.delete()

    except Exception as error:
        error_msg = "Error: {} while deleting dynamodb items".format(error)
        logging.error(error_msg)

#FETCH DATA
def get_data_dynamodb(dynamodb,
                      table_name,
                      num_data=-1,
                      fieldname=False,
                      fieldvalue=False,
                      scan_type=False):
    """
    Get a particular item from dynamodb using scan
    :param dynamodb: dynamodb object
    :param table_name: Table name
    :param num_data: If -1 is specified gets all data, or N data
    :param fieldname: To scan the fieldname
    :param fieldvalue: fieldvalue to scan
    :param scan_type: scan_type if true with fieldname and value will get the results
    """
    try:
        table = dynamodb.Table(table_name)
        if scan_type and fieldname and fieldvalue and isinstance(fieldname, str) and not isinstance(fieldvalue, list):
            response = table.scan(FilterExpression=Attr(fieldname).eq(fieldvalue))
        elif scan_type and fieldname and fieldvalue and isinstance(fieldname, str) and isinstance(fieldvalue,
                                                                                                  list) and len(
                fieldvalue) > 1:
            response = table.scan(FilterExpression=reduce(Or, ([(Key(fieldname).eq(value)) for value in fieldvalue])))
        elif scan_type and fieldname and fieldvalue and isinstance(fieldname, list) and isinstance(fieldvalue,
                                                                                                   list) and (
                len(fieldname) == len(fieldvalue)):
            response = table.scan(
                FilterExpression=reduce(And, ([(Key(name).eq(value)) for name, value in zip(fieldname, fieldvalue)])))
        elif fieldname and fieldvalue and isinstance(fieldname, str) and not isinstance(fieldvalue, list):
            response = dynamodb.get_item(TableName=table_name, Key={fieldname: fieldvalue})
        else:
            if isinstance(fieldname, list) or isinstance(fieldvalue, list):
                logging.warning(
                    "WARNING: Couldnt filter the fieldname: {} and fieldvalue: {} for table: {}.".format(fieldname,
                                                                                                         fieldvalue,
                                                                                                         table_name))
                return []
            response = table.scan()

        if response and num_data == -1:
            item = response['Items']
            return item
        elif response and num_data >= 1:
            item = response['Items']
            return item[:num_data]

    except Exception as error:
        logging.error(error)
        return []

#FETCH DATA WITHOUT LIMITATION 
def get_data_dynamodb_without_limitations(dynamodb,
                                          table_name,
                                          num_data=-1,
                                          fieldname=False,
                                          fieldvalue=False,
                                          scan_type=False,
                                          limitations=False):
    """
    Get a particular item from dynamodb using scan
    :param dynamodb: dynamodb object
    :param table_name: Table name
    :param num_data: If -1 is specified gets all data, or N data
    :param fieldname: To scan the fieldname
    :param fieldvalue: fieldvalue to scan
    :param scan_type: scan_type if true with fieldname and value will get the results
    """
    try:
        table = dynamodb.Table(table_name)
        if scan_type:
            response = table.scan()  # FilterExpression=Attr(fieldname).eq(fieldvalue))

            data = response['Items']
            if limitations:
                while 'LastEvaluatedKey' in response:
                    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    data.extend(response['Items'])
            if fieldname and fieldvalue:
                data = [r for r in data if r[fieldname] == fieldvalue]
            return data

    except:
        logging.error("FETCH INTERRUPTED")

#INSERTATION 
def insert_data_dynamodb(dynamodb, table_name, json_data):
    """
    Insert a json into dynamodb
    :param table_name: Name of the Table
    :param json_data: JSON object
    """
    try:
        table = dynamodb.Table(table_name)
        table.put_item(Item=json_data)
        logging.info("Inserted JSON data: {} into table: `{}`".format(
            json_data, table_name))
    except :
        logging.error("INSERTION INTERUPTED")

#UPDATION 
def update_data_dynamodb(dynamodb, table_name, search_key_fields,
                         update_key_fields):
    """
    Update Json value in dynamodb
    :param dynamodb: Dynamodb object
    :param table_name: Table name
    :param fieldname: Field name
    :param fieldvalue: field value
    """
    try:

        update_fields = [
            '{} = :val{}'.format(v, i + 1)
            for i, v in enumerate(update_key_fields.keys())
        ]
        update_fields = 'SET ' + ','.join(update_fields)
        expression_attribute_values = [
            "':val{}': '{}'".format(i + 1, v)
            for i, v in enumerate(update_key_fields.values())
        ]
        expression_attribute_values = '{' + ','.join(
            expression_attribute_values) + '}'
        expression_attribute_values = eval(expression_attribute_values)
        table = dynamodb.Table(table_name)
        table.update_item(
            Key=search_key_fields,
            UpdateExpression=update_fields,
            ExpressionAttributeValues=expression_attribute_values)

    except:
        logging.error("UPDATION INTERRUPTED"}