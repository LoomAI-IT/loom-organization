from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal  # Добавляем импорт
from typing import List, Optional


@dataclass
class Organization:
    id: int
    name: str
    rub_balance: Decimal  # Изменено с int на Decimal
    autoposting_moderation: bool
    video_cut_description_end_sample: str
    publication_text_end_sample: str
    created_at: datetime

    @classmethod
    def serialize(cls, rows) -> List['Organization']:
        return [
            cls(
                id=row.id,
                name=row.name,
                rub_balance=Decimal(str(row.rub_balance)),  # Конвертируем в Decimal
                autoposting_moderation=row.autoposting_moderation,
                video_cut_description_end_sample=row.video_cut_description_end_sample,
                publication_text_end_sample=row.publication_text_end_sample,
                created_at=row.created_at
            )
            for row in rows
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "rub_balance": float(self.rub_balance),  # Конвертируем в float для JSON
            "autoposting_moderation": self.autoposting_moderation,
            "video_cut_description_end_sample": self.video_cut_description_end_sample,
            "publication_text_end_sample": self.publication_text_end_sample,
            "created_at": self.created_at.isoformat()
        }