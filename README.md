## User data analytics pipeline using AWS services

### Table of Contents
1. [Introduction](README.md#introduction)
1. [Data pipeline](README.md#data-pipeline)
1. [How to setup the pipeline](README.md#how-to-setup-the-pipeline)
1. [Testing](README.md#testing)
1. [Future work](README.md#future-work)
1. [Contact Information](README.md#contact-information)


### Introduction
This repository provides an API endpoint for posting user details such as name, address and contact in a JSON format. Specific records of interest are then extracted and stored in an S3 bucket for further analysis.

### Data pipeline 

###### API Gateway
AWS API Gateway is used to provide a REST API.

###### Backend
Lambda function is chosen as a backend to process requests because it is well suited to the use-case compared to a traditional EC2. 

###### Data store
Processed data is stored in S3. To accomodate future changes in requirements, the raw unprocessed data is stored as a backup in a separate S3 bucket as well.
###### Connecting backend to data store (S3)
There are a number of approaches for pushing data from the backend (lambda function) to S3.

- *Direct:* In this case, the backend lambda function directly writes into S3. This is the most cost efficient option as there are no intermediary services involved. However, there is no easy way for appending into an S3 file object. So the options are either to create a new S3 file for every request or to access an existing file, append to it and put it back to S3.

- *SQS*: This option uses AWS SQS to buffer incomming requests so that another lambda function could process them and write them into S3. However, the SQS documentation does not explicitly state if it is possible to trigger a lambda function when queue length reaches a certain threshold. So the options are to configure CloudWatch to periodically invoke the lambda function, or to let SQS trigger the lambda function for every incoming request. In the latter case, we are better off using the *Direct* approach.

- *Kinesis Data Firehose:* In this case, the backend lambda function places each request into a Kinesis delivery stream. Assuming requests come in a stream, the advantage of this approach is twofold. First, Firehose has a builtin buffering feature to accumulate requests before a data transformation lambda function is triggered. Second, it can be configured to automatically backup raw data to s3. This is the approach used in this code base.

###### ETL

AWS Glue is used to crawl S3 buckets to create queryable tables. 

###### Analytics 

AWS Athena is used to query and analyze data tables created by Glue using standard SQL. Athena expects the data to be written one record per line. This requirement forced some manual work in handling the processed data in Kinesis Firehose.

The data pipeline is shown in the following figure.

<center><img src="img/pipeline.png" align="middle" style="width: 400px; height: 300px" /></center>

### How to setup the pipeline
###### Setup AWS credentials as environmental variables

Make sure the user has sufficient permission to create and modify the services discussed above.
```
export AWS_ACCESS_KEY_ID="access-key"
export AWS_SECRET_ACCESS_KEY="secret-key"
export AWS_DEFAULT_REGION="region"
```
###### Clone this repository

```bash
git clone https://github.com/mEyob/user-data`
```

###### Infrastructure as a Code using Terraform

S3 bucket names should be globally unique accross all AWS accounts. To avoid the `BucketAlreadyExists` Error, change the bucket names in [names.tfvars](terraform/names.tfvars) before proceeding to the following Terraform commands. Also, change the Firehose Delivery Stream
destination bucket name in [transformer-lambda.py](src/transformer-lambda.py) to a new 
one defined in names.tfvars.
Next, change the working directory to the [terraform](terraform) folder and run the following commands.

```
terraform init
terraform plan -var-file="names.tfvars"
terraform apply -var-file="names.tfvars"
```

When the infrastructure is setup successfully, the URL generated by API Gateway will be printed to the terminal.

When commands like `terraform plan` or `terraform apply` are executed, Terraform loads configuration files ending in `.tf` for the given directory (module). The order in which resources are declared in these files has no significance as Terraform first builds a [dependence graph](https://www.terraform.io/docs/internals/graph.html) for the resources, which is then used for generating a plan, refreshing state or making other changes.

The dependency graph can be obtained by running the command

```
terraform graph
```

###### Terraform graph example

Consider a simple example where we want to spin up a single EC2 with an Elastic IP  within a specific subnet of a specific VPC. See the example configuration [here](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip). The following figure shows the dependency graph for this simple case. 

<center><img src="img/simple-graph.svg" align="middle" style="width: 400px; height: 300px" /></center>

The VPC needs to be created first, followed by the Internet Gateway and the subnet before the instance can be created and an EIP attached to it.

Similarly, the dependency graph for this project is shown [here](img/graph.svg).

### Testing

Unit tests for the backend and transformer lambdas can be done using the scripts in the [test](test) folder. 

To test the pipeline (integration test), run the [test_user_info.py](test/test_user_info.py) module and enter
the URL generated above. The test script requires the `requests` python module, which can be 
installed as 

```
pip install requests
```

### Future work

This code base is created as a prototype in a short period of time, so it could benefit from further work as discussed below.

###### ETL and Analytics

Glue and Athena are used in this code base. However, a quick Google search reveals a number of other alternative/complementary services such as Stitch, Elastic Search and Kibana. Comparing and benchmarking these alternatives for a specific use-case can be a compelling path to follow.

###### Terraform 
The code for the lambda functions could be zipped and stored in S3 for versioning.

### Contact information
[Misikir Eyob](https://meyob.github.io)

[LinkedIn](https://www.linkedin.com/in/misikir-eyob/)

mikireyob@gmail.com
