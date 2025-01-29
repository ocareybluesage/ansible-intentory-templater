from invoke import task
from src.ec2_client import Ec2Client, Ec2ClientResponse
from src.ssm_client import SsmClient, SsmClientResponse, RdsCreds
from src.templater import Templater

@task
def foo(_, env: str, client: str):
    templater: Templater = Templater.new(template_path="templates/inventory.yml.jinja")
    ec2_client: Ec2Client = Ec2Client.new(profile_name="it-devops-bss")
    ssm_client: SsmClient = SsmClient.new(profile_name="it-devops-bss-devops")

    ec2_response: Ec2ClientResponse = ec2_client.get_instances_by_env(env = env)
    rds_creds: RdsCreds = ssm_client.get_parameter_by_name(name=f"/secrets/{client}/{env}/database/application-user", model=RdsCreds)
    
    template_data = {"env": env, "client": client, "instances": ec2_response.get_instances(), "rds_creds": rds_creds}
    templater.render(template_data=template_data)
