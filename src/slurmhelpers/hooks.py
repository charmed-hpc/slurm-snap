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

"""Hooks for the Slurm snap."""

import logging
import os
from pathlib import Path

from snaphelpers import Snap

from .log import setup_logging
from .models import Munged, Slurmd, Slurmrestd


def _setup_dirs(snap: Snap) -> None:
    """Create directories needed by Slurm and Munge to function within the snap.

    Args:
        snap: The Snap instance.
    """
    # Generate directories need by Slurm and Munge.
    logging.info("provisioning required directories for slurm and munge")
    etc = Path(snap.paths.common) / "etc"
    var = Path(snap.paths.common) / "var"
    run = Path(snap.paths.common) / "run"
    for directory in [
        # etc - configuration files
        etc / "logrotate",
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
        # run - variable runtime data
        run / "munge",
        run / "slurm",
    ]:
        logging.debug("generating directory %s", directory)
        directory.mkdir(parents=True)

    # Set permissions on special directories
    logging.debug("updating directory permissions")
    etc.chmod(0o711)
    (etc / "munge").chmod(0o700)
    (etc / "slurm").chmod(0o755)
    (var / "lib" / "munge").chmod(0o711)
    (run / "munge").chmod(0o755)


def _setup_logrotate(snap: Snap) -> None:
    """Configure `logrotate` for the Slurm.

    Args:
        snap: The Snap instance.
    """
    tmpl = (snap.paths.snap / "templates" / "logrotate.conf.tmpl").read_text()
    config = os.path.expandvars(tmpl)
    (snap.paths.common / "etc" / "logrotate" / "logrotate.conf").write_text(config)


def install(snap: Snap) -> None:
    """Install hook for the Slurm snap.

    The install hook will create the default directories
    required by munge and Slurm under $SNAP_DATA, set the default
    snap configuration, and generate a munge.key file for the host.
    """
    setup_logging(snap.paths.common / "hooks.log")
    munged = Munged(snap)
    slurmd = Slurmd(snap)
    slurmrestd = Slurmrestd(snap)

    logging.info("executing snap `install` hook")
    _setup_dirs(snap)
    _setup_logrotate(snap)

    logging.info("setting default global configuration for snap")
    munged.max_thread_count = 1
    slurmd.config_server = ""
    slurmrestd.max_connections = 124
    slurmrestd.max_thread_count = 20

    logging.info("generating default munge.key secret")
    munged.generate_key()


def configure(snap: Snap) -> None:
    """Configure hook for the Slurm snap."""
    setup_logging(snap.paths.common / "hooks.log")
    logging.info("Executing snap `configure` hook.")
    options = snap.config.get_options(
        "munge", "slurm", "slurmd", "slurmdbd", "slurmrestd"
    ).as_dict()

    if "munged" in options:
        logging.info("updating the `munged` service's configuration")
        munged = Munged(snap)
        munged.update_config(options["munged"])

    if "slurmd" in options:
        logging.info("updating `slurmd` service configuration")
        slurmd = Slurmd(snap)
        slurmd.update_config(options["slurmd"])

    if "slurmrestd" in options:
        logging.info("updating `slurmrestd` service configuration")
        slurmrestd = Slurmrestd(snap)
        slurmrestd.update_config(options["slurmrestd"])
