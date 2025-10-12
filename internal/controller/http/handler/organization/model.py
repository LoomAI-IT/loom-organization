from pydantic import BaseModel


class CreateOrganizationBody(BaseModel):
    name: str


class UpdateOrganizationBody(BaseModel):
    organization_id: int
    name: str = None
    tone_of_voice: list[str] = None
    brand_rules: list[str] = None
    compliance_rules: list[str] = None
    products: list[dict] = None
    locale: dict = None
    additional_info: list[dict] = None


class TopUpBalanceBody(BaseModel):
    organization_id: int
    amount_rub: str
    interserver_secret_key: str


class DebitBalanceBody(BaseModel):
    organization_id: int
    interserver_secret_key: str
    amount_rub: str


# Response models
class CreateOrganizationResponse(BaseModel):
    organization_id: int


class GetOrganizationResponse(BaseModel):
    organization: dict


class GetAllOrganizationsResponse(BaseModel):
    organizations: list[dict]


# Cost Multiplier models
class UpdateCostMultiplierBody(BaseModel):
    organization_id: int
    generate_text_cost_multiplier: float = None
    generate_image_cost_multiplier: float = None
    generate_vizard_video_cut_cost_multiplier: float = None
    transcribe_audio_cost_multiplier: float = None
