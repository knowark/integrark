from pathlib import Path
from ...application.services import QueryService, StandardQueryService
from ...application.coordinators import ExecutionCoordinator
from ..core import Config, JwtSupplier
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def standard_query_service(self) -> StandardQueryService:
        return StandardQueryService()

    def execution_coordinator(
            self, query_service: QueryService) -> ExecutionCoordinator:
        return ExecutionCoordinator(query_service)

    def jwt_supplier(self) -> JwtSupplier:
        secret_file = Path(self.config.get('secrets', {}).get('jwt', ''))
        secret = (secret_file.read_text().strip()
                  if secret_file.is_file() else 'INTEGRARK_SECRET')

        return JwtSupplier(secret)
