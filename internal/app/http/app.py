from fastapi import FastAPI
from starlette.responses import StreamingResponse

from internal import model, interface
from internal.controller.http.handler.organization.model import *


def NewHTTP(
        db: interface.IDB,
        organization_controller: interface.IOrganizationController,
        http_middleware: interface.IHttpMiddleware,
        prefix: str
):
    app = FastAPI(
        title="Organization Service API",
        description="API для управления организациями",
        version="1.0.0",
        openapi_url=prefix + "/openapi.json",
        docs_url=prefix + "/docs",
        redoc_url=prefix + "/redoc",
    )
    include_middleware(app, http_middleware)
    include_db_handler(app, db, prefix)
    include_organization_handlers(app, organization_controller, prefix)

    return app


def include_middleware(
        app: FastAPI,
        http_middleware: interface.IHttpMiddleware,
):
    # Порядок middleware важен - они применяются в обратном порядке регистрации
    http_middleware.authorization_middleware04(app)
    http_middleware.logger_middleware03(app)
    http_middleware.metrics_middleware02(app)
    http_middleware.trace_middleware01(app)


def include_organization_handlers(
        app: FastAPI,
        organization_controller: interface.IOrganizationController,
        prefix: str
):
    # Создание организации
    app.add_api_route(
        prefix + "/create",
        organization_controller.create_organization,
        methods=["POST"],
        tags=["Organization"],
        response_model=CreateOrganizationResponse,
        summary="Создать организацию",
        description="Создает новую организацию с указанным именем"
    )

    # Получение организации по ID
    app.add_api_route(
        prefix + "/{organization_id}",
        organization_controller.get_organization_by_id,
        methods=["GET"],
        tags=["Organization"],
        response_model=GetOrganizationResponse,
        summary="Получить организацию по ID",
        description="Возвращает информацию об организации по её идентификатору"
    )

    # Получение всех организаций
    app.add_api_route(
        prefix + "/all",
        organization_controller.get_all_organizations,
        methods=["GET"],
        tags=["Organization"],
        response_model=GetAllOrganizationsResponse,
        summary="Получить все организации",
        description="Возвращает список всех организаций"
    )

    # Обновление организации
    app.add_api_route(
        prefix + "",
        organization_controller.update_organization,
        methods=["PUT"],
        tags=["Organization"],
        response_model=UpdateOrganizationResponse,
        summary="Обновить организацию",
        description="Обновляет информацию об организации"
    )

    # Удаление организации
    app.add_api_route(
        prefix + "/{organization_id}",
        organization_controller.delete_organization,
        methods=["DELETE"],
        tags=["Organization"],
        response_model=DeleteOrganizationResponse,
        summary="Удалить организацию",
        description="Удаляет организацию по её идентификатору"
    )

    # Пополнение баланса организации
    app.add_api_route(
        prefix + "/balance/top-up",
        organization_controller.top_up_balance,
        methods=["POST"],
        tags=["Organization"],
        summary="Пополнить баланс организации",
        description="Пополняет баланс организации на указанную сумму (требует межсервисный ключ)"
    )

    # Списание с баланса организации
    app.add_api_route(
        prefix + "/balance/debit",
        organization_controller.debit_balance,
        methods=["POST"],
        tags=["Organization"],
        summary="Списать с баланса организации",
        description="Списывает указанную сумму с баланса организации (требует межсервисный ключ)"
    )


def include_db_handler(app: FastAPI, db: interface.IDB, prefix: str):
    """
    Добавляет служебные эндпоинты для управления базой данных
    """
    app.add_api_route(
        prefix + "/table/create",
        create_table_handler(db),
        methods=["GET"],
        tags=["Database"],
        summary="Создать таблицы",
        description="Создает все необходимые таблицы в базе данных"
    )

    app.add_api_route(
        prefix + "/table/drop",
        drop_table_handler(db),
        methods=["GET"],
        tags=["Database"],
        summary="Удалить таблицы",
        description="Удаляет все таблицы из базы данных"
    )
    app.add_api_route(prefix + "/health", heath_check_handler(), methods=["GET"])

def heath_check_handler():
    async def heath_check():
        return "ok"

    return heath_check

def create_table_handler(db: interface.IDB):
    async def create_table():
        try:
            await db.multi_query(model.create_organization_tables_queries)
            return {"message": "Tables created successfully"}
        except Exception as err:
            raise err

    return create_table


def drop_table_handler(db: interface.IDB):
    async def drop_table():
        try:
            await db.multi_query(model.drop_organization_tables_queries)
            return {"message": "Tables dropped successfully"}
        except Exception as err:
            raise err

    return drop_table