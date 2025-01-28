from invoke import task
from src.ec2_client import Ec2Client, Ec2ClientResponse
from src.templater import Templater

@task
def foo(_, env: str, client: str):
    templater = Templater.new(template_path="templates/inventory.yml.jinja")
    ec2_client: Ec2Client = Ec2Client.new()

    response: Ec2ClientResponse = ec2_client.get_instances_by_env(env = env)
    template_data = {"env": env, "client": client, "instances": response.get_instances()}
    templater.render(template_data=template_data)
