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

                self.logger.info("Create organization request", {
                    "org_name": body.name
                })

                organization_id = await self.organization_service.create_organization(
                    name=body.name,
                )

                self.logger.info("Organization created successfully", {
                    "organization_id": organization_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=201,
                    content={
                        "message": "Organization created successfully",
                        "organization_id": organization_id
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def get_organization_by_id(self, request: Request, organization_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.get_organization_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:

                self.logger.info("Get organization by ID request", {
                    "organization_id": organization_id
                })

                organization = await self.organization_service.get_organization_by_id(organization_id)

                self.logger.info("Organization retrieved successfully", {
                    "organization_id": organization_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content=organization.to_dict()
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err


    async def get_all_organizations(self) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.get_all_organizations",
                kind=SpanKind.INTERNAL
        ) as span:
            try:

                self.logger.info("Get all organizations request")

                organizations = await self.organization_service.get_all_organizations()

                self.logger.info("All organizations retrieved successfully", {
                    "count": len(organizations)
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Organizations retrieved successfully",
                        "organizations": [org.to_dict() for org in organizations]
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def update_organization(self, request: Request, body: UpdateOrganizationBody) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.update_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": body.organization_id}
        ) as span:
            try:

                self.logger.info("Update organization request", {
                })

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

                self.logger.info("Organization updated successfully", {
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={"message": "Organization updated successfully"}
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def delete_organization(self, organization_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.delete_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:

                self.logger.info("Delete organization request", {
                    "organization_id": organization_id
                })

                await self.organization_service.delete_organization(organization_id)

                self.logger.info("Organization deleted successfully", {
                    "organization_id": organization_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={"message": "Organization deleted successfully"}
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
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
                    self.logger.warning("Неверный межсервисный ключ для пополнения баланса", {
                        "organization_id": body.organization_id
                    })
                    raise HTTPException(status_code=403, detail="Invalid interserver secret key")

                self.logger.info("Top up balance request", {
                    "organization_id": body.organization_id,
                    "amount_rub": body.amount_rub
                })

                await self.organization_service.top_up_balance(
                    organization_id=body.organization_id,
                    amount_rub=Decimal(body.amount_rub)
                )

                self.logger.info("Balance topped up successfully", {
                    "organization_id": body.organization_id,
                    "amount_rub": body.amount_rub
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Balance topped up successfully",
                        "organization_id": body.organization_id,
                        "amount_rub": body.amount_rub
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
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
                    self.logger.warning("Неверный межсервисный ключ для списания баланса", {
                        "organization_id": body.organization_id
                    })
                    raise HTTPException(status_code=403, detail="Invalid interserver secret key")

                self.logger.info("Debit balance request", {
                    "organization_id": body.organization_id,
                    "amount_rub": body.amount_rub
                })

                await self.organization_service.debit_balance(
                    organization_id=body.organization_id,
                    amount_rub=Decimal(body.amount_rub)
                )

                self.logger.info("Balance debited successfully", {
                    "organization_id": body.organization_id,
                    "amount_rub": body.amount_rub
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Balance debited successfully",
                        "organization_id": body.organization_id,
                        "amount_rub": body.amount_rub
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err