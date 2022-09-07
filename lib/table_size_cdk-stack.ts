import * as cdk from 'aws-cdk-lib';
import { Duration, Stack } from 'aws-cdk-lib';
import { Rule, Schedule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction } from 'aws-cdk-lib/aws-events-targets';
import { PolicyStatement, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { Function, Code, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as path from 'path';

export class TableSizeCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Role for Lambda Function
    const role = new Role(this, 'TableSizeIamRole', {
      roleName: 'TableSizePublisherIamRole',
      assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
    });

    // Permissions for Role to List/Describe DDB Tables
    // PutMetric to CW Metrics and Logs to CW Logs
    const lambdaPermissions = new PolicyStatement({
      actions: [
        'dynamodb:ListTables',
        'dynamodb:DescribeTable',
        'cloudwatch:PutMetricData',
        'logs:*'
      ],
      resources: ['*'],
    });

    role.addToPolicy(lambdaPermissions)

    // Create Lambda Function
    const putMetricFunction = new Function(this, 'PutMetricFunction', {
      runtime: Runtime.PYTHON_3_9,
      functionName: 'TableSizePublishMetricFunction',
      memorySize: 512,
      timeout: Duration.minutes(5),
      handler: 'index.lambda_handler',
      code: Code.fromAsset(path.join(__dirname, '../src/lambda/')),
      role: role,
      environment: {
        REGION: Stack.of(this).region,
      }
    });

    // Create Event Bridge Rule, Triggers Every 6 Hours
    const eventRule = new Rule(this, 'ScheduleRule', {
      ruleName: 'TableSizePublisherEventRule',
      schedule: Schedule.rate(Duration.hours(6)),
      enabled: true,
      targets: [new LambdaFunction(putMetricFunction)],
    });

  }
}
