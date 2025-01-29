from __future__ import annotations
from typing import Dict, List

from pydantic import BaseModel
from boto3 import Session


class SsmClient:

    def __init__(self, ssm_client):
        self.ssm_client = ssm_client

    def get_parameter_by_name(self, name: str, model: BaseModel) -> BaseModel:
        response: Dict[str, str] = self.ssm_client.get_parameter(
            Name=f"{name}", WithDecryption=True
        )

        response: SsmClientResponse = SsmClientResponse(**response)
        response = model.model_validate_json(response.Parameter.get_value())

        return response

    @staticmethod
    def new(profile_name: str) -> SsmClient:
        session = Session(profile_name=profile_name)
        ssm_client = session.client("ssm")

        return SsmClient(ssm_client)


class SsmClientResponse(BaseModel):
    Parameter: Parameter

class Parameter(BaseModel):
    Name: str
    Value: str

    def get_value(self) -> str:
        return self.Value

class RdsCreds(BaseModel):
    hostname: str
    password: str

    def get_hostname(self) -> str:
        return self.hostname
    
    def get_password(self) -> str:
        return self.password
