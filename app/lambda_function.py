import json
import csv
import boto3
import os

def load_data(bucket, key):
    """ 
    Load S3 data as in memory string

    Args:
        bucket (str): S3 bucket name
        key (str): S3 prefix path to CSV file
    Returns:
        CSV string 
    """
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    return obj.get()['Body'].read().decode('utf-8') 

def parse_data(data, id_col, delimiter=","):
    """
    Convert CSV to dictionary with keys as
    id_col values and values as dictionary 
    representations of each row.

    Args:
        data (str): CSV string
        id_col (str): column name of ID
        delimiter (str): optional custom delimiter; default ','
    Returns:
        data dictionary
    """
    dct = {}
    count = 0
    for dat in csv.reader(data.splitlines(), delimiter=delimiter):
        if count == 0:
            names = dat
            id_index = names.index(id_col)
        else:
            dct[str(dat[id_index])] = dict(zip(names, dat))
        count += 1
    return dct
    
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': data.get(str(event["id"]))
    }
    
raw_data = load_data(os.environ["BUCKET"], os.environ["KEY"])
data = parse_data(raw_data, os.environ["ID_COL"], os.environ["DELIMITER"])
