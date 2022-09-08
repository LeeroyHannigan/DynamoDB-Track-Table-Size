# Table Size Metrics Publisher

This sample application uses Amazon EventBridge, Lambda and CloudWatch Metrics to plot your DynamoDB tables size over time, at a granularity of 6 hour periods.


## How to start

Steps below assume you have `aws-cli` configured on your machine
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

You must also install and bootstap CDK:
- `npm install aws-cdk-lib`
- `cdk bootstrap`
---

## How to run
* Clone this repo 
  * `git clone https://github.com/LeeroyHannigan/DynamoDB-Track-Table-Size.git` 
* Navigate to the root 
  * `cd DynamoDB-Track-Table-Size`
* Install npm packages 
  * `npm i`
* Deploy CDK Stack
  * `cdk deploy`
---