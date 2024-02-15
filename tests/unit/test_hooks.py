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

from slurmhelpers import hooks


class TestHooks:
    """Test the hooks and relevant branches from slurmhelpers.hooks."""

    def test_install_hook(self, mocker, snap) -> None:
        """Test `install` hook."""
        mocker.patch("pathlib.Path.chmod")
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("pathlib.Path.touch")
        mocker.patch("pathlib.Path.write_bytes")
        mocker.patch("dotenv.set_key")
        hooks.install(snap)

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
