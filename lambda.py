import json
import boto3

# Initialize the EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Extract relevant details from the GuardDuty finding
    finding = event['detail']
    instance_id = finding['resource']['instanceDetails']['instanceId']
    action_type = finding['service']['action']['actionType']
    severity = finding['severity']
    
    # Log the incoming finding for debugging purposes
    print(f"Received GuardDuty finding for instance {instance_id} with action type {action_type} and severity {severity}")

    # Check if the finding suggests unauthorized access
    if action_type == 'UNAUTHORIZED_ACCESS':
        try:
            # Remove all security groups from the instance to isolate it
            response = ec2.modify_instance_attribute(
                InstanceId=instance_id,
                Groups=["sg-0206b5f6858610c58"]
            )
            
            # Log successful isolation
            print(f"Successfully isolated instance {instance_id} due to unauthorized access.")
            
            # Optionally, you could add an SNS notification or another action here
            
        except Exception as e:
            # Log any errors that occur
            print(f"Failed to isolate instance {instance_id}. Error: {str(e)}")
            raise e
        
    else:
        print(f"Action type {action_type} is not set up for automated response.")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Instance {instance_id} processed for action type {action_type}.")
    }
