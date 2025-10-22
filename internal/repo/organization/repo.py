import json

from .sql_query import *
from internal import interface, model

from pkg.trace_wrapper import traced_method


class OrganizationRepo(interface.IOrganizationRepo):
    def __init__(
            self,
            tel: interface.ITelemetry,
            db: interface.IDB,
    ):
        self.tracer = tel.tracer()
        self.db = db

    @traced_method()
    async def create_organization(self, name: str) -> int:
        args = {
            'name': name,
        }

        organization_id = await self.db.insert(create_organization, args)

        return organization_id

    @traced_method()
    async def get_organization_by_id(self, organization_id: int) -> list[model.Organization]:
        args = {'organization_id': organization_id}
        rows = await self.db.select(get_organization_by_id, args)
        organizations = model.Organization.serialize(rows) if rows else []

        return organizations

    @traced_method()
    async def get_all_organizations(self) -> list[model.Organization]:
        rows = await self.db.select(get_all_organizations, {})
        organizations = model.Organization.serialize(rows) if rows else []

        return organizations

    @traced_method()
    async def update_organization(
            self,
            organization_id: int,
            name: str = None,
            description: str = None,
            tone_of_voice: list[str] = None,
            compliance_rules: list[dict] = None,
            products: list[dict] = None,
            locale: dict = None,
            additional_info: list[dict] = None,
    ) -> None:
        update_fields = []
        args: dict = {'organization_id': organization_id}

        if name is not None:
            update_fields.append("name = :name")
            args['name'] = name

        if name is not None:
            update_fields.append("description = :description")
            args['description'] = description

        if tone_of_voice is not None:
            update_fields.append("tone_of_voice = :tone_of_voice")
            args['tone_of_voice'] = tone_of_voice

        if compliance_rules is not None:
            update_fields.append("compliance_rules = :compliance_rules")
            args['compliance_rules'] = [json.dumps(rule) for rule in compliance_rules]

        if products is not None:
            update_fields.append("products = :products")
            args['products'] = [json.dumps(product) for product in products]

        if locale is not None:
            update_fields.append("locale = :locale")
            args['locale'] = json.dumps(locale)

        if additional_info is not None:
            update_fields.append("additional_info = :additional_info")
            args['additional_info'] = [json.dumps(info) for info in additional_info]

        if not update_fields:
            return

        query = f"""
                UPDATE organizations
                SET {', '.join(update_fields)}
                WHERE id = :organization_id;
                """

        await self.db.update(query, args)

    @traced_method()
    async def delete_organization(self, organization_id: int) -> None:
        args = {'organization_id': organization_id}
        await self.db.update(delete_organization, args)

    @traced_method()
    async def update_balance(self, organization_id: int, rub_balance: str) -> None:
        args = {
            'organization_id': organization_id,
            'rub_balance': str(rub_balance)
        }
        await self.db.update(update_balance, args)

    # Cost Multipliers methods
    @traced_method()
    async def create_cost_multiplier(
            self,
            organization_id: int,
            generate_text_cost_multiplier: float,
            generate_image_cost_multiplier: float,
            generate_vizard_video_cut_cost_multiplier: float,
            transcribe_audio_cost_multiplier: float
    ) -> int:
        args = {
            'organization_id': organization_id,
            'generate_text_cost_multiplier': generate_text_cost_multiplier,
            'generate_image_cost_multiplier': generate_image_cost_multiplier,
            'generate_vizard_video_cut_cost_multiplier': generate_vizard_video_cut_cost_multiplier,
            'transcribe_audio_cost_multiplier': transcribe_audio_cost_multiplier,
        }

        cost_multiplier_id = await self.db.insert(create_cost_multiplier, args)

        return cost_multiplier_id

    @traced_method()
    async def get_cost_multiplier_by_organization_id(self, organization_id: int) -> list[model.CostMultiplier]:
        args = {'organization_id': organization_id}
        rows = await self.db.select(get_cost_multiplier_by_organization_id, args)
        cost_multipliers = model.CostMultiplier.serialize(rows) if rows else []

        return cost_multipliers

    @traced_method()
    async def update_cost_multiplier(
            self,
            organization_id: int,
            generate_text_cost_multiplier: float = None,
            generate_image_cost_multiplier: float = None,
            generate_vizard_video_cut_cost_multiplier: float = None,
            transcribe_audio_cost_multiplier: float = None,
    ) -> None:
        update_fields = []
        args: dict = {'organization_id': organization_id}

        if generate_text_cost_multiplier is not None:
            update_fields.append("generate_text_cost_multiplier = :generate_text_cost_multiplier")
            args['generate_text_cost_multiplier'] = generate_text_cost_multiplier

        if generate_image_cost_multiplier is not None:
            update_fields.append("generate_image_cost_multiplier = :generate_image_cost_multiplier")
            args['generate_image_cost_multiplier'] = generate_image_cost_multiplier

        if generate_vizard_video_cut_cost_multiplier is not None:
            update_fields.append("generate_vizard_video_cut_cost_multiplier = :generate_vizard_video_cut_cost_multiplier")
            args['generate_vizard_video_cut_cost_multiplier'] = generate_vizard_video_cut_cost_multiplier

        if transcribe_audio_cost_multiplier is not None:
            update_fields.append("transcribe_audio_cost_multiplier = :transcribe_audio_cost_multiplier")
            args['transcribe_audio_cost_multiplier'] = transcribe_audio_cost_multiplier

        if not update_fields:
            return

        query = f"""
                UPDATE cost_multipliers
                SET {', '.join(update_fields)}
                WHERE organization_id = :organization_id;
                """

        await self.db.update(query, args)

    @traced_method()
    async def delete_cost_multiplier(self, organization_id: int) -> None:
        args = {'organization_id': organization_id}
        await self.db.update(delete_cost_multiplier, args)
