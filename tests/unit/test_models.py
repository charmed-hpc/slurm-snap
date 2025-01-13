#!/usr/bin/env python3
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

"""Test models that wrap the configuration for the bundled daemons."""

import subprocess

import pytest


class TestBaseModel:
    """Test the `_BaseModel` parent class for data models."""

    def test_needs_restart(self, base_model) -> None:
        """The `_needs_restart` method."""
        # Test when service is inactive.
        base_model._needs_restart(["test"])


class TestMungedModel:
    """Test the `Munged` data model."""

    def test_max_thread_count(self, mocker, munged) -> None:
        """Test `max_thread_count` attribute."""
        # MUNGED_MAX_THREAD_COUNT does not exist in .env file.
        mocker.patch("dotenv.get_key", return_value=None)
        assert munged.max_thread_count is None

        # MUNGED_MAX_THREAD_COUNT exists in .env file.
        mocker.patch("dotenv.get_key", return_value=16)
        assert munged.max_thread_count == 16

        # New MUNGED_MAX_THREAD_COUNT is equivalent to old value.
        mocker.patch("dotenv.get_key", return_value=16)
        munged.max_thread_count = 16

        # Set new MUNGED_MAX_THREAD_COUNT value.
        mocker.patch("dotenv.set_key")
        mocker.patch("dotenv.get_key", return_value=16)
        munged.max_thread_count = 8

    def test_generate_key(self, mocker, munged) -> None:
        """Test `generate_key` method."""
        # Generate key when `munge.key` file does not yet exist.
        mocker.patch("subprocess.check_output")
        munged.generate_key()

        # Fail to generate new `munge.key`.
        mocker.patch(
            "subprocess.check_output",
            side_effect=subprocess.CalledProcessError(0, ["mungectl", "key", "generate"]),
        )
        with pytest.raises(subprocess.CalledProcessError):
            munged.generate_key()

    def test_update_config(self, mocker, munged) -> None:
        """Test `update_config` method."""
        # Set `munged` daemon configuration but a bad option is included.
        mocker.patch("slurmhelpers.models.Munged.max_thread_count")
        with pytest.raises(AttributeError):
            munged.update_config({"max-thread-count": 24, "awgeez": "rick"})

        # Set `munged` daemon configuration with only good options included.
        mocker.patch("slurmhelpers.models.Munged.max_thread_count")
        munged.update_config({"max-thread-count": 24})


class TestSlurmdModel:
    """Test the `Slurmd` data model."""

    def test_config_server(self, mocker, slurmd) -> None:
        """Test `config_server` property."""
        # SLURMD_CONFIG_SERVER does not exist in .env file.
        assert slurmd.config_server is None

        # SLURMD_CONFIG_SERVER exists in .env file.
        mocker.patch("dotenv.get_key", return_value="localhost:6820")
        assert slurmd.config_server == "localhost:6820"

        # New SLURMD_CONFIG_SERVER is equivalent to old value.
        mocker.patch("dotenv.get_key", return_value="localhost:6820")
        slurmd.config_server = "localhost:6820"

    def test_update_config(self, mocker, slurmd) -> None:
        """Test `update_config` method."""
        # Set `slurmd` daemon configuration but a bad option is included.
        mocker.patch("slurmhelpers.models.Slurmd.config_server")
        with pytest.raises(AttributeError):
            slurmd.update_config({"config-server": "localhost:6820", "awgeez": "rick"})

        # Set `slurmd` daemon configuration with only good options included.
        mocker.patch("slurmhelpers.models.Slurmd.config_server")
        slurmd.update_config({"config-server": "localhost:6820"})


class TestSlurmrestdModel:
    """Test the `Slurmrestd` data model."""

    def test_max_connections(self, mocker, slurmrestd) -> None:
        """Test `max_connections` property."""
        # SLURMRESTD_MAX_CONNECTIONS does not exist in .env file.
        mocker.patch("dotenv.get_key", return_value=None)
        assert slurmrestd.max_connections is None

        # SLURMRESTD_MAX_CONNECTIONS exists in .env file.
        mocker.patch("dotenv.get_key", return_value=16)
        assert slurmrestd.max_connections == 16

        # New SLURMRESTD_MAX_CONNECTIONS is equivalent to old value.
        mocker.patch("dotenv.get_key", return_value=16)
        slurmrestd.max_connections = 16

        # Set new SLURMRESTD_MAX_CONNECTIONS value.
        mocker.patch("dotenv.set_key")
        mocker.patch("dotenv.get_key", return_value=16)
        slurmrestd.max_connections = 8

    def test_max_thread_count(self, mocker, slurmrestd) -> None:
        """Test `max_thread_count` property."""
        # SLURMRESTD_MAX_THREAD_COUNT does not exist in .env file.
        mocker.patch("dotenv.get_key", return_value=None)
        assert slurmrestd.max_thread_count is None

        # SLURMRESTD_MAX_THREAD_COUNT exists in .env file.
        mocker.patch("dotenv.get_key", return_value=16)
        assert slurmrestd.max_thread_count == 16

        # New SLURMRESTD_MAX_THREAD_COUNT is equivalent to old value.
        mocker.patch("dotenv.get_key", return_value=16)
        slurmrestd.max_thread_count = 16

        # Set new SLURMRESTD_MAX_THREAD_COUNT value.
        mocker.patch("dotenv.set_key")
        mocker.patch("dotenv.get_key", return_value=16)
        slurmrestd.max_thread_count = 8

    def test_update_config(self, mocker, slurmrestd) -> None:
        """Test `update_config` method."""
        # Set `slurmrestd` daemon configuration but a bad option is included.
        mocker.patch("slurmhelpers.models.Slurmrestd.max_connections")
        mocker.patch("slurmhelpers.models.Slurmrestd.max_thread_count")
        with pytest.raises(AttributeError):
            slurmrestd.update_config(
                {"max-connections": 24, "max-thread-count": 24, "awgeez": "rick"}
            )

        # Set `slurmrestd` daemon configuration with only good options included.
        mocker.patch("slurmhelpers.models.Slurmrestd.max_connections")
        mocker.patch("slurmhelpers.models.Slurmrestd.max_thread_count")
        slurmrestd.update_config({"max-connections": 24, "max-thread-count": 24})
