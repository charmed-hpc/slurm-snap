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

"""Configure unit tests."""

from unittest.mock import MagicMock

import pytest
from snaphelpers import Snap, SnapConfig, SnapConfigOptions, SnapServices


@pytest.fixture
def env():
    """Mock the snap runtime environment."""
    yield {
        "SNAP": "/snap/slurm/1",
        "SNAP_COMMON": "/var/snap/slurm/common",
        "SNAP_DATA": "/var/snap/slurm/1",
        "SNAP_INSTANCE_NAME": "",
        "SNAP_NAME": "slurm",
        "SNAP_REVISION": "2",
        "SNAP_USER_COMMON": "",
        "SNAP_USER_DATA": "",
        "SNAP_VERSION": "23.11.1",
        "SNAP_REAL_HOME": "/home/ubuntu",
    }


@pytest.fixture
def snap(env):
    """Create a mock `Snap` object with configuration preloaded."""
    snap = Snap(environ=env)
    config_options = MagicMock(SnapConfigOptions)
    config_options.as_dict.return_value = {
        "munge": {},
        "slurm": {},
        "slurmd": {},
        "slurmdbd": {},
        "slurmrestd": {},
    }
    config = MagicMock(SnapConfig)
    config.get_options.return_value = config_options
    snap.config = config
    snap.services = MagicMock(SnapServices)
    yield snap


@pytest.fixture
def snap_empty_config(env):
    """Create a mock `Snap` object with empty configuration."""
    snap = Snap(environ=env)
    snap.config = MagicMock(SnapConfig)
    snap.services = MagicMock(SnapServices)
    yield snap
