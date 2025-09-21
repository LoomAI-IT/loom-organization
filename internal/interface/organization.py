from abc import abstractmethod
from typing import Protocol

from fastapi.responses import JSONResponse
from fastapi import Request

from internal import model
from internal.controller.http.handler.organization.model import *


class IOrganizationController(Protocol):
    @abstractmethod
    async def create_organization(
            self,
            body: CreateOrganizationBody
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def get_organization_by_id(self, request: Request,  organization_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def get_all_organizations(self) -> JSONResponse:
        pass

    @abstractmethod
    async def update_organization(
            self,
            request: Request,
            body: UpdateOrganizationBody
    ) -> JSONResponse:
        pass

    @abstractmethod
    async def delete_organization(self, organization_id: int) -> JSONResponse:
        pass

    @abstractmethod
    async def top_up_balance(self, body: TopUpBalanceBody) -> JSONResponse:
        pass

    @abstractmethod
    async def debit_balance(self, body: DebitBalanceBody) -> JSONResponse:
        pass


class IOrganizationService(Protocol):
    @abstractmethod
    async def create_organization(
            self,
            name: str
    ) -> int:
        pass

    @abstractmethod
    async def get_organization_by_id(self, organization_id: int) -> model.Organization:
        pass

    @abstractmethod
    async def get_all_organizations(self) -> list[model.Organization]:
        pass

    @abstractmethod
    async def update_organization(
            self,
            organization_id: int,
            name: str = None,
            autoposting_moderation: bool = None,
            video_cut_description_end_sample: str = None,
            publication_text_end_sample: str = None,
    ) -> None:
        pass

    @abstractmethod
    async def delete_organization(self, organization_id: int) -> None:
        pass

    @abstractmethod
    async def top_up_balance(self, organization_id: int, amount_rub: Decimal) -> None:
        pass

    @abstractmethod
    async def debit_balance(self, organization_id: int, amount_rub: Decimal) -> None:
        pass


class IOrganizationRepo(Protocol):
    @abstractmethod
    async def create_organization(
            self,
            name: str,
    ) -> int:
        pass

    @abstractmethod
    async def get_organization_by_id(self, organization_id: int) -> list[model.Organization]:
        pass

    @abstractmethod
    async def get_all_organizations(self) -> list[model.Organization]:
        pass

    @abstractmethod
    async def update_organization(
            self,
            organization_id: int,
            name: str = None,
            autoposting_moderation: bool = None,
            video_cut_description_end_sample: str = None,
            publication_text_end_sample: str = None,
    ) -> None:
        pass

    @abstractmethod
    async def delete_organization(self, organization_id: int) -> None:
        pass

    @abstractmethod
    async def update_balance(self, organization_id: int, rub_balance: str) -> None:
        pass
