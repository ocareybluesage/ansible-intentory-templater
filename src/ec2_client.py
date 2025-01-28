from __future__ import annotations
import boto3


class Ec2Client:
    def __init__(self, client):
        self.client = client

    def get_instances_by_env(self, env):
        foo = self.client.describe_instances(
            Filters=[
                {
                    "Name": "tag:Env",
                    "Values": [
                        f"{env}",
                    ],
                },
            ],
        )

        print(f"{foo}")

    @staticmethod
    def new() -> Ec2Client:
        client = boto3.client("ec2")
        ec2_client = Ec2Client(client)
        return ec2_client
