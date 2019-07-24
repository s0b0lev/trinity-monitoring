from argparse import (
    ArgumentParser,
    Namespace,
    _SubParsersAction,
)

from trinity.config import (
    TrinityConfig,
)
from trinity.extensibility import (
    BaseMainProcessPlugin,
)


class MonitoringPlugin(BaseMainProcessPlugin):
    @property
    def name(self) -> str:
        return "Monitoring UI"

    @classmethod
    def configure_parser(cls,
                         arg_parser: ArgumentParser,
                         subparser: _SubParsersAction) -> None:

        attach_parser = subparser.add_parser(
            'monitoring',
            help='Open monitoring UI',
        )
        attach_parser.set_defaults(func=cls.run_monitoring)

    @classmethod
    def run_monitoring(cls, args: Namespace, trinity_config: TrinityConfig) -> None:
        pass
