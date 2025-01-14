# Copyright 2025 Canonical Ltd.
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

# Check if the Slurm snap exists before running a recipe.
_check_snap_exists:
    @[ -f slurm_*.snap ] || \
        { echo "Slurm snap must be built for this recipe to run. Run \`just snap\` to build snap". \
        && exit 1; }

# Build snap
snap:
    snapcraft -v pack

# Apply coding style standards to project
fmt:
    tox run -e fmt

# Check project against coding style standards
lint:
    tox run -e lint

# Run unit tests
unit:
    tox run -e unit

# Run integration tests
integration: _check_snap_exists
    #!/usr/bin/env bash
    cp slurm_*.snap tests/integration/configless-slurm/testdata/slurm.snap
    pushd tests/integration/configless-slurm
    gambol -v run configless-slurm.yaml
    popd && rm -f tests/integration/configless-slurm/testdata/slurm.snap

# Clean up project directory
clean:
    snapcraft -v clean

# Show available recipes
help:
    @just --list --unsorted
