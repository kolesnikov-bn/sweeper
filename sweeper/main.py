from sweeper.app.persistence.rules.factories import rule_registry
from sweeper.app.usecases.sweeper_usecase import SweeperUsecase
from sweeper.infrastructure.settings.base import Settings


def main() -> None:
    SweeperUsecase(rule_registry, Settings()).usecase()


if __name__ == "__main__":
    main()
