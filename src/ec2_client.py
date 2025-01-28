from __future__ import annotations
from typing import Dict, List

from pydantic import BaseModel
import boto3


class Ec2Client:
    def __init__(self, client):
        self.client = client

    def get_instances_by_env(self, env):
        response: Dict[str, str] = self.client.describe_instances(
            Filters=[
                {
                    "Name": "tag:Env",
                    "Values": [
                        f"{env}",
                    ],
                },
            ],
        )
        response = Ec2ClientResponse(**response)
        print(f"{response}")

    @staticmethod
    def new() -> Ec2Client:
        client = boto3.client("ec2")
        ec2_client = Ec2Client(client)
        return ec2_client


class Ec2ClientResponse(BaseModel):
    Reservations: List[Reservation]

class Reservation(BaseModel):
    Instances: List[Instance]

class Instance(BaseModel):
    PrivateIpAddress: str
    Tags: List[Dict[str, str]]