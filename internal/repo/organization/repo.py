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
            video_cut_description_end_sample: str = None,
            publication_text_end_sample: str = None,
            tone_of_voice: list[str] = None,
            brand_rules: list[str] = None,
            compliance_rules: list[str] = None,
            audience_insights: list[str] = None,
            products: list[dict] = None,
            locale: dict = None,
            additional_info: list[str] = None,
    ) -> None:
        update_fields = []
        args: dict = {'organization_id': organization_id}

        if name is not None:
            update_fields.append("name = :name")
            args['name'] = name

        if video_cut_description_end_sample is not None:
            update_fields.append("video_cut_description_end_sample = :video_cut_description_end_sample")
            args['video_cut_description_end_sample'] = video_cut_description_end_sample

        if publication_text_end_sample is not None:
            update_fields.append("publication_text_end_sample = :publication_text_end_sample")
            args['publication_text_end_sample'] = publication_text_end_sample

        if tone_of_voice is not None:
            update_fields.append("tone_of_voice = :tone_of_voice")
            args['tone_of_voice'] = tone_of_voice

        if brand_rules is not None:
            update_fields.append("brand_rules = :brand_rules")
            args['brand_rules'] = brand_rules

        if compliance_rules is not None:
            update_fields.append("compliance_rules = :compliance_rules")
            args['compliance_rules'] = compliance_rules

        if audience_insights is not None:
            update_fields.append("audience_insights = :audience_insights")
            args['audience_insights'] = audience_insights

        if products is not None:
            update_fields.append("products = :products")
            args['products'] = [json.dumps(product) for product in products]

        if locale is not None:
            update_fields.append("locale = :locale")
            args['locale'] = json.dumps(locale)

        if additional_info is not None:
            update_fields.append("additional_info = :additional_info")
            args['additional_info'] = additional_info

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
