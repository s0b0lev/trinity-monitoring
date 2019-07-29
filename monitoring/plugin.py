import argparse
import asyncio
import logging

from lahja import ConnectionConfig

from trinity.constants import MAIN_EVENTBUS_ENDPOINT

from trinity.config import TrinityConfig
from trinity.endpoint import TrinityEventBusEndpoint
from trinity.extensibility.events import PluginStartedEvent

from trinity.extensibility import BaseMainProcessPlugin
from trinity.protocol.eth.events import NewBlockHashesEvent
from trinity._utils.os import friendly_filename_or_url


async def monitoring(normalized_name, trinity_config) -> None:
    event_bus = TrinityEventBusEndpoint("monitoring_ui")
    connection_config = ConnectionConfig.from_name(
        normalized_name,
        trinity_config.ipc_dir,
    )
    await event_bus.start()
    await event_bus.start_server(connection_config.path)
    await event_bus.connect_to_endpoints(
        ConnectionConfig.from_name(
            MAIN_EVENTBUS_ENDPOINT, trinity_config.ipc_dir
        )
    )
    await event_bus.announce_endpoint()
    await event_bus.broadcast(
        PluginStartedEvent(type(MonitoringPlugin))
    )

    asyncio.ensure_future(event_bus.auto_connect_new_announced_endpoints())
    event_bus.subscribe(
        NewBlockHashesEvent,
        lambda event: logging.info(
            event.msg
        )
    )


class MonitoringPlugin(BaseMainProcessPlugin):
    @property
    def name(self) -> str:
        return "Monitoring UI"

    @classmethod
    def configure_parser(cls,
                         arg_parser: argparse.ArgumentParser,
                         subparser: argparse._SubParsersAction) -> None:

        attach_parser = subparser.add_parser(
            'monitoring',
            help='Open monitoring UI',
        )
        attach_parser.set_defaults(func=cls.run_monitoring)

    @classmethod
    def run_monitoring(cls, args: argparse.Namespace, trinity_config: TrinityConfig):
        normalized_name = friendly_filename_or_url("monitoring_ui")
        with trinity_config.process_id_file(normalized_name):
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(monitoring(normalized_name, trinity_config))
            loop.run_forever()
            loop.close()
