from typing import List
from invoke import task
from src.ec2_client import Ec2Client, Ec2ClientResponse, Instance
from src.ssm_client import SsmClient, SsmClientResponse, RdsCreds
from src.templater import Templater


# envs is comma deliniated list of environments
@task
def foo(
    _,
    envs: str,
    client: str,
    output_file_path: str = "inventory/foo.yml",
    client_aws_profile: str = "it-devops-bss",
    bss_devops_aws_profile: str = "it-devops-bss-devops",
    ssh_private_key_file_path: str = "../BlueSage-Terraform/bss-terraform-infrastructure/bss-lower.pem"
):
    envs = envs.split(",")
    ec2_client: Ec2Client = Ec2Client.new(profile_name=client_aws_profile)
    ssm_client: SsmClient = SsmClient.new(profile_name=bss_devops_aws_profile)

    ec2_response: Ec2ClientResponse = ec2_client.get_instances_by_env(envs=envs)

    parameter_names = [
        RdsCreds.get_parameter_path(client=client, env=env) for env in envs
    ]
    ssm_response: SsmClientResponse = ssm_client.get_parameter_by_name(
        names=parameter_names
    )

    rds_creds: List[RdsCreds] = [
        RdsCreds.model_validate_json(parameter.get_value())
        for parameter in ssm_response.Parameters
    ]
    instances: List[Instance] = ec2_response.get_instances()

    templater: Templater = Templater.new(template_path="templates/inventory.yml.jinja")
    template_data = {
        "envs": envs,
        "client": client,
        "instances": instances,
        "rds_creds": rds_creds,
        "client_aws_profile": client_aws_profile,
        "ssh_private_key_file_path": ssh_private_key_file_path
    }

    rendered_template = templater.render(template_data=template_data)
    templater.write_template(rendered_template=rendered_template, output_file_path=output_file_path)
