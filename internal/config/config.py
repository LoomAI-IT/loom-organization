import os


class Config:
    def __init__(self):
        # Основные настройки сервиса
        self.service_name = os.getenv("SERVICE_NAME", "organization-service")
        self.service_version = os.getenv("SERVICE_VERSION", "1.0.0")
        self.environment = os.getenv("ENVIRONMENT", "dev")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.root_path = os.getenv("ROOT_PATH", "/")
        self.prefix = os.getenv("PREFIX", "/api/v1")
        self.http_port = os.getenv("HTTP_PORT", "8080")

        # Настройки базы данных PostgreSQL
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "organization_db")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_pass = os.getenv("DB_PASS", "postgres")

        # Настройки OTLP (OpenTelemetry)
        self.otlp_host = os.getenv("OTLP_HOST", "localhost")
        self.otlp_port = int(os.getenv("OTLP_PORT", "4317"))

        # Настройки алертинга в Telegram
        self.alert_tg_bot_token = os.getenv("ALERT_TG_BOT_TOKEN", "")
        self.alert_tg_chat_id = int(os.getenv("ALERT_TG_CHAT_ID", "0"))
        self.alert_tg_chat_thread_id = int(os.getenv("ALERT_TG_CHAT_THREAD_ID", "0"))

        # Настройки Grafana
        self.grafana_url = os.getenv("GRAFANA_URL", "http://localhost:3000")

        # Настройки Redis для мониторинга
        self.monitoring_redis_host = os.getenv("MONITORING_REDIS_HOST", "localhost")
        self.monitoring_redis_port = int(os.getenv("MONITORING_REDIS_PORT", "6379"))
        self.monitoring_redis_db = int(os.getenv("MONITORING_REDIS_DB", "0"))
        self.monitoring_redis_password = os.getenv("MONITORING_REDIS_PASSWORD", "")

        # Настройки клиента авторизации Kontur
        self.kontur_authorization_host = os.getenv("KONTUR_AUTHORIZATION_HOST", "localhost")
        self.kontur_authorization_port = int(os.getenv("KONTUR_AUTHORIZATION_PORT", "8081"))