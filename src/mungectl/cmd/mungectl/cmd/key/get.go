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

const getHelp = "Get the current munge key"
const getExample = `
mungectl key get > key.out

	Get current munge key, encode into a base64 string, and write to key.out.
`

var getCmd = &cobra.Command{
	Use:     "get",
	Short:   getHelp,
	Example: getExample,
	Run:     getExecute,
}

func getExecute(cmd *cobra.Command, args []string) {
	file := path.Join(os.Getenv("SNAP_COMMON"), "etc", "munge", "munge.key")
	content, err := key.Read(file)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to read current munge key file %s\n", file)
		os.Exit(1)
	}

	fmt.Fprintln(os.Stdout, key.Encode(content))
}
