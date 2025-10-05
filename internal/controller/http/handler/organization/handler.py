from decimal import Decimal

from opentelemetry.trace import Status, StatusCode, SpanKind
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.organization.model import (
    CreateOrganizationBody, UpdateOrganizationBody,
    TopUpBalanceBody, DebitBalanceBody
)


class OrganizationController(interface.IOrganizationController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            organization_service: interface.IOrganizationService,
            interserver_secret_key: str,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.organization_service = organization_service
        self.interserver_secret_key = interserver_secret_key

    async def create_organization(self, body: CreateOrganizationBody) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.create_organization",
                kind=SpanKind.INTERNAL,
                attributes={"org_name": body.name}
        ) as span:
            try:

                self.logger.info("Начало создания организации")

                organization_id = await self.organization_service.create_organization(
                    name=body.name,
                )

                self.logger.info("Организация успешно создана")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=201,
                    content={
                        "organization_id": organization_id
                    }
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def get_organization_by_id(self, request: Request, organization_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.get_organization_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:

                self.logger.info("Начало получения организации по ID")

                organization = await self.organization_service.get_organization_by_id(organization_id)

                self.logger.info("Организация успешно получена")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=200,
                    content=organization.to_dict()
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err


    async def get_all_organizations(self) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.get_all_organizations",
                kind=SpanKind.INTERNAL
        ) as span:
            try:

                self.logger.info("Начало получения всех организаций")

                organizations = await self.organization_service.get_all_organizations()

                self.logger.info("Все организации успешно получены")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=200,
                    content={
                        "organizations": [org.to_dict() for org in organizations]
                    }
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def update_organization(self, request: Request, body: UpdateOrganizationBody) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.update_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": body.organization_id}
        ) as span:
            try:

                self.logger.info("Начало обновления организации")

                await self.organization_service.update_organization(
                    organization_id=body.organization_id,
                    name=body.name,
                    video_cut_description_end_sample=body.video_cut_description_end_sample,
                    publication_text_end_sample=body.publication_text_end_sample,
                    tone_of_voice=body.tone_of_voice,
                    brand_rules=body.brand_rules,
                    compliance_rules=body.compliance_rules,
                    audience_insights=body.audience_insights,
                    products=body.products,
                    locale=body.locale,
                    additional_info=body.additional_info
                )

                self.logger.info("Организация успешно обновлена")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=200,
                    content={}
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def delete_organization(self, organization_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.delete_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:

                self.logger.info("Начало удаления организации")

                await self.organization_service.delete_organization(organization_id)

                self.logger.info("Организация успешно удалена")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=200,
                    content={"message": "Organization deleted successfully"}
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def top_up_balance(self, body: TopUpBalanceBody) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.top_up_balance",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": body.organization_id,
                    "amount_rub": body.amount_rub
                }
        ) as span:
            try:
                # Проверка межсервисного ключа
                if body.interserver_secret_key != self.interserver_secret_key:
                    self.logger.warning("Неверный межсервисный ключ для пополнения баланса")
                    raise HTTPException(status_code=403, detail="Invalid interserver secret key")

                self.logger.info("Начало пополнения баланса")

                await self.organization_service.top_up_balance(
                    organization_id=body.organization_id,
                    amount_rub=Decimal(body.amount_rub)
                )

                self.logger.info("Баланс успешно пополнен")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=200,
                    content={
                        "organization_id": body.organization_id,
                        "amount_rub": body.amount_rub
                    }
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err

    async def debit_balance(self, body: DebitBalanceBody) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.debit_balance",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": body.organization_id,
                    "amount_rub": body.amount_rub
                }
        ) as span:
            try:
                # Проверка межсервисного ключа
                if body.interserver_secret_key != self.interserver_secret_key:
                    self.logger.warning("Неверный межсервисный ключ для списания баланса")
                    raise HTTPException(status_code=403, detail="Invalid interserver secret key")

                self.logger.info("Начало списания баланса")

                await self.organization_service.debit_balance(
                    organization_id=body.organization_id,
                    amount_rub=Decimal(body.amount_rub)
                )

                self.logger.info("Баланс успешно списан")

                span.set_status(StatusCode.OK)
                return JSONResponse(
                    status_code=200,
                    content={
                        "organization_id": body.organization_id,
                        "amount_rub": body.amount_rub
                    }
                )

            except Exception as err:
                
                span.set_status(StatusCode.ERROR, str(err))
                raise err