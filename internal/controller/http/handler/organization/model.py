from decimal import Decimal

from pydantic import BaseModel
from typing import Optional


class CreateOrganizationBody(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Organization",
            }
        }


class UpdateOrganizationBody(BaseModel):
    organization_id: int
    name: Optional[str] = None
    autoposting_moderation: Optional[bool] = None
    video_cut_description_end_sample: Optional[str] = None
    publication_text_end_sample: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "organization_id": 1,
                "name": "Updated Organization Name",
                "autoposting_moderation": False,
                "video_cut_description_end_sample": "Sample video description ending",
                "publication_text_end_sample": "Sample publication text ending"
            }
        }

class TopUpBalanceBody(BaseModel):
    organization_id: int
    amount_rub: str
    interserver_secret_key: str

class DebitBalanceBody(BaseModel):
    organization_id: int
    interserver_secret_key: str
    amount_rub: str

    class Config:
        json_schema_extra = {
            "example": {
                "organization_id": 1,
                "amount_rub": "100.50",  # Пример как строка
                "interserver_secret_key": "secret"
            }
        }

# Response models
class CreateOrganizationResponse(BaseModel):
    message: str
    organization_id: int


class GetOrganizationResponse(BaseModel):
    message: str
    organization: dict


class GetAllOrganizationsResponse(BaseModel):
    message: str
    organizations: list[dict]


class UpdateOrganizationResponse(BaseModel):
    message: str


class DeleteOrganizationResponse(BaseModel):
    message: str