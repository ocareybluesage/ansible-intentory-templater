from typing import List
from invoke import task
from src import Config
from src.ec2_client import Ec2Client, Ec2ClientResponse, Instance
from src.ssm_client import SsmClient, SsmClientResponse, RdsCreds
from src.templater import Templater
from src.inventory_group import update_inventory_group


@task
def template(
    _,
    envs: str,
    client_code: str,
    client_aws_profile: str = "it-devops-bss",
    bss_devops_aws_profile: str = "it-devops-bss-devops",
    ssh_private_key_file_path: str = "../BlueSage-Terraform/bss-terraform-infrastructure/bss-lower.pem",
):
    """
    Templates out ansible inventory yaml configuration file

    Args:
        envs: A comma delinatied list of environments. Cannot include spaces. Ex: dev,qa,uat,foo,bar
        client_code: client code corresponding to client infrasture you want to configure using ansible
        client_aws_profile: name of aws profile that points to aws client account 
        bss_devops_aws_profile: name of aws profile that points to aws bss-devops account 
        ssh_private_key_file_path: file path to .pem keys which can be used to ssh into the host ec2 instances
    """
    config = Config.new(environments=envs)
    environments = config.get_environments()

    ec2_client: Ec2Client = Ec2Client.new(profile_name=client_aws_profile)
    ssm_client: SsmClient = SsmClient.new(profile_name=bss_devops_aws_profile)

    ec2_response: Ec2ClientResponse = ec2_client.get_instances_by_environment(
        environments=environments
    )

    parameter_names = [
        RdsCreds.get_parameter_path(client_code=client_code, env=env)
        for env in environments
    ]
    ssm_response: SsmClientResponse = ssm_client.get_parameter_by_name(
        names=parameter_names
    )

    rds_creds: List[RdsCreds] = [
        RdsCreds.model_validate_json(parameter.get_value())
        for parameter in ssm_response.Parameters
    ]
    instances: List[Instance] = ec2_response.get_instances()

    template_data = {
        "envs": environments,
        "client_code": client_code,
        "instances": instances,
        "rds_creds": rds_creds,
        "client_aws_profile": client_aws_profile,
        "ssh_private_key_file_path": ssh_private_key_file_path,
    }

    templater: Templater = Templater.new(config=config)
    rendered_template = templater.render(template_data=template_data)
    templater.write_template(
        rendered_template=rendered_template, client_code=client_code
    )

    update_inventory_group(config=config, client_code=client_code)
