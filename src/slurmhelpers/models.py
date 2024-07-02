# Copyright 2024 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Models for managing lifecycle operations inside the Slurm snap."""

import base64
import logging
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import dotenv
from slurmutils.editors import slurmconfig, slurmdbdconfig
from slurmutils.models import (
    DownNodes,
    DownNodesList,
    FrontendNode,
    FrontendNodeMap,
    Node,
    NodeMap,
    NodeSet,
    NodeSetMap,
    Partition,
    PartitionMap,
)
from snaphelpers import Snap


def _apply_callback(key, value, model) -> Any:
    """Apply callback to Slurm configuration value.

    This function will return the value unmodified if the passed Slurm
    configuration key does not have a callback or there is no parsing callback.

    Args:
        key: Slurm configuration key. Used to look up callback for value.
        value: Value to apply callback to.
        model: Configuration model with `callbacks` map.
    """
    if key in model.callbacks and (callback := model.callbacks[key].parse) is not None:
        value = callback(value)

    return value


class _BaseModel(ABC):

    def __init__(self, snap: Snap) -> None:
        self._snap = snap
        self._env_file = snap.paths.common / ".env"

    def _get_config(self, key: str) -> str:
        """Get a global configuration value.

        Args:
            key: Key of configuration value to retrieve from the .env file.
        """
        return dotenv.get_key(self._env_file, key)

    def _set_config(self, key: str, value: str) -> None:
        """Set the global configuration of the Slurm snap.

        This function updates configuration specific to the snap
        itself, not one of the bundled Slurm or munge services.
        A `.env` file in $SNAP_COMMON is used to store configuration
        values. These configuration values are used by service wrappers
        to control how the wrapped service is launched by the snap.

        Args:
            key: Configuration to update/set.
            value: Value to set for configuration.
        """
        logging.info("Setting %s to %s.", key, value if value != "" else "''")
        dotenv.set_key(self._env_file, key, value)

    @abstractmethod
    def update_config(self, config: Dict[str, str]) -> None:  # pragma: no cover
        """Update configuration specific to the service.

        Every model must have this method as it will be used
        to process configuration retrieved via `snapctl`. This
        method makes it easier to do unit tests on the hooks
        since each method can be tested easily.
        """
        raise NotImplementedError

    def _needs_restart(self, services: List[str]) -> None:
        """Determine if specified list of services needs to be restarted.

        Args:
            services: List of servers to check status of. If the service is active,
                log that the service needs to be restarted to the log file.
        """
        for service in services:
            if self._snap.services.list()[service].active:
                logging.info(
                    "Service `%s` must be restarted to apply latest configuration changes.",
                    service,
                )


class Munge(_BaseModel):
    """Manage lifecycle operations for the munge daemon."""

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.secret_file = self._snap.paths.common / "etc" / "munge" / "munge.key"

    @property
    def key(self) -> Optional[str]:
        """Get current munge.key secret. DO NOT EXPOSE THIS PUBLICLY."""
        if not self.secret_file.exists():
            return

        return base64.b64encode(self.secret_file.read_bytes()).decode()

    @key.setter
    def key(self, v: str) -> None:
        """Set new munge.key file secret."""
        if self.key == v:
            logging.debug("No change for `munge.key` secret file. Not updating.")
            return

        if not self.secret_file.exists():
            logging.debug("Creating empty `munge.key` secret file.")
            self.secret_file.touch(0o600)

        logging.info("Updating `munge.key` secret file to new key.")
        self.secret_file.write_bytes(base64.b64decode(v.encode()))
        self._needs_restart(["munged"])

    @property
    def max_thread_count(self) -> Optional[int]:
        """Get the number of threads to spawn for processing credential requests."""
        v = self._get_config("MUNGE_MAX_THREAD_COUNT")
        if v is None:
            return

        return int(v)

    @max_thread_count.setter
    def max_thread_count(self, v: int) -> None:
        """Set the number of threads to spawn for processing credential requests."""
        if self.max_thread_count == v:
            logging.debug("No change for `munged` max thread count. Not updating.")
            return

        self._set_config("MUNGED_MAX_THREAD_COUNT", str(v))
        self._needs_restart(["munged"])

    def generate_key(self) -> None:
        """Generate a default munge.key secret for the munge daemon upon installation.

        Replicates the daemon autostart feature from the  munge Debian package.
        """
        logging.info("Generating new secret file for service `munged`.")
        try:
            subprocess.check_output(["mungectl", "generate"])
        except subprocess.CalledProcessError:
            logging.fatal("Failed to generate a new munge key")
            raise

        self._needs_restart(["munged"])

    def update_config(self, config: Dict[str, str]) -> None:
        """Update configuration for the `munged` service."""
        for k in config.keys():
            match k:
                case "key":
                    self.key = config[k]
                case "max-thread-count":
                    self.max_thread_count = config[k]
                case _:
                    raise AttributeError(f"Unrecognised configuration option {k}.")


class Slurmd(_BaseModel):
    """Manage lifecycle operations for the slurmd daemon."""

    @property
    def config_server(self) -> Optional[str]:
        """Get comma-separated list of Slurm controllers.

        First controller in the list is the primary controller.
        """
        return self._get_config("SLURMD_CONFIG_SERVER")

    @config_server.setter
    def config_server(self, v: str) -> None:
        """Set comma-separated list of Slurm controllers.

        First controller in the list is the primary controller.
        """
        if self.config_server == v:
            logging.debug("No change for `slurmd` configuration server list. Not updating.")
            return

        self._set_config("SLURMD_CONFIG_SERVER", str(v))
        self._needs_restart(["slurmd"])

    def update_config(self, config: Dict[str, str]) -> None:
        """Update configuration for the `slurmd` service."""
        for k, v in config.items():
            match k:
                case "config-server":
                    self.config_server = v
                case _:
                    raise AttributeError(f"Unrecognised configuration option {k}.")


class Slurmdbd(_BaseModel):
    """Manage lifecycle operations for the slurmdbd daemon."""

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.config_file = self._snap.paths.common / "etc" / "slurm" / "slurmdbd.conf"

    def update_config(self, config: Dict[str, str]) -> None:
        """Update configuration for the `slurmdbd` service."""
        # Load current `slurmdbd.conf` configuration file.
        # Preserve old configuration so that we can determine
        # if substantial changes were made to the `slurmdbd.conf` file.
        sconf = slurmdbdconfig.load(self.config_file)
        old = sconf.dict()

        # Assemble new `slurmdbd.conf` file.
        for k, v in config.items():
            key = k.replace("-", "_")
            if not hasattr(sconf, key):
                raise AttributeError(f"`slurmdbd` config file does not support option {key}.")

            setattr(sconf, key, _apply_callback(key, v, model=sconf))

        if sconf.dict() == old:
            logging.debug("No change in `slurmdbd` service configuration. Not updating.")
            return

        slurmdbdconfig.dump(sconf, self.config_file)
        self._needs_restart(["slurmdbd"])


class Slurmrestd(_BaseModel):
    """Manage lifecycle operations for the slurmrestd daemon."""

    @property
    def max_connections(self) -> Optional[int]:
        """Get the maximum number of client connections to process at one time."""
        v = self._get_config("SLURMRESTD_MAX_CONNECTIONS")
        if v is None:
            return

        return int(v)

    @max_connections.setter
    def max_connections(self, v: int) -> None:
        """Set the maximum number of client connections to process at one time."""
        if self.max_connections == v:
            logging.debug("No change for `slurmrestd` max connections. Not updating.")
            return

        self._set_config("SLURMRESTD_MAX_CONNECTIONS", str(v))
        self._needs_restart(["slurmrestd"])

    @property
    def max_thread_count(self) -> Optional[int]:
        """Get the number of threads to spawn for processing client requests."""
        v = self._get_config("SLURMRESTD_MAX_THREAD_COUNT")
        if v is None:
            return

        return int(v)

    @max_thread_count.setter
    def max_thread_count(self, v: int) -> None:
        """Set the number of threads to spawn for processing client requests."""
        if self.max_thread_count == v:
            logging.debug("No change for `slurmrestd` max thread count. Not updating.")
            return

        self._set_config("SLURMRESTD_MAX_THREAD_COUNT", str(v))
        self._needs_restart(["slurmrestd"])

    def update_config(self, config: Dict[str, str]) -> None:
        """Update configuration for the `slurmrestd` service."""
        for k in config.keys():
            match k:
                case "max-connections":
                    self.max_connections = config[k]
                case "max-thread-count":
                    self.max_thread_count = config[k]
                case _:
                    raise AttributeError(f"Unrecognised configuration option {k}.")


def _process_nodes(config: Dict[str, Dict[str, Any]]) -> NodeMap:
    """Process node inventory from the Slurm snap configuration."""
    node_map = NodeMap()
    for k, v in config.items():
        node = Node(NodeName=k)
        for _k, _v in v.items():
            key = _k.replace("-", "_")
            if not hasattr(node, key):
                raise AttributeError(f"Node: Unrecognised configuration option {key}.")

            setattr(node, key, _apply_callback(key, _v, model=node))

        node_map[node.node_name] = node

    return node_map


def _process_frontend_nodes(config: Dict[str, Dict[str, Any]]) -> FrontendNodeMap:
    """Process frontend node inventory from the Slurm snap configuration."""
    frontend_map = FrontendNodeMap()
    for k, v in config.items():
        node = FrontendNode(FrontendName=k)
        for _k, _v in v.items():
            key = _k.replace("-", "_")
            if not hasattr(node, key):
                raise AttributeError(f"FrontendNode: Unrecognised configuration option {key}.")

            setattr(node, key, _apply_callback(key, _v, model=node))

        frontend_map[node.frontend_name] = node

    return frontend_map


def _process_down_nodes(config: Dict[str, str]) -> DownNodesList:
    """Process down nodes inventory from the Slurm snap configuration.

    Only one DownNodes can be set via `snap set ...`. If extended functionality
    beyond this is required, it's better to either directly set the configuration
    file, or use a different method to update the `slurm.conf` file.
    """
    down_nodes = DownNodes()
    for k, v in config.items():
        match key := k.replace("-", "_"):
            case "nodes":
                down_nodes.down_nodes = v.split(",")
            case "reason":
                down_nodes.reason = v
            case "state":
                down_nodes.state = v
            case _:
                raise AttributeError(f"DownNodes: Unrecognised configuration option {key}.")

    return DownNodesList([down_nodes.dict()])


def _process_node_sets(config: Dict[str, Dict[str, Any]]) -> NodeSetMap:
    """Process node set inventory from the Slurm snap configuration."""
    node_set_map = NodeSetMap()
    for k, v in config.items():
        node = NodeSet(NodeSet=k)
        for _k, _v in v.items():
            key = _k.replace("-", "_")
            if not hasattr(node, key):
                raise AttributeError(f"NodeSet: Unrecognised configuration option {key}.")

            setattr(node, key, _apply_callback(key, _v, model=node))

        node_set_map[node.node_set] = node

    return node_set_map


def _process_partitions(config: Dict[str, Dict[str, Any]]) -> PartitionMap:
    """Process partition inventory from the Slurm snap configuration."""
    partition_map = PartitionMap()
    for k, v in config.items():
        part = Partition(PartitionName=k)
        for _k, _v in v.items():
            key = _k.replace("-", "_")
            if not hasattr(part, key):
                raise AttributeError(f"FrontendNode: Unrecognised configuration option {key}.")

            setattr(part, key, _apply_callback(key, _v, model=part))

        partition_map[part.partition_name] = part

    return partition_map


class Slurm(_BaseModel):
    """Manage lifecycle operations for the Slurm workload manager."""

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.config_file = self._snap.paths.common / "etc" / "slurm" / "slurm.conf"

    def update_config(self, config: Dict[str, Any]) -> None:
        """Update configuration of the Slurm workload manager."""
        # Load current `slurm.conf` configuration file.
        # Preserve old configuration so that we can determine
        # if substantial changes were made to the `slurm.conf` file.
        sconf = slurmconfig.load(self.config_file)
        old = sconf.dict()

        # Assemble new `slurm.conf` file.
        for k, v in config.items():
            match key := k.replace("-", "_"):
                case "include":
                    # Multiline configuration options. Requires special handling.
                    sconf.include = v.split(",")
                case "slurmctld_host":
                    # Multiline configuration options. Requires special handling.
                    sconf.slurmctld_host = v.split(",")
                case "nodes":
                    sconf.nodes = _process_nodes(v)
                case "frontend_nodes":
                    sconf.frontend_nodes = _process_frontend_nodes(v)
                case "down_nodes":
                    sconf.down_nodes = _process_down_nodes(v)
                case "node_sets":
                    sconf.node_sets = _process_node_sets(v)
                case "partitions":
                    sconf.partitions = _process_partitions(v)
                case _:
                    if not hasattr(sconf, key):
                        raise AttributeError(f"Slurm config file does not support option {key}.")

                    setattr(sconf, key, _apply_callback(key, v, model=sconf))

        if sconf.dict() == old:
            logging.debug("No change in Slurm workload manager configuration. Not updating.")
            return

        logging.info("Updating Slurm workload manager configuration file %s.", self.config_file)
        slurmconfig.dump(sconf, self.config_file)
        self._needs_restart(["slurmctld", "slurmd", "slurmdbd", "slurmrestd"])
