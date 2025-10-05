from contextvars import ContextVar

from opentelemetry.trace import Status, StatusCode, SpanKind

from internal import model
from internal import interface
from pkg.client.client import AsyncHTTPClient


class LoomAuthorizationClient(interface.ILoomAuthorizationClient):
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
            prefix="/api/authorization",
            use_tracing=True,
            logger=logger,
            log_context=log_context
        )
        self.tracer = tel.tracer()

    async def authorization(self, account_id: int) -> model.JWTTokens:
        with self.tracer.start_as_current_span(
                "LoomAuthorizationClient.authorization",
                kind=SpanKind.CLIENT,
                attributes={
                    "account_id": account_id
                }
        ) as span:
            try:
                body = {
                    "account_id": account_id
                }
                response = await self.client.post("/", json=body)
                json_response = response.json()

                span.set_status(StatusCode.OK)
                return model.JWTTokens(**json_response)
            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
                raise

    async def check_authorization(self, access_token: str) -> model.AuthorizationData:
        with self.tracer.start_as_current_span(
                "LoomAuthorizationClient.check_authorization",
                kind=SpanKind.CLIENT,
        ) as span:
            try:
                cookies = {"Access-Token": access_token}
                response = await self.client.get("/check", cookies=cookies)
                json_response = response.json()

                span.set_status(StatusCode.OK)
                return model.AuthorizationData(**json_response)
            except Exception as e:
                
                span.set_status(StatusCode.ERROR, str(e))
                raise