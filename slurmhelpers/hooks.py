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

"""Hooks for the Slurm snap."""

import logging
from pathlib import Path
from typing import Dict

import dotenv
from snaphelpers import Snap

from .log import log
from .models import Munge, Slurm, Slurmd, Slurmdbd, Slurmrestd

snap = Snap()
munge = Munge(snap)
slurm = Slurm(snap)
slurmd = Slurmd(snap)
slurmdbd = Slurmdbd(snap)
slurmrestd = Slurmrestd(snap)


def _setup_dirs() -> None:
    """Create directories needed by Slurm and Munge to function within the snap."""
    # Generate directories need by Slurm and Munge.
    logging.info("Provisioning required directories for Slurm and munge.")
    etc = Path(snap.paths.common) / "etc"
    var = Path(snap.paths.common) / "var"
    for directory in [
        # etc - configuration files
        etc / "default",
        etc / "munge",
        etc / "slurm",
        etc / "slurm" / "plugstack.conf.d",
        etc / "slurm" / "epilog.d",
        etc / "slurm" / "prolog.d",
        # var/lib - variable state information
        var / "lib" / "munge",
        var / "lib" / "slurm",
        var / "lib" / "slurm" / "checkpoint",
        var / "lib" / "slurm" / "slurmctld",
        var / "lib" / "slurm" / "slurmd",
        var / "lib" / "slurm" / "slurmdbd",
        var / "lib" / "slurm" / "slurmrestd",
        # var/log - variable log data
        var / "log" / "slurm",
        # var/run - variable runtime data
        var / "run" / "munge",
    ]:
        logging.debug("Generating directory %s.", directory)
        directory.mkdir(parents=True)

    # Set permissions on special directories
    logging.debug("Updating directory permissions.")
    etc.chmod(0o711)
    (etc / "munge").chmod(0o700)
    (etc / "slurm").chmod(0o755)
    (var / "lib" / "munge").chmod(0o711)
    (var / "run" / "munge").chmod(0o755)


def _update_global_config(config: Dict[str, str]) -> bool:
    """Update the global configuration of the Slurm snap.

    This function updates configuration specific to the snap
    itself, not one of the bundled Slurm or munge services.
    A `.env` file in $SNAP_COMMON is used to store configuration
    values. These configuration values are used by service wrappers
    to control how the wrapped service is launched by the snap.

    Args:
        config: Map of configuration values to update/set.
    """
    env_file = snap.paths.common / ".env"
    for k, v in config.items():
        logging.debug("Setting %s to %s.", k, v if v != "" else "''")
        dotenv.set_key(env_file, k, v)


@log(file=snap.paths.common / "hooks.log")
def install(_: Snap) -> None:
    """Install hook for the Slurm snap.

    The install hook will create the default directories
    required by munge and Slurm under $SNAP_DATA, set the default
    snap configuration, and generate a munge.key file for the host.
    """
    logging.info("Executing snap `install` hook.")
    _setup_dirs()

    logging.info("Setting default global configuration for snap.")
    munge.max_thread_count = 1
    slurmd.config_server = ""
    slurmrestd.max_connections = 124
    slurmrestd.max_thread_count = 20

    logging.info("Generating default munge.key secret.")
    munge.generate_key()


@log(file=snap.paths.common / "hooks.log")
def configure(_: Snap) -> None:
    """Configure hook for the Slurm snap."""
    logging.debug("Executing snap `configure` hook.")
    options = snap.config.get_options(
        "munge", "slurm", "slurmd", "slurmdbd", "slurmrestd"
    ).as_dict()

    if "munge" in options:
        logging.info("Updating the `munged` service's configuration.")
        munge.update_config(options["munge"])

    if "slurm" in options:
        logging.info("Updating Slurm workload manager configuration.")
        slurm.update_config(options["slurm"])

    if "slurmd" in options:
        logging.info("Updating `slurmd` service configuration.")
        slurmd.update_config(options["slurmd"])

    if "slurmdbd" in options:
        logging.info("Updating `slurmdbd` service configuration.")
        slurmdbd.update_config(options["slurmdbd"])

    if "slurmrestd" in options:
        logging.info("Updating `slurmrestd` service configuration.")
        slurmrestd.update_config(options["slurmrestd"])
