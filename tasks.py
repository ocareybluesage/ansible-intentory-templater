from invoke import task
from src.ec2_client import Ec2Client, Ec2ClientResponse
from src.ssm_client import SsmClient, SsmClientResponse
from src.templater import Templater

@task
def foo(_, env: str, client: str):
    templater: Templater = Templater.new(template_path="templates/inventory.yml.jinja")
    ec2_client: Ec2Client = Ec2Client.new(profile_name="it-devops-bss")
    ssm_client: SsmClient = SsmClient.new(profile_name="it-devops-bss-devops")

    response: Ec2ClientResponse = ec2_client.get_instances_by_env(env = env)
    ssm_response: SsmClientResponse = ssm_client.get_parameter_by_name(f"/secrets/{client}/{env}/database/application-user")
    print(ssm_response)
    
    template_data = {"env": env, "client": client, "instances": response.get_instances()}
    templater.render(template_data=template_data)
