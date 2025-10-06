from decimal import Decimal

from internal import interface, model, common

from pkg.trace_wrapper import traced_method


class OrganizationService(interface.IOrganizationService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            organization_repo: interface.IOrganizationRepo,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.organization_repo = organization_repo

    @traced_method()
    async def create_organization(self, name: str) -> int:
        organization_id = await self.organization_repo.create_organization(
            name=name
        )
        return organization_id

    @traced_method()
    async def get_organization_by_id(self, organization_id: int) -> model.Organization:
        organizations = await self.organization_repo.get_organization_by_id(organization_id)
        if not organizations:
            self.logger.warning("Организация не найдена")
            raise common.ErrOrganizationNotFound()

        organization = organizations[0]
        return organization

    @traced_method()
    async def get_all_organizations(self) -> list[model.Organization]:
        organizations = await self.organization_repo.get_all_organizations()
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
        organizations = await self.organization_repo.get_organization_by_id(organization_id)
        if not organizations:
            self.logger.warning("Организация не найдена")
            raise common.ErrOrganizationNotFound()

        await self.organization_repo.update_organization(
            organization_id=organization_id,
            name=name,
            video_cut_description_end_sample=video_cut_description_end_sample,
            publication_text_end_sample=publication_text_end_sample,
            tone_of_voice=tone_of_voice,
            brand_rules=brand_rules,
            compliance_rules=compliance_rules,
            audience_insights=audience_insights,
            products=products,
            locale=locale,
            additional_info=additional_info
        )

    @traced_method()
    async def delete_organization(self, organization_id: int) -> None:
        organizations = await self.organization_repo.get_organization_by_id(organization_id)
        if not organizations:
            self.logger.warning("Организация не найдена")
            raise common.ErrOrganizationNotFound()

        await self.organization_repo.delete_organization(organization_id)

    @traced_method()
    async def top_up_balance(self, organization_id: int, amount_rub: Decimal) -> None:
        # Проверяем, что организация существует
        organizations = await self.organization_repo.get_organization_by_id(organization_id)
        if not organizations:
            self.logger.warning("Организация не найдена")
            raise common.ErrOrganizationNotFound()

        organization = organizations[0]

        rub_balance = organization.rub_balance + amount_rub

        await self.organization_repo.update_balance(
            organization_id=organization_id,
            rub_balance=str(rub_balance)
        )

    @traced_method()
    async def debit_balance(self, organization_id: int, amount_rub: Decimal) -> None:
        # Проверяем, что организация существует
        organizations = await self.organization_repo.get_organization_by_id(organization_id)
        if not organizations:
            self.logger.warning("Организация не найдена")
            raise common.ErrOrganizationNotFound()

        organization = organizations[0]

        rub_balance = organization.rub_balance - amount_rub

        # # Проверяем, что у организации достаточно средств
        # current_balance = organizations[0].rub_balance
        # if current_balance < amount_rub:
        #     raise common.ErrInsufficientBalance()

        await self.organization_repo.update_balance(
            organization_id=organization_id,
            rub_balance=str(rub_balance)
        )
