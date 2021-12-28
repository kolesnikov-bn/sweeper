from infrastructure.settings.base import Settings

from sweeper.persistence.rules.factories import rule_registry
from sweeper.usecases.sweeper_usecase import SweeperUsecase


def main() -> None:
    SweeperUsecase(rule_registry, Settings()).usecase()


if __name__ == "__main__":
    main()
