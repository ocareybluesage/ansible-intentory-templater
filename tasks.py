from invoke import task
from src.ec2_client import Ec2Client, Ec2ClientResponse

@task
def foo(_, env: str):
    ec2_client: Ec2Client = Ec2Client.new()
    response: Ec2ClientResponse = ec2_client.get_instances_by_env(env = env)
