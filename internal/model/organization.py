from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Organization:
    id: int
    name: str
    rub_balance: Decimal

    tone_of_voice: list[str]
    brand_rules: list[str]
    compliance_rules: list[str]
    additional_info: list[dict]

    products: list[dict]
    locale: dict
    created_at: datetime

    @classmethod
    def serialize(cls, rows) -> list['Organization']:
        return [
            cls(
                id=row.id,
                name=row.name,
                rub_balance=Decimal(str(row.rub_balance)),
                tone_of_voice=row.tone_of_voice,
                brand_rules=row.brand_rules,
                compliance_rules=row.compliance_rules,
                additional_info=row.additional_info,
                products=row.products,
                locale=row.locale,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "rub_balance": str(self.rub_balance),
            "tone_of_voice": self.tone_of_voice,
            "brand_rules": self.brand_rules,
            "compliance_rules": self.compliance_rules,
            "additional_info": self.additional_info,
            "products": self.products,
            "locale": self.locale,
            "created_at": self.created_at,
        }


@dataclass
class CostMultiplier:
    id: int
    organization_id: int
    generate_text_cost_multiplier: float
    generate_image_cost_multiplier: float
    generate_vizard_video_cut_cost_multiplier: float
    transcribe_audio_cost_multiplier: float
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
                transcribe_audio_cost_multiplier=float(row.transcribe_audio_cost_multiplier),
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
            "transcribe_audio_cost_multiplier": self.transcribe_audio_cost_multiplier,
            "created_at": self.created_at.isoformat()
        }
