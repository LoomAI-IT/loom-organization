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
    video_cut_description_end_sample: Optional[str] = None
    publication_text_end_sample: Optional[str] = None
    tone_of_voice: Optional[list[str]] = None
    brand_rules: Optional[list[str]] = None
    compliance_rules: Optional[list[str]] = None
    audience_insights: Optional[list[str]] = None
    products: Optional[list[dict]] = None
    locale: Optional[dict] = None
    additional_info: Optional[list[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "organization_id": 1,
                "name": "Updated Organization Name",
                "video_cut_description_end_sample": "Sample video description ending",
                "publication_text_end_sample": "Sample publication text ending",
                "tone_of_voice": ["professional", "friendly"],
                "brand_rules": ["Use consistent branding"],
                "compliance_rules": ["Follow GDPR"],
                "audience_insights": ["Target age 25-45"],
                "products": [{"name": "Product A", "price": 100}],
                "locale": {"language": "ru", "country": "RU"},
                "additional_info": ["Extra information"]
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