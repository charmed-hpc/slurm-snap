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
	"bufio"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"os"
	"strings"
)

// Scan new munge key from stdin. Returns an error if
// no base64-encoded munge key is provided on stdin.
func Scan() (string, error) {
	stat, _ := os.Stdin.Stat()
	if (stat.Mode() & os.ModeCharDevice) == 0 {
		key := strings.Builder{}
		scanner := bufio.NewScanner(os.Stdin)

		for scanner.Scan() {
			key.WriteString(scanner.Text())
		}
		if err := scanner.Err(); err != nil {
			return "", err
		}

		return strings.TrimSpace(key.String()), nil
	}

	return "", errors.New("no munge key provided on stdin")
}

// Generate a new munge key. Returns an error if a failure
// is encountered when generating new bytes for key.
func Generate() ([]byte, error) {
	b := make([]byte, 1024)
	if _, err := rand.Read(b); err != nil {
		return nil, err
	}
	return b, nil
}

// Read munge key file. Returns an error if the munge key file
// does not exist or a failure occurs when reading the file.
func Read(path string) ([]byte, error) {
	key, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return key, nil
}

// Write munge key file. Returns an error if a failure
// occurs when writing the new key.
func Write(path string, key []byte) error {
	return os.WriteFile(path, key, 0600)
}

// Encode munge key into a base64 string.
func Encode(key []byte) string {
	return base64.StdEncoding.EncodeToString(key)
}

// Decode munge key from a base64 string. Returns an error
// if a failure occurs when decoding the base64 string.
func Decode(key string) ([]byte, error) {
	key = strings.TrimSpace(key)
	decoded, err := base64.StdEncoding.DecodeString(key)
	if err != nil {
		return nil, err
	}
	return decoded, nil
}
