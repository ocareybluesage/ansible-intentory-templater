from __future__ import annotations
from typing import Dict, List

from pydantic import BaseModel
from boto3 import Session, client


class SsmClient:

    def __init__(self, client):
        self.client = client

    def get_parameter_by_name(self, name):
        response: Dict[str, str] = self.client.get_parameters(
            Names=[
                f"{name}",
            ],
        )        
        return response

    @staticmethod
    def new(profile_name: str) -> SsmClient:
        session = Session(profile_name=profile_name)
        client = session.client('ssm')    
        ssm_client = SsmClient(client)
        return ssm_client
