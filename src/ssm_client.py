from __future__ import annotations
from typing import Dict, List

from pydantic import BaseModel
from boto3 import Session


class SsmClient:

    def __init__(self, ssm_client):
        self.ssm_client = ssm_client

    def get_parameter_by_name(self, name):
        response: Dict[str, str] = self.ssm_client.get_parameters(
            Names=[
                f"{name}",
            ],
        )        
        response: SsmClientResponse = SsmClientResponse(**response)

        [parameter for parameter in response.Parameters if parameter.is_secure_string()]
        
        return response

    @staticmethod
    def new(profile_name: str) -> SsmClient:
        session = Session(profile_name=profile_name)
        ssm_client = session.client('ssm')    

        return SsmClient(ssm_client)

class SsmClientResponse(BaseModel):
    Parameters: List[Parameter]

class Parameter(BaseModel):
    Name: str
    Type: str
    Value: str

    def is_secure_string(self) -> bool:
        return self.Type == "SecureString"
