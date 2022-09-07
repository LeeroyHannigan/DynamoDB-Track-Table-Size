# Table Size Metrics Publisher

This sample application uses Amazon EventBridge, Lambda and CloudWatch Metrics to plot your DynamoDB tables size over time, at a granularity of 6 hour periods.


## How to run

Steps below assume you have `aws-cli` configured on your machine and you have run `cdk bootstrap`:

* Clone this repo 
  * `git clone https://github.com/LeeroyHannigan/DynamoDB-Track-Table-Size.git` 
* Navigate to the root 
  * `cd DynamoDB-Track-Table-Size`
* Install npm packages 
  * `npm i`
* Deploy CDK Stack
  * `cdk deploy`