from __future__ import annotations
from typing import Dict, List

from pydantic import BaseModel
from boto3 import Session


class SsmClient:

    def __init__(self, ssm_client):
        self.ssm_client = ssm_client

    def get_parameter_by_name(self, names: List[str]) -> SsmClientResponse:
        response: Dict[str, str] = self.ssm_client.get_parameters(
            Names=names,
            WithDecryption=True,
        )
        response: SsmClientResponse = SsmClientResponse(**response)

        return response

    @staticmethod
    def new(profile_name: str) -> SsmClient:
        session = Session(profile_name=profile_name)
        ssm_client = session.client("ssm")

        return SsmClient(ssm_client)


class SsmClientResponse(BaseModel):
    Parameters: List[Parameter]


class Parameter(BaseModel):
    Name: str
    Value: str

    def get_value(self) -> str:
        return self.Value


class RdsCreds(BaseModel):
    hostname: str
    password: str
    username: str

    def get_hostname(self) -> str:
        return self.hostname

    def get_password(self) -> str:
        return self.password
    
    @property
    def env(self) -> str:
        return self.username.split("_")[-1]

    @staticmethod
    def get_parameter_path(client_code: str, env: str):
        return f"/secrets/{client_code}/{env}/database/application-user"
