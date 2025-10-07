from decimal import Decimal

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.organization.model import (
    CreateOrganizationBody, UpdateOrganizationBody,
    TopUpBalanceBody, DebitBalanceBody
)
from pkg.log_wrapper import auto_log

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

    @auto_log()
    @traced_method()
    async def create_organization(self, body: CreateOrganizationBody) -> JSONResponse:
        organization_id = await self.organization_service.create_organization(
            name=body.name,
        )
        return JSONResponse(
            status_code=201,
            content={
                "organization_id": organization_id
            }
        )

    @auto_log()
    @traced_method()
    async def get_organization_by_id(self, request: Request, organization_id: int) -> JSONResponse:
        organization = await self.organization_service.get_organization_by_id(organization_id)
        return JSONResponse(
            status_code=200,
            content=organization.to_dict()
        )

    @auto_log()
    @traced_method()
    async def get_all_organizations(self) -> JSONResponse:
        organizations = await self.organization_service.get_all_organizations()
        return JSONResponse(
            status_code=200,
            content={
                "organizations": [org.to_dict() for org in organizations]
            }
        )

    @auto_log()
    @traced_method()
    async def update_organization(self, request: Request, body: UpdateOrganizationBody) -> JSONResponse:
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

        return JSONResponse(
            status_code=200,
            content={}
        )

    @auto_log()
    @traced_method()
    async def delete_organization(self, organization_id: int) -> JSONResponse:
        await self.organization_service.delete_organization(organization_id)
        return JSONResponse(
            status_code=200,
            content={"message": "Organization deleted successfully"}
        )

    @auto_log()
    @traced_method()
    async def top_up_balance(self, body: TopUpBalanceBody) -> JSONResponse:
        if body.interserver_secret_key != self.interserver_secret_key:
            self.logger.warning("Неверный межсервисный ключ для пополнения баланса")
            raise HTTPException(status_code=403, detail="Invalid interserver secret key")

        await self.organization_service.top_up_balance(
            organization_id=body.organization_id,
            amount_rub=Decimal(body.amount_rub)
        )
        return JSONResponse(
            status_code=200,
            content={
                "organization_id": body.organization_id,
                "amount_rub": body.amount_rub
            }
        )

    @auto_log()
    @traced_method()
    async def debit_balance(self, body: DebitBalanceBody) -> JSONResponse:
        if body.interserver_secret_key != self.interserver_secret_key:
            self.logger.warning("Неверный межсервисный ключ для списания баланса")
            raise HTTPException(status_code=403, detail="Invalid interserver secret key")

        await self.organization_service.debit_balance(
            organization_id=body.organization_id,
            amount_rub=Decimal(body.amount_rub)
        )

        return JSONResponse(
            status_code=200,
            content={
                "organization_id": body.organization_id,
                "amount_rub": body.amount_rub
            }
        )
