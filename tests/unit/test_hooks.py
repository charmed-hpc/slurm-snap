#!/usr/bin/env python3
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

"""Test the Python-based hooks of the Slurm snap.

Current Python-based hooks include:
  - `install`
  - `configure`
"""

import os
import pathlib

from slurmhelpers import hooks

mock_logrotate_config = """
$SNAP_COMMON/var/log/slurm/*.log {
    weekly
    rotate 4
    size=5M
    create 640 slurm root
    missingok
    nocopytruncate
    nomail
    notifempty
    noolddir
    sharedscripts
    compress
    delaycompress
    compresscmd $SNAP/bin/bzip2
    compressext .bz2
    postrotate
        $SNAP/usr/bin/pkill -x --signal SIGUSR2 slurmctld
        $SNAP/usr/bin/pkill -x --signal SIGUSR2 slurmd
        $SNAP/usr/bin/pkill -x --signal SIGUSR2 slurmdbd
        exit 0
    endscript
}
""".strip()
target_logrotate_config = """
/var/snap/slurm/common/var/log/slurm/*.log {
    weekly
    rotate 4
    size=5M
    create 640 slurm root
    missingok
    nocopytruncate
    nomail
    notifempty
    noolddir
    sharedscripts
    compress
    delaycompress
    compresscmd /snap/slurm/x1/bin/bzip2
    compressext .bz2
    postrotate
        /snap/slurm/x1/usr/bin/pkill -x --signal SIGUSR2 slurmctld
        /snap/slurm/x1/usr/bin/pkill -x --signal SIGUSR2 slurmd
        /snap/slurm/x1/usr/bin/pkill -x --signal SIGUSR2 slurmdbd
        exit 0
    endscript
}
""".strip()


class TestHooks:
    """Test the hooks and relevant branches from slurmhelpers.hooks."""

    def test_install_hook(self, mocker, snap) -> None:
        """Test `install` hook."""
        mocker.patch("subprocess.check_output")
        mocker.patch("pathlib.Path.chmod")
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("pathlib.Path.touch")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch("pathlib.Path.write_text")
        mocker.patch("pathlib.Path.write_bytes")
        mocker.patch("dotenv.set_key")
        hooks.install(snap)

    def test_setup_logrotate(self, mocker, snap) -> None:
        """Test `_setup_logrotate` helper method."""
        mocker.patch("pathlib.Path.read_text", return_value=mock_logrotate_config)
        mocker.patch("pathlib.Path.write_text")
        os.environ["SNAP"] = "/snap/slurm/x1"
        os.environ["SNAP_COMMON"] = "/var/snap/slurm/common"

        # Assert that logrotate template was rendered correctly.
        hooks._setup_logrotate(snap)
        pathlib.Path.write_text.assert_called_once_with(target_logrotate_config)

    def test_configure_hook(self, mocker, snap) -> None:
        """Test `configure` hook."""
        mocker.patch("slurmhelpers.models.Munge.update_config")
        mocker.patch("slurmhelpers.models.Slurm.update_config")
        mocker.patch("slurmhelpers.models.Slurmd.update_config")
        mocker.patch("slurmhelpers.models.Slurmdbd.update_config")
        mocker.patch("slurmhelpers.models.Slurmrestd.update_config")
        hooks.configure(snap)

    def test_configure_hook_no_config(self, snap_empty_config) -> None:
        """Test `configure` when snap configuration is empty."""
        hooks.configure(snap_empty_config)
