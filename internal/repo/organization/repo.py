from opentelemetry.trace import Status, StatusCode, SpanKind
from fastapi.responses import JSONResponse

from .sql_query import *
from internal import interface, model, common


class OrganizationRepo(interface.IOrganizationRepo):
    def __init__(
            self,
            tel: interface.ITelemetry,
            db: interface.IDB,
    ):
        self.tracer = tel.tracer()
        self.db = db

    async def create_organization(self, name: str, autoposting_moderation: bool = True) -> int:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.create_organization",
                kind=SpanKind.INTERNAL,
                attributes={"name": name}
        ) as span:
            try:
                args = {
                    'name': name,
                    'autoposting_moderation': autoposting_moderation,
                }

                organization_id = await self.db.insert(create_organization, args)

                span.set_status(Status(StatusCode.OK))
                return organization_id
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def get_organization_by_id(self, organization_id: int) -> list[model.Organization]:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.get_organization_by_id",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                args = {'organization_id': organization_id}
                rows = await self.db.select(get_organization_by_id, args)
                organizations = model.Organization.serialize(rows) if rows else []

                span.set_status(Status(StatusCode.OK))
                return organizations
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err


    async def get_all_organizations(self) -> list[model.Organization]:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.get_all_organizations",
                kind=SpanKind.INTERNAL
        ) as span:
            try:
                rows = await self.db.select(get_all_organizations, {})
                organizations = model.Organization.serialize(rows) if rows else []

                span.set_status(Status(StatusCode.OK))
                return organizations
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def update_organization(
            self,
            organization_id: int,
            name: str = None,
            autoposting_moderation: bool = None,
            video_cut_description_end_sample: str = None,
            publication_text_end_sample: str = None,
    ) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.update_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                # Формируем запрос динамически в зависимости от переданных параметров
                update_fields = []
                args: dict = {'organization_id': organization_id}

                if name is not None:
                    update_fields.append("name = :name")
                    args['name'] = name

                if autoposting_moderation is not None:
                    update_fields.append("autoposting_moderation = :autoposting_moderation")
                    args['autoposting_moderation'] = autoposting_moderation

                if video_cut_description_end_sample is not None:
                    update_fields.append("video_cut_description_end_sample = :video_cut_description_end_sample")
                    args['video_cut_description_end_sample'] = video_cut_description_end_sample

                if publication_text_end_sample is not None:
                    update_fields.append("publication_text_end_sample = :publication_text_end_sample")
                    args['publication_text_end_sample'] = publication_text_end_sample

                if not update_fields:
                    # Если нет полей для обновления, просто возвращаемся
                    span.set_status(Status(StatusCode.OK))
                    return

                # Формируем финальный запрос
                query = f"""
                UPDATE organizations 
                SET {', '.join(update_fields)}
                WHERE id = :organization_id;
                """

                await self.db.update(query, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def delete_organization(self, organization_id: int) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.delete_organization",
                kind=SpanKind.INTERNAL,
                attributes={"organization_id": organization_id}
        ) as span:
            try:
                args = {'organization_id': organization_id}
                await self.db.update(delete_organization, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def top_up_balance(self, organization_id: int, amount_rub: int) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.top_up_balance",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                    "amount_rub": amount_rub
                }
        ) as span:
            try:
                args = {
                    'organization_id': organization_id,
                    'amount_rub': amount_rub
                }
                await self.db.update(top_up_balance, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err

    async def debit_balance(self, organization_id: int, amount_rub: int) -> None:
        with self.tracer.start_as_current_span(
                "OrganizationRepo.debit_balance",
                kind=SpanKind.INTERNAL,
                attributes={
                    "organization_id": organization_id,
                    "amount_rub": amount_rub
                }
        ) as span:
            try:
                args = {
                    'organization_id': organization_id,
                    'amount_rub': amount_rub
                }
                await self.db.update(debit_balance, args)

                span.set_status(Status(StatusCode.OK))
            except Exception as err:
                span.record_exception(err)
                span.set_status(Status(StatusCode.ERROR, str(err)))
                raise err