from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Organization:
    id: int
    name: str
    rub_balance: Decimal
    video_cut_description_end_sample: str
    publication_text_end_sample: str
    tone_of_voice: list[str]
    brand_rules: list[str]
    compliance_rules: list[str]
    audience_insights: list[str]
    products: list[dict]
    locale: dict
    additional_info: list[str]
    created_at: datetime

    @classmethod
    def serialize(cls, rows) -> list['Organization']:
        return [
            cls(
                id=row.id,
                name=row.name,
                rub_balance=Decimal(str(row.rub_balance)),
                video_cut_description_end_sample=row.video_cut_description_end_sample,
                publication_text_end_sample=row.publication_text_end_sample,
                tone_of_voice=row.tone_of_voice or [],
                brand_rules=row.brand_rules or [],
                compliance_rules=row.compliance_rules or [],
                audience_insights=row.audience_insights or [],
                products=row.products or [],
                locale=row.locale or {},
                additional_info=row.additional_info or [],
                created_at=row.created_at
            )
            for row in rows
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "rub_balance": str(self.rub_balance),
            "video_cut_description_end_sample": self.video_cut_description_end_sample,
            "publication_text_end_sample": self.publication_text_end_sample,
            "tone_of_voice": self.tone_of_voice,
            "brand_rules": self.brand_rules,
            "compliance_rules": self.compliance_rules,
            "audience_insights": self.audience_insights,
            "products": self.products,
            "locale": self.locale,
            "additional_info": self.additional_info,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class CostMultiplier:
    id: int
    organization_id: int
    generate_text_cost_multiplier: float
    generate_image_cost_multiplier: float
    generate_vizard_video_cut_cost_multiplier: float
    created_at: datetime

    @classmethod
    def serialize(cls, rows) -> list['CostMultiplier']:
        return [
            cls(
                id=row.id,
                organization_id=row.organization_id,
                generate_text_cost_multiplier=float(row.generate_text_cost_multiplier),
                generate_image_cost_multiplier=float(row.generate_image_cost_multiplier),
                generate_vizard_video_cut_cost_multiplier=float(row.generate_vizard_video_cut_cost_multiplier),
                created_at=row.created_at
            )
            for row in rows
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "generate_text_cost_multiplier": self.generate_text_cost_multiplier,
            "generate_image_cost_multiplier": self.generate_image_cost_multiplier,
            "generate_vizard_video_cut_cost_multiplier": self.generate_vizard_video_cut_cost_multiplier,
            "created_at": self.created_at.isoformat()
        }
