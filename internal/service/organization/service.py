from decimal import Decimal

from opentelemetry.trace import Status, StatusCode, SpanKind

from internal import interface, model, common


class OrganizationService(interface.IOrganizationService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            organization_repo: interface.IOrganizationRepo,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.organization_repo = organization_repo

    async def create_organization(self, name: str) -> int:
        with self.tracer.start_as_current_span(
                "OrganizationService.create_organization",
                kind=SpanKind.INTERNAL,
                attributes={"org_name": name}
        ) as span:
            try:
                organization_id = await self.organization_repo.create_organization(
                    name=name
                )

                span.set_status(StatusCode.OK)
                return organization_id

            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def get_organization_by_id(self, organization_id: int) -> model.Organization:
        with self.tracer.start_as_current_span(
                "OrganizationService.get_organization_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                organizations = await self.organization_repo.get_organization_by_id(organization_id)
                if not organizations:
                    self.logger.warning("Организация не найдена")
                    raise common.ErrOrganizationNotFound()

                organization = organizations[0]

                span.set_status(StatusCode.OK)
                return organization

            except Exception as e:
                self.logger.error("Ошибка при получении организации по ID")
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def get_all_organizations(self) -> list[model.Organization]:
        with self.tracer.start_as_current_span(
                "OrganizationService.get_all_organizations",
                kind=SpanKind.INTERNAL
        ) as span:
            try:
                organizations = await self.organization_repo.get_all_organizations()

                span.set_status(StatusCode.OK)
                return organizations

            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                raise

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
        with self.tracer.start_as_current_span(
                "OrganizationService.update_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                # Проверяем, что организация существует
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

                span.set_status(StatusCode.OK)

            except Exception as e:

                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def delete_organization(self, organization_id: int) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationService.delete_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                # Проверяем, что организация существует
                organizations = await self.organization_repo.get_organization_by_id(organization_id)
                if not organizations:
                    self.logger.warning("Организация не найдена")
                    raise common.ErrOrganizationNotFound()

                await self.organization_repo.delete_organization(organization_id)

                span.set_status(StatusCode.OK)

            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def top_up_balance(self, organization_id: int, amount_rub: Decimal) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationService.top_up_balance",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                }
        ) as span:
            try:
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

                span.set_status(StatusCode.OK)

            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def debit_balance(self, organization_id: int, amount_rub: Decimal) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationService.debit_balance",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                }
        ) as span:
            try:
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

                span.set_status(StatusCode.OK)

            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                raise