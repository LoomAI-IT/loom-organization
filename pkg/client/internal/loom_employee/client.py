from contextvars import ContextVar

from opentelemetry.trace import SpanKind

from internal import model
from internal import interface
from pkg.client.client import AsyncHTTPClient
from pkg.trace_wrapper import traced_method


class LoomEmployeeClient(interface.ILoomEmployeeClient):
    def __init__(
            self,
            tel: interface.ITelemetry,
            host: str,
            port: int,
            log_context: ContextVar[dict],
    ):
        logger = tel.logger()
        self.client = AsyncHTTPClient(
            host,
            port,
            prefix="/api/employee",
            use_tracing=True,
            log_context=log_context
        )
        self.tracer = tel.tracer()

    @traced_method(SpanKind.CLIENT)
    async def get_employees_by_organization(self, organization_id: int) -> list[model.Employee]:
        response = await self.client.get(f"/organization/{organization_id}/employees")
        json_response = response.json()

        return [model.Employee(**emp) for emp in json_response["employees"]]

    @traced_method(SpanKind.CLIENT)
    async def delete_employee(self, account_id: int) -> None:
        await self.client.delete(f"/{account_id}")

