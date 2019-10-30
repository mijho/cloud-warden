"""Configuration - Static vars"""

import boto3
import os

ASG_CONFIG = boto3.client('autoscaling', region_name='eu-west-1')
EC2_CONFIG = boto3.client('ec2', region_name='eu-west-1')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
SAWMILL_DEVELOPER_LOGS = os.environ.get('SAWMILL_DEVELOPER_LOGS')
SAWMILL_PB_MODE = os.environ.get('SAWMILL_PB_MODE')
AWS_REGIONS = [
    'us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-east-1', 'ap-south-1', 'ap-northeast-1',
    'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'cn-north-1',
    'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north01', 'me-south-1',
    'sa-east-1', 'us-gov-east-1', 'us-gov-west-1'
]
WARDEN_SCHEDULES = ['OfficeHours', 'ExtendedHours', 'DailyOnDemand', 'WeeklyOnDemand', 'terraform']
OFF_STATE = ['shutting-down', 'terminated', 'stopping', 'stopped']
ON_STATE = ['pending', 'running']
