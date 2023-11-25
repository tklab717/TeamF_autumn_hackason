import boto3

REGION = 'ap-northeast-1'

# Function for get_parameters
class SSM:
  def get_parameters(param_key):
      ssm = boto3.client('ssm', region_name=REGION)
      response = ssm.get_parameters(
          Names=[
              param_key,
          ],
          WithDecryption=True
      )
      return response['Parameters'][0]['Value']