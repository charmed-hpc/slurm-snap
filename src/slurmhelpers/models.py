# Copyright 2024-2025 Canonical Ltd.
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

import logging
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import dotenv
from snaphelpers import Snap


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
        logging.info("setting %s to %s", key, value if value != "" else "''")
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
                    "service `%s` must be restarted to apply latest configuration changes",
                    service,
                )


class Munged(_BaseModel):
    """Manage lifecycle operations for the munge daemon."""

    def __init__(self, *args) -> None:
        super().__init__(*args)

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
        logging.info("generating new secret key file for service `munged`")
        try:
            subprocess.check_output(
                [
                    "mungectl",
                    "key",
                    f"--keyfile={self._snap.paths.common / 'etc/munge/munge.key'}",
                    "generate",
                ]
            )
        except subprocess.CalledProcessError as e:
            logging.error("failed to generate a new munge key. reason %s", e)
            raise

        self._needs_restart(["munged"])

    def update_config(self, config: Dict[str, str]) -> None:
        """Update configuration for the `munged` service."""
        for k in config.keys():
            match k:
                case "max-thread-count":
                    self.max_thread_count = config[k]
                case _:
                    raise AttributeError(f"Unrecognized configuration option {k}")


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
            logging.debug("no change for `slurmd` configuration server list. not updating")
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
                    raise AttributeError(f"Unrecognized configuration option {k}")


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
            logging.debug("no change for `slurmrestd` max connections. not updating")
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
            logging.debug("no change for `slurmrestd` max thread count. not updating")
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
                    raise AttributeError(f"Unrecognized configuration option {k}")
