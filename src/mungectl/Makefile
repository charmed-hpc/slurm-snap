# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

FORMAT_BOLD = \033[1m
FORMAT_YELLOW = \033[0;33m
FORMAT_BLUE = \033[0;34m
FORMAT_END = \033[0m

##@ Lint

.PHONY: fmt
fmt: ## Format `mungectl` source code
	@go fmt -x ./...
	@golangci-lint run --fix

.PHONY: lint
lint: ## Lint `mungectl` source code
	@golangci-lint run

##@ Test

.PHONY: unit
unit: ## Run `mungectl` unit tests
	@go test -v ./...


.PHONY: help
help:
	@awk 'BEGIN {\
		FS = ":.*##"; \
		printf                "Usage: ${FORMAT_BLUE}OPTION${FORMAT_END}=<value> make ${FORMAT_YELLOW}<target>${FORMAT_END}\n"\
		} \
		/^[a-zA-Z0-9_-]+:.*?##/ { printf "  ${FORMAT_BLUE}%-46s${FORMAT_END} %s\n", $$1, $$2 } \
		/^.?.?##~/              { printf "   %-46s${FORMAT_YELLOW}%-46s${FORMAT_END}\n", "", substr($$1, 6) } \
		/^##@/                  { printf "\n${FORMAT_BOLD}%s${FORMAT_END}\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
