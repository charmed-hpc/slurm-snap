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

FORMAT_BOLD = \033[1m
FORMAT_YELLOW = \033[0;33m
FORMAT_BLUE = \033[0;34m
FORMAT_END = \033[0m

##@ Build

.PHONY: snap
snap: ## Build Slurm snap package
	@snapcraft -v pack

##@ Test

define INTEGRATION_TESTS
	integration-configless
endef

.PHONY: integration
integration: $(INTEGRATION_TESTS) ## Run Slurm integration tests with gambol

.PHONY: check-snap-exists
check-snap-exists:
	@[ -f slurm_*.snap ] || \
		{ echo "slurm snap must be built before this test can run" && exit 1; }

.PHONY: integration-configless
integration-configless: check-snap-exists
	@awk 'BEGIN {\
		printf "running integration test: ${FORMAT_BOLD}configless slurm${FORMAT_END}\n" } '
	@cp slurm_*.snap tests/integration/configless-slurm/testdata/slurm.snap
	cd tests/integration/configless-slurm && gambol -v run configless-slurm.yaml
	@rm -f tests/integration/configless-slurm/testdata/slurm_*.snap/slurm.snap

##@ Clean

.PHONY: clean
clean: ## Clean up build environment
	snapcraft -v clean

.PHONY: help
help:
	@awk 'BEGIN {\
		FS = ":.*##"; \
		printf                "Usage: ${FORMAT_BLUE}OPTION${FORMAT_END}=<value> make ${FORMAT_YELLOW}<target>${FORMAT_END}\n"\
		} \
		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  ${FORMAT_BLUE}%-46s${FORMAT_END} %s\n", $$1, $$2 } \
		/^.?.?##~/              { printf "   %-46s${FORMAT_YELLOW}%-46s${FORMAT_END}\n", "", substr($$1, 6) } \
		/^##@/                  { printf "\n${FORMAT_BOLD}%s${FORMAT_END}\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

