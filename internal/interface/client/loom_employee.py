from typing import Protocol
from abc import abstractmethod
from internal import model


class ILoomEmployeeClient(Protocol):
    @abstractmethod
    async def get_employees_by_organization(self, organization_id: int) -> list[model.Employee]: pass

    @abstractmethod
    async def delete_employee(self, account_id: int) -> None: pass
