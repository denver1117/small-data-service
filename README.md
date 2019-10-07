![small-data-service](https://github.com/denver1117/small-data-service/blob/master/docs/images/logo.png)

## small-data-service: Serving requests to simple CSV data stored in S3 

### What is it?
`small-data-service` is an [AWS lambda function](https://aws.amazon.com/lambda/) which is 
publicly available in the [AWS serverless application repository](https://aws.amazon.com/serverless/serverlessrepo/). It can be used to serve small and simple CSV data stored in S3, one record at a time as requested. For example, given the following CSV data file stored in S3:

| productId  | productName   | productPrice  |
| ---------- | ------------- |-------------- |
| 1234       | stapler       | 2.99          |
| 1235       | scissors      | 10.05         |
| 1236       | ream of paper | 9.99          |

we can designate `productId` as the `IdCol`. The service will load the CSV into memory as each lambda container spins up.
It will parse the loaded CSV data appropriately to enable very fast key/value lookup. An example request and response:

```
request = {
    "id": 1236
    }
    
response = {
    "statusCode": 200,
    "body": {
        "productId": 1236, 
        "productName": "ream of paper", 
        "productPrice": 9.99
        }
    }
```

### Deployment
The lambda can be deployed from the AWS Serverless Application Repository. The link for `small-data-service` 
is [here](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:171665969987:applications~small-data-service).

### Use Cases
The intended use case of `small-data-service` is to provide a simple way to serve single record requests to CSV data 
stored in S3 with no infrastructure to manage. Where traditional alternatives would be to store this data in a relational data store (`Amazon RDS`), a document store (`Amazon DocumentDB`, `Amazon Elasticsearch Service`, `Amazon DynamoDB`) or in memory on one or more virtual machines (`Amazon EC2`, `Amazon EKS`), these cost time and money to setup and manage. This is often too much overhead for very simple data that is small in size. 

Here are some use cases that `small-data-service` was designed with in mind:

- **Simple document service:** Given a relatively small document store in S3, `small-data-service` can be used as a lightweight document service. Assuming a unique ID associated with each document, clients can requests the document 
details given a specific ID. The service will return the CSV row for that ID as a JSON-like response.

- **Machine learning prediction service:** Given offline machine learning predictions corresponding to an ID known
to other services in an application, `small-data-service` can be used to serve those predictions. Clients can request
the predictions for a given ID, and the service will return the CSV row for that ID as a JSON-like response.

### Parameters
The following parameters are allowed (some are required) to instantiate a deployment of the lambda function. The 
`Bucket` and `Key` parameters designate the location of the CSV data file in S3. the `IdCol` parameter specifies 
which CSV column is to be used as the ID column for making requests. The optional `Delimiter` parameter allows
customization of the CSV reader.
```
Parameters:
  Bucket:
    Type: String
    Description: (Required) The S3 bucket of your CSV file
  Key:
    Type: String
    Description: (Required) The S3 key of yor CSV file
  IdCol:
    Type: String
    Description: (Required) The name of your ID column. Must be one of the column names in the CSV file
  Delimiter:
    Type: String
    Default: ','
    Description: (Optional) Custom CSV delimiter. Defaults to comma separated
```

### Required Data Format
The specified CSV data stored in S3 needs to be a in a standard CSV format with a header line containing column names. 
The data needs to be in a single file. Custom delimiters are allowed, however the default is a standard comma separated
file. Under the hood, `small-data-service` will run `csv.reader(data, delimiter=delimiter)` on your CSV data. Any format
of data in S3 that cannot be properly parsed with the csv reader as shown will not work.

### Required Roles
The lambda function will need to run with an execution role that has read access to the specified CSV data stored in S3.

### Caveats
The main caveat is that `small-data-service` will cost more and lose performance (especially on cold start) as the CSV
data grows in size. At a certain point, the service is constrained by the upper bound on memory for a lambda function. Users will need to adjust the memory allocated to the lambda function appropriately.
