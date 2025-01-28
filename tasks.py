from invoke import task
from src.ec2_client import Ec2Client

@task
def foo(_):
    ec2_client: Ec2Client = Ec2Client.new()
    ec2_client.get_instances_by_env(env = "dev")