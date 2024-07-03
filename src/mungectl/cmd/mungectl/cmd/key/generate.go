// Copyright 2024 Canonical Ltd.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

package key

import (
	"fmt"
	"os"
	"path"

	"github.com/spf13/cobra"

	key "mungectl/internal/key"
)

const generateHelp = "Generate a new munge key"
const generateExample = `mungectl generate
	Generate a new munge key and write to key file location
`

var generateCmd = &cobra.Command{
	Use:     "generate",
	Short:   generateHelp,
	Example: generateExample,
	Run:     generateExecute,
}

func generateExecute(cmd *cobra.Command, args []string) {
	content, err := key.Generate()
	if err != nil {
		fmt.Fprintln(os.Stderr, "failed to generate new munge key")
		os.Exit(1)
	}

	file := path.Join(os.Getenv("SNAP_COMMON"), "etc", "munge", "munge.key")
	if err := key.Write(file, content); err != nil {
		fmt.Fprintf(os.Stderr, "failed to write generated munge key file %s\n", file)
	}
}
