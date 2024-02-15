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

"""Test models that wrap the configuration for the bundled daemons."""

import pytest
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
    SlurmConfig,
    SlurmdbdConfig,
)

from slurmhelpers.models import (
    _process_down_nodes,
    _process_frontend_nodes,
    _process_node_sets,
    _process_nodes,
    _process_partitions,
)


class TestBaseModel:
    """Test the `_BaseModel` parent class for data models."""

    def test_needs_restart(self, base_model) -> None:
        """The `_needs_restart` method."""
        # Test when service is inactive.
        base_model._needs_restart(["test"])


class TestMungeModel:
    """Test the `Munge` data model."""

    def test_key(self, mocker, munge) -> None:
        """Test `key` attribute."""
        # `munge.key` does not exist after snap installation.
        mocker.patch("pathlib.Path.exists", return_value=False)
        assert munge.key is None

        # Set `munge.key` if it has not been created yet (or deleted!)
        mocker.patch("pathlib.Path.exists", return_value=False)
        mocker.patch("pathlib.Path.touch")
        mocker.patch("pathlib.Path.write_bytes")
        munge.key = "qI06pi2vDnZZbuAA54fIfhtxQnRYdYhMhRPBDtCVAPTlS1BhcWXNf70KHNsi7tLQXfcQIVy+8MKXEewdisFuYYDcLeiBaiHHRQn84RYmeUi+kqK8hcitd9wIrTROxE/ZA+RMAgJkkH/raV8e9Z7IYLZ1DDMuGHv5pkdQRlfphK4="

        # Set `munge.key`, but the munge.key file has already been created.
        mocker.patch("pathlib.Path.exists", return_value=True)
        mocker.patch("pathlib.Path.write_bytes")
        mocker.patch(
            "pathlib.Path.read_bytes",
            return_value=b'\xa7\x8d:\xa6-\xaf\x0evYn\xe0\x00\xe7\x87\xc8~\x1bqBtXu\x88L\x85\x13\xc1\x0e\xd0\x95\x00\xf4\xe5KPaqe\xcd\x7f\xbd\n\x1c\xdb"\xee\xd2\xd0]\xf7\x10!\\\xbe\xf0\xc2\x97\x11\xec\x1d\x8a\xc1na\x80\xdc-\xe8\x81j!\xc7E\t\xfc\xe1\x16&yH\xbe\x92\xa2\xbc\x85\xc8\xadw\xdc\x08\xad4N\xc4O\xd9\x03\xe4L\x02\x02d\x90\x7f\xebi_\x1e\xf5\x9e\xc8`\xb6u\x0c3.\x18{\xf9\xa6GPFW\xe9\x84\xae',
        )
        munge.key = "qI06pi2vDnZZbuAA54fIfhtxQnRYdYhMhRPBDtCVAPTlS1BhcWXNf70KHNsi7tLQXfcQIVy+8MKXEewdisFuYYDcLeiBaiHHRQn84RYmeUi+kqK8hcitd9wIrTROxE/ZA+RMAgJkkH/raV8e9Z7IYLZ1DDMuGHv5pkdQRlfphK4="

        # Get `munge.key` value if it exists.
        mocker.patch("pathlib.Path.exists", return_value=True)
        mocker.patch(
            "pathlib.Path.read_bytes",
            return_value=b'\xa8\x8d:\xa6-\xaf\x0evYn\xe0\x00\xe7\x87\xc8~\x1bqBtXu\x88L\x85\x13\xc1\x0e\xd0\x95\x00\xf4\xe5KPaqe\xcd\x7f\xbd\n\x1c\xdb"\xee\xd2\xd0]\xf7\x10!\\\xbe\xf0\xc2\x97\x11\xec\x1d\x8a\xc1na\x80\xdc-\xe8\x81j!\xc7E\t\xfc\xe1\x16&yH\xbe\x92\xa2\xbc\x85\xc8\xadw\xdc\x08\xad4N\xc4O\xd9\x03\xe4L\x02\x02d\x90\x7f\xebi_\x1e\xf5\x9e\xc8`\xb6u\x0c3.\x18{\xf9\xa6GPFW\xe9\x84\xae',
        )
        assert (
            munge.key
            == "qI06pi2vDnZZbuAA54fIfhtxQnRYdYhMhRPBDtCVAPTlS1BhcWXNf70KHNsi7tLQXfcQIVy+8MKXEewdisFuYYDcLeiBaiHHRQn84RYmeUi+kqK8hcitd9wIrTROxE/ZA+RMAgJkkH/raV8e9Z7IYLZ1DDMuGHv5pkdQRlfphK4="
        )

        # Set new `munge.key` value, but it is equivalent to the original `munge.key`.
        mocker.patch("pathlib.Path.exists", return_value=True)
        mocker.patch(
            "pathlib.Path.read_bytes",
            return_value=b'\xa8\x8d:\xa6-\xaf\x0evYn\xe0\x00\xe7\x87\xc8~\x1bqBtXu\x88L\x85\x13\xc1\x0e\xd0\x95\x00\xf4\xe5KPaqe\xcd\x7f\xbd\n\x1c\xdb"\xee\xd2\xd0]\xf7\x10!\\\xbe\xf0\xc2\x97\x11\xec\x1d\x8a\xc1na\x80\xdc-\xe8\x81j!\xc7E\t\xfc\xe1\x16&yH\xbe\x92\xa2\xbc\x85\xc8\xadw\xdc\x08\xad4N\xc4O\xd9\x03\xe4L\x02\x02d\x90\x7f\xebi_\x1e\xf5\x9e\xc8`\xb6u\x0c3.\x18{\xf9\xa6GPFW\xe9\x84\xae',
        )
        munge.key = "qI06pi2vDnZZbuAA54fIfhtxQnRYdYhMhRPBDtCVAPTlS1BhcWXNf70KHNsi7tLQXfcQIVy+8MKXEewdisFuYYDcLeiBaiHHRQn84RYmeUi+kqK8hcitd9wIrTROxE/ZA+RMAgJkkH/raV8e9Z7IYLZ1DDMuGHv5pkdQRlfphK4="

    def test_max_thread_count(self, mocker, munge) -> None:
        """Test `max_thread_count` attribute."""
        # MUNGED_MAX_THREAD_COUNT does not exist in .env file.
        mocker.patch("dotenv.get_key", return_value=None)
        assert munge.max_thread_count is None

        # MUNGED_MAX_THREAD_COUNT exists in .env file.
        mocker.patch("dotenv.get_key", return_value=16)
        assert munge.max_thread_count == 16

        # New MUNGED_MAX_THREAD_COUNT is equivalent to old value.
        mocker.patch("dotenv.get_key", return_value=16)
        munge.max_thread_count = 16

        # Set new MUNGED_MAX_THREAD_COUNT value.
        mocker.patch("dotenv.set_key")
        mocker.patch("dotenv.get_key", return_value=16)
        munge.max_thread_count = 8

    def test_generate_key(self, mocker, munge) -> None:
        """Test `generate_key` method."""
        # Generate key when `munge.key` file does not yet exist.
        mocker.patch("pathlib.Path.exists", return_value=False)
        mocker.patch("pathlib.Path.touch")
        mocker.patch("pathlib.Path.write_bytes")
        munge.generate_key()

        # Generate key when `munge.key` file exists.
        mocker.patch("pathlib.Path.exists", return_value=True)
        mocker.patch("pathlib.Path.write_bytes")
        munge.generate_key()

    def test_update_config(self, mocker, munge) -> None:
        """Test `update_config` method."""
        # Set `munged` daemon configuration but a bad option is included.
        mocker.patch("slurmhelpers.models.Munge.key")
        mocker.patch("slurmhelpers.models.Munge.max_thread_count")
        with pytest.raises(AttributeError):
            munge.update_config({"key": "supersecret", "max-thread-count": 24, "awgeez": "rick"})

        # Set `munged` daemon configuration with only good options included.
        mocker.patch("slurmhelpers.models.Munge.key")
        mocker.patch("slurmhelpers.models.Munge.max_thread_count")
        munge.update_config({"key": "supersecret", "max-thread-count": 24})


class TestSlurmModel:
    """Test the `Slurm` data model."""

    def test_update_config(self, mocker, slurm) -> None:
        """Test `update_config` method."""
        nodes = NodeMap()
        frontend_nodes = FrontendNodeMap()
        down_nodes = DownNodesList()
        node_sets = NodeSetMap()
        partitions = PartitionMap()
        config = SlurmConfig()
        config.include = ["/etc/infiniband.conf", "/etc/nvgpu.conf"]
        config.slurmctld_host = ["control0(12.34.56.78)", "control1(12.34.56.79)"]
        config.tmp_fs = "/tmp/slurm"
        config.nodes = nodes
        config.frontend_nodes = frontend_nodes
        config.down_nodes = down_nodes
        config.node_sets = node_sets
        config.partitions = partitions

        # Test when there has been no change to slurm configuration.
        mocker.patch("slurmutils.editors.slurmconfig.load", return_value=config)
        mocker.patch("slurmutils.editors.slurmconfig.dump")
        mocker.patch("slurmhelpers.models._process_nodes", return_value=nodes)
        mocker.patch("slurmhelpers.models._process_frontend_nodes", return_value=frontend_nodes)
        mocker.patch("slurmhelpers.models._process_down_nodes", return_value=down_nodes)
        mocker.patch("slurmhelpers.models._process_node_sets", return_value=node_sets)
        mocker.patch("slurmhelpers.models._process_partitions", return_value=partitions)
        slurm.update_config(
            {
                "include": "/etc/infiniband.conf,/etc/nvgpu.conf",
                "slurmctld-host": "control0(12.34.56.78),control1(12.34.56.79)",
                "tmp-fs": "/tmp/slurm",
                "nodes": {},
                "frontend-nodes": {},
                "down-nodes": {},
                "node-sets": {},
                "partitions": {},
            }
        )

        # Test when there has been a change made to the slurm configuration.
        mocker.patch("slurmutils.editors.slurmconfig.load", return_value=config)
        mocker.patch("slurmutils.editors.slurmconfig.dump")
        mocker.patch("slurmhelpers.models._process_nodes", return_value=nodes)
        mocker.patch("slurmhelpers.models._process_frontend_nodes", return_value=frontend_nodes)
        mocker.patch("slurmhelpers.models._process_down_nodes", return_value=down_nodes)
        mocker.patch("slurmhelpers.models._process_node_sets", return_value=node_sets)
        mocker.patch("slurmhelpers.models._process_partitions", return_value=partitions)
        slurm.update_config(
            {
                "include": "/etc/infiniband.conf,/etc/nvgpu.conf",
                "slurmctld-host": "control0(12.34.56.78),control1(12.34.56.79)",
                "tmp-fs": "/var/tmp/slurm",
                "nodes": {},
                "frontend-nodes": {},
                "down-nodes": {},
                "node-sets": {},
                "partitions": {},
            }
        )

        # Test when a bad slurmdbd configuration option has been provided.
        mocker.patch("slurmutils.editors.slurmconfig.load", return_value=config)
        mocker.patch("slurmutils.editors.slurmconfig.dump")
        mocker.patch("slurmhelpers.models._process_nodes", return_value=nodes)
        mocker.patch("slurmhelpers.models._process_frontend_nodes", return_value=frontend_nodes)
        mocker.patch("slurmhelpers.models._process_down_nodes", return_value=down_nodes)
        mocker.patch("slurmhelpers.models._process_node_sets", return_value=node_sets)
        mocker.patch("slurmhelpers.models._process_partitions", return_value=partitions)
        with pytest.raises(AttributeError):
            slurm.update_config(
                {
                    "include": "/etc/infiniband.conf,/etc/nvgpu.conf",
                    "slurmctld-host": "control0(12.34.56.78),control1(12.34.56.79)",
                    "tmp-fs": "/var/tmp/slurm",
                    "nodes": {},
                    "frontend-nodes": {},
                    "down-nodes": {},
                    "node-sets": {},
                    "partitions": {},
                    "awgeez": "rick",
                }
            )

    def test_process_nodes(self) -> None:
        """Test `_process_nodes` function."""
        node_map = NodeMap()
        node = Node(NodeName="batch0")
        node.node_addr = "12.23.45.78"
        node.cpus = 64
        node.procs = 128
        node.real_memory = 100000
        node.state = "UP"
        node_map[node.node_name] = node

        # Test with clean `Node` configuration.
        holder = _process_nodes(
            {
                "batch0": {
                    "node-addr": "12.23.45.78",
                    "cpus": 64,
                    "procs": 128,
                    "real-memory": 100000,
                    "state": "UP",
                }
            }
        )
        assert node_map["batch0"].dict() == holder["batch0"].dict()

        # Test with invalid `Node` configuration.
        with pytest.raises(AttributeError):
            _process_nodes(
                {
                    "batch0": {
                        "node-addr": "12.23.45.78",
                        "cpus": 64,
                        "procs": 128,
                        "real-memory": 100000,
                        "state": "UP",
                        "awgeez": "rick",
                    }
                }
            )

    def test_process_frontend_nodes(self) -> None:
        """Test `_process_frontend_nodes` function."""
        node_map = FrontendNodeMap()
        node = FrontendNode(FrontendName="frontend0")
        node.frontend_addr = "12.23.45.78"
        node.reason = "Upgrading desktop environment"
        node.state = "DOWN"
        node_map[node.frontend_name] = node

        # Test with clean `FrontendNode` configuration.
        holder = _process_frontend_nodes(
            {
                "frontend0": {
                    "frontend-addr": "12.23.45.78",
                    "state": "DOWN",
                    "reason": "Upgrading desktop environment",
                }
            }
        )
        assert node_map["frontend0"].dict() == holder["frontend0"].dict()

        # Test with invalid `FrontendNode` configuration.
        with pytest.raises(AttributeError):
            _process_frontend_nodes(
                {
                    "frontend0": {
                        "frontend-addr": "12.23.45.78",
                        "state": "DOWN",
                        "reason": "Upgrading desktop environment",
                        "awgeez": "rick",
                    }
                }
            )

    def test_process_down_nodes(self) -> None:
        """Test `process_down_nodes` function."""
        down_nodes = DownNodesList()
        down_node = DownNodes()
        down_node.down_nodes = ["batch1"]
        down_node.state = "FAIL"
        down_node.reason = "Power failure"
        down_nodes.append(down_node)

        # Test with clean `DownNodes` configuration.
        holder = _process_down_nodes(
            {"nodes": "batch1", "state": "FAIL", "reason": "Power failure"}
        )
        assert down_nodes.data == holder.data

        # Test with invalid `DownNodes` configuration.
        with pytest.raises(AttributeError):
            _process_down_nodes(
                {"nodes": "batch1", "state": "FAIL", "reason": "Power failure", "awgeez": "rick"}
            )

    def test_process_node_sets(self) -> None:
        """Test `_process_node_sets` function."""
        node_sets = NodeSetMap()
        node_set = NodeSet(NodeSet="nvgpu")
        node_set.nodes = ["batch0"]
        node_set.feature = "nvgpu"
        node_sets[node_set.node_set] = node_set

        # Test with clean `NodeSet` configuration.
        holder = _process_node_sets({"nvgpu": {"nodes": "batch0", "feature": "nvgpu"}})
        assert node_sets["nvgpu"].dict() == holder["nvgpu"].dict()

        # Test with invalid `NodeSet` configuration.
        with pytest.raises(AttributeError):
            _process_node_sets(
                {"nvgpu": {"nodes": "batch0", "feature": "nvgpu", "awgeez": "rick"}}
            )

    def test_process_partitions(self) -> None:
        """Test `_process_partitions` function."""
        partition_map = PartitionMap()
        partition = Partition(PartitionName="part0")
        partition.nodes = ["batch0"]
        partition.state = "UP"
        partition.max_mem_per_cpu = 1000
        partition.allow_accounts = ["morty"]
        partition_map[partition.partition_name] = partition

        # Test with clean `Partition` configuration.
        holder = _process_partitions(
            {
                "part0": {
                    "nodes": "batch0",
                    "state": "UP",
                    "max-mem-per-cpu": 1000,
                    "allow-accounts": "morty",
                }
            }
        )
        assert partition_map["part0"].dict() == holder["part0"].dict()

        # Test with invalid `Partition` configuration.
        with pytest.raises(AttributeError):
            _process_partitions(
                {
                    "part0": {
                        "nodes": "batch0",
                        "state": "UP",
                        "max-mem-per-cpu": 1000,
                        "allow-accounts": "morty",
                        "awgeez": "rick",
                    }
                }
            )


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


class TestSlurmdbdModel:
    """Test the `Slurmdbd` data model."""

    def test_update_config(self, mocker, slurmdbd) -> None:
        """Test `update_config` method."""
        config = SlurmdbdConfig()
        config.log_file = "/var/log/slurm/slurmdbd.log"
        config.private_data = ["accounts", "events", "jobs"]
        config.track_slurmctld_down = "no"

        # Test when there has been no change to slurmdbd configuration.
        mocker.patch("slurmutils.editors.slurmdbdconfig.load", return_value=config)
        mocker.patch("slurmutils.editors.slurmdbdconfig.dump")
        slurmdbd.update_config(
            {
                "log-file": "/var/log/slurm/slurmdbd.log",
                "private-data": "accounts,events,jobs",
                "track-slurmctld-down": "no",
            }
        )

        # Test when there has been a change to the slurmdbd configuration.
        mocker.patch("slurmutils.editors.slurmdbdconfig.load", return_value=config)
        mocker.patch("slurmutils.editors.slurmdbdconfig.dump")
        slurmdbd.update_config(
            {
                "log-file": "/var/log/slurm/slurmdbd.log",
                "private-data": "accounts,events,jobs",
                "track-slurmctld-down": "yes",
            }
        )

        # Test when a bad slurmdbd configuration option has been provided.
        mocker.patch("slurmutils.editors.slurmdbdconfig.load", return_value=config)
        mocker.patch("slurmutils.editors.slurmdbdconfig.dump")
        with pytest.raises(AttributeError):
            slurmdbd.update_config(
                {
                    "log-file": "/var/log/slurm/slurmdbd.log",
                    "private-data": "accounts,events,jobs",
                    "track-slurmctld-down": "yes",
                    "awgeez": "rick",
                }
            )


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
