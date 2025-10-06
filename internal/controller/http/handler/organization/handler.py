from decimal import Decimal

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.organization.model import (
    CreateOrganizationBody, UpdateOrganizationBody,
    TopUpBalanceBody, DebitBalanceBody
)

from pkg.trace_wrapper import traced_method


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

    @traced_method()
    async def create_organization(self, body: CreateOrganizationBody) -> JSONResponse:
        self.logger.info("Начало создания организации")

        organization_id = await self.organization_service.create_organization(
            name=body.name,
        )

        self.logger.info("Организация успешно создана")
        return JSONResponse(
            status_code=201,
            content={
                "organization_id": organization_id
            }
        )

    @traced_method()
    async def get_organization_by_id(self, request: Request, organization_id: int) -> JSONResponse:
        self.logger.info("Начало получения организации по ID")

        organization = await self.organization_service.get_organization_by_id(organization_id)

        self.logger.info("Организация успешно получена")
        return JSONResponse(
            status_code=200,
            content=organization.to_dict()
        )

    @traced_method()
    async def get_all_organizations(self) -> JSONResponse:
        self.logger.info("Начало получения всех организаций")

        organizations = await self.organization_service.get_all_organizations()

        self.logger.info("Все организации успешно получены")
        return JSONResponse(
            status_code=200,
            content={
                "organizations": [org.to_dict() for org in organizations]
            }
        )

    @traced_method()
    async def update_organization(self, request: Request, body: UpdateOrganizationBody) -> JSONResponse:
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
        return JSONResponse(
            status_code=200,
            content={}
        )

    @traced_method()
    async def delete_organization(self, organization_id: int) -> JSONResponse:
        self.logger.info("Начало удаления организации")

        await self.organization_service.delete_organization(organization_id)

        self.logger.info("Организация успешно удалена")
        return JSONResponse(
            status_code=200,
            content={"message": "Organization deleted successfully"}
        )

    @traced_method()
    async def top_up_balance(self, body: TopUpBalanceBody) -> JSONResponse:
        if body.interserver_secret_key != self.interserver_secret_key:
            self.logger.warning("Неверный межсервисный ключ для пополнения баланса")
            raise HTTPException(status_code=403, detail="Invalid interserver secret key")

        self.logger.info("Начало пополнения баланса")

        await self.organization_service.top_up_balance(
            organization_id=body.organization_id,
            amount_rub=Decimal(body.amount_rub)
        )

        self.logger.info("Баланс успешно пополнен")
        return JSONResponse(
            status_code=200,
            content={
                "organization_id": body.organization_id,
                "amount_rub": body.amount_rub
            }
        )

    @traced_method()
    async def debit_balance(self, body: DebitBalanceBody) -> JSONResponse:
        if body.interserver_secret_key != self.interserver_secret_key:
            self.logger.warning("Неверный межсервисный ключ для списания баланса")
            raise HTTPException(status_code=403, detail="Invalid interserver secret key")

        self.logger.info("Начало списания баланса")

        await self.organization_service.debit_balance(
            organization_id=body.organization_id,
            amount_rub=Decimal(body.amount_rub)
        )

        self.logger.info("Баланс успешно списан")

        return JSONResponse(
            status_code=200,
            content={
                "organization_id": body.organization_id,
                "amount_rub": body.amount_rub
            }
        )
