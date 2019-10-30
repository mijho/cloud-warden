# Cloud Warden

*WIP*

A python utility that does the rounds around AWS compute resources shutting down and switching on resources according
to schedules.

```
optional arguments:
  -h, --help                                        show this help message and exit
  -s --schedule 
        {OfficeHours,ExtendedHours,
        DailyOnDemand,WeeklyOnDemand}               Set which tag value to target
  -a --action {on,off}                              Set whether to power off or on the tagged instances
  -r {aws-region}                                   Sets what region to run the checks in
  -d, --dryrun                                      Whether to actually run the power on/off event
```

### AWS Regions

The following regions can be specified to run against:

```
'us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-east-1', 'ap-south-1', 'ap-northeast-1',
'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'cn-north-1',
'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north01', 'me-south-1',
'sa-east-1', 'us-gov-east-1', 'us-gov-west-1'
```

### Environment Variables

The following Environment Variables can be set:
```
WEBHOOK_URL = `url to send push notifications to`
SAWMILL_DEVELOPER_LOGS = `true/false`
