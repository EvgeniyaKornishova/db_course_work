from pydantic import BaseModel


class CredentialBase(BaseModel):
    login: str


class CredentialIn(CredentialBase):
    password: str


class CredentialOut(CredentialBase):
    user_id: str
    password: str
