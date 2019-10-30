import boto3
import config
import argparse
import json

from collections import defaultdict
from sawmill.logger import Sawmill

logger = Sawmill.new_logger(__name__)


def get_instance_data(region, token) -> dict:
    logger.info('Scanning EC2 instances')

    if token == '':
        response = boto3.client('ec2', region_name=region).describe_instances(
            MaxResults=100
        )
    else:
        response = boto3.client('ec2', region_name=region).describe_instances(
            NextToken=token
        )

    return response


def process_reservations(reservation) -> list:
    logger.info('Processing Reservation')
    instance_states = []

    for _, instances in enumerate(reservation['Reservations']):
        instance = instances['Instances'][0]
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        tags = instance['Tags']
        name = 'unamed'
        shutdown_policy = 'None'

        for tag in tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
            elif tag['Key'] == "ShutdownPolicy":
                shutdown_policy = tag['Value']

        instance_state = {'Name': name, 'InstanceId': instance_id, 'State': state, 'ShutdownPolicy': shutdown_policy}
        instance_states.append(instance_state)

    return instance_states


def define_actions(manifest, regions, schedule, action) -> list:
    instance_manifest = []
    for region in regions:
        for _, instances in enumerate(manifest[region]):
            for instance in instances:
                if instance['ShutdownPolicy'] == 'AlwaysOn':
                    instance_dict = {'Region': region, 'Action': 'none'}
                    instance.update(instance_dict)
                    instance_manifest.append(instance)
                elif instance['ShutdownPolicy'] == 'OfficeHours':
                    if schedule == 'OfficeHours' and action == 'on' and instance['State'] in config.OFF_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_on'}
                    elif schedule == 'OfficeHours' and action == 'off' and instance['State'] in config.ON_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_off'}
                    else:
                        instance_dict = {'Region': region, 'Action': 'none'}
                    instance.update(instance_dict)
                    instance_manifest.append(instance)
                elif instance['ShutdownPolicy'] == 'ExtendedHours':
                    if schedule == 'ExtendedHours' and action == 'on' and instance['State'] in config.OFF_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_on'}
                    elif schedule == 'ExtendedHours' and action == 'off' and instance['State'] in config.ON_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_off'}
                    else:
                        instance_dict = {'Region': region, 'Action': 'none'}
                    instance.update(instance_dict)
                    instance_manifest.append(instance)
                elif instance['ShutdownPolicy'] == 'DailyOnDemand':
                    if schedule == 'DailyOnDemand' and action == 'on' and instance['State'] in config.OFF_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_on'}
                    elif schedule == 'DailyOnDemand' and action == 'off' and instance['State'] in config.ON_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_off'}
                    else:
                        instance_dict = {'Region': region, 'Action': 'none'}
                    instance.update(instance_dict)
                    instance_manifest.append(instance)
                elif instance['ShutdownPolicy'] == 'WeeklyOnDemand':
                    if schedule == 'WeeklyOnDemand' and action == 'on' and instance['State'] in config.OFF_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_on'}
                    elif schedule == 'WeeklyOnDemand' and action == 'off' and instance['State'] in config.ON_STATE:
                        instance_dict = {'Region': region, 'Action': 'power_off'}
                    else:
                        instance_dict = {'Region': region, 'Action': 'none'}
                    instance.update(instance_dict)
                    instance_manifest.append(instance)
                else:
                    instance_dict = {'Region': region, 'Action': 'none'}
                    instance.update(instance_dict)
                    print(f'{instance} does not have a valid shutdown policy please rectify before next run')
                    instance_manifest.append(instance)

    return instance_manifest


def power_instance_on(instance, region, dryrun) -> None:
    response = boto3.client('ec2', region_name=region).start_instances(
        InstanceIds=[
            instance,
        ],
        DryRun=dryrun
    )
    logger.debug(str(response))


def power_instance_off(instance, region, dryrun) -> None:
    response = boto3.client('ec2', region_name=region).stop_instances(
        InstanceIds=[
            instance,
        ],
        DryRun=dryrun
    )
    logger.debug(str(response))


def console_handler(schedule, action, regions, dryrun):
    instance_manifest = defaultdict(list)
    for region in regions:
        instances = []
        reservation = get_instance_data(region, '')
        instances = instances + process_reservations(reservation)

        while 'NextToken' in reservation:
            next_token = reservation['NextToken']
            reservation = get_instance_data(region, next_token)
            instances = instances + process_reservations(reservation)
        instance_manifest[region].append(instances)

    action_manifest = define_actions(instance_manifest, regions, schedule, action)
    for instance in action_manifest:
        if instance['Action'] == 'power_on':
            instance_name = instance['Name']
            logger.info(f'Powering on {instance_name}')
            power_instance_on(instance['InstanceId'], instance['Region'], dryrun)
        elif instance['Action'] == 'power_off':
            instance_name = instance['Name']
            logger.info(f'Powering off {instance_name}')
            power_instance_off(instance['InstanceId'], instance['Region'], dryrun)


def lambda_handler(event, context):
    logger.debug('Entered via Lambda handler')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Cloud-warden will power on or off EC2 instance according to the schedule requested.'
    )
    parser.add_argument(
        '-s',
        '--schedule',
        dest='schedule',
        nargs=1,
        action='store',
        choices=config.WARDEN_SCHEDULES,
        required=True,
        help='Set which tag value to target'
    )
    parser.add_argument(
        '-a',
        '--action',
        dest='action',
        nargs=1,
        choices=['on', 'off'],
        required=True,
        action='store',
        help='Set whether to power off or on the tagged instances'
    )
    parser.add_argument(
        '-r',
        '--regions',
        dest='regions',
        nargs='+',
        choices=config.AWS_REGIONS,
        default='eu-west-1',
        action='store',
        help='Sets what region to run the checks in'
    )
    parser.add_argument(
        '-d',
        '--dryrun',
        dest='dryrun',
        const=True,
        default=False,
        action='store_const',
        help='Whether to actually run the power on/off event'
    )

    args = parser.parse_args()
    console_handler(args.schedule[0], args.action[0], args.regions, args.dryrun)