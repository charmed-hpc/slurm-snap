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

const setHelp = "Set a new munge key"
const setExample = `
mungectl key set < secret.key

	Replace old munge key with one read from stdin
`

var setCmd = &cobra.Command{
	Use:     "set",
	Short:   setHelp,
	Example: setExample,
	Run:     setExecute,
}

func setExecute(cmd *cobra.Command, args []string) {
	content, err := key.Scan()
	if err != nil {
		fmt.Fprintln(os.Stderr, "failed to read munge key from stdin")
		os.Exit(2)
	}

	file := path.Join(os.Getenv("SNAP_COMMON"), "etc", "munge", "munge.key")
	decoded, err := key.Decode(content)
	if err != nil {
		fmt.Fprintln(os.Stderr, "failed to decode new munge key")
		os.Exit(1)
	}
	if err := key.Write(file, decoded); err != nil {
		fmt.Fprintf(os.Stderr, "failed to write new munge key to %s\n", file)
		os.Exit(1)
	}
}
