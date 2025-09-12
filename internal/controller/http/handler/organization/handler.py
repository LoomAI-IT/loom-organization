from opentelemetry.trace import Status, StatusCode, SpanKind
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from internal import interface
from internal.controller.http.handler.organization.model import (
    CreateOrganizationBody, UpdateOrganizationBody
)


class OrganizationController(interface.IOrganizationController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            organization_service: interface.IOrganizationService,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.organization_service = organization_service

    async def create_organization(self, body: CreateOrganizationBody) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.create_organization",
                kind=SpanKind.INTERNAL,
                attributes={"name": body.name}
        ) as span:
            try:

                self.logger.info("Create organization request", {
                    "name": body.name
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
                authorization_data = request.state.authorization_data
                account_id = authorization_data.account_id

                if account_id == 0:
                    raise HTTPException(status_code=401, detail="Unauthorized")

                self.logger.info("Get organization by ID request", {
                    "account_id": account_id,
                    "organization_id": organization_id
                })

                organization = await self.organization_service.get_organization_by_id(organization_id)

                self.logger.info("Organization retrieved successfully", {
                    "account_id": account_id,
                    "organization_id": organization_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Organization retrieved successfully",
                        "organization": organization.to_dict()
                    }
                )

            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def get_organization_by_employee_id(self, request: Request, employee_id: int) -> JSONResponse:
        with self.tracer.start_as_current_span(
                "OrganizationController.get_organization_by_employee_id",
                kind=SpanKind.INTERNAL,
                attributes={"employee_id": employee_id}
        ) as span:
            try:
                authorization_data = request.state.authorization_data
                account_id = authorization_data.account_id

                if account_id == 0:
                    raise HTTPException(status_code=401, detail="Unauthorized")

                self.logger.info("Get organization by employee ID request", {
                    "account_id": account_id,
                    "employee_id": employee_id
                })

                organization = await self.organization_service.get_organization_by_employee_id(employee_id)

                self.logger.info("Organization retrieved by employee ID successfully", {
                    "account_id": account_id,
                    "employee_id": employee_id
                })

                span.set_status(Status(StatusCode.OK))
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Organization retrieved successfully",
                        "organization": organization.to_dict()
                    }
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
                authorization_data = request.state.authorization_data
                account_id = authorization_data.account_id

                if account_id == 0:
                    raise HTTPException(status_code=401, detail="Unauthorized")

                self.logger.info("Update organization request", {
                    "account_id": account_id,
                })

                await self.organization_service.update_organization(
                    organization_id=body.organization_id,
                    name=body.name,
                    autoposting_moderation=body.autoposting_moderation,
                    video_cut_description_end_sample=body.video_cut_description_end_sample,
                    publication_text_end_sample=body.publication_text_end_sample
                )

                self.logger.info("Organization updated successfully", {
                    "account_id": account_id
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