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
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

const secret = "we be testing"
const secretBase64 = "d2UgYmUgdGVzdGluZw=="

func TestKeyScan(t *testing.T) {
	// send mock input into stdin
	r, w, err := os.Pipe()
	if err != nil {
		t.Error(err)
	}
	if _, err := w.Write([]byte(secretBase64)); err != nil {
		t.Error(err)
	}
	w.Close()

	// restore stdin after test
	defer func(f *os.File) { os.Stdin = f }(os.Stdin)
	os.Stdin = r

	content, err := Scan()
	if assert.NoError(t, err) {
		assert.Equal(t, secretBase64, content)
	}
}

func TestKeyGenerate(t *testing.T) {
	content, err := Generate()
	if assert.NoError(t, err) {
		assert.NotNil(t, content)
	}
}

func TestKeyWrite(t *testing.T) {
	f, err := os.CreateTemp("", "munge")
	if err != nil {
		t.Error(err)
	}
	defer f.Close()
	defer os.Remove(f.Name())
	assert.NoError(t, Write(f.Name(), []byte(secret)))
}

func TestKeyRead(t *testing.T) {
	f, err := os.CreateTemp("", "munge")
	if err != nil {
		t.Error(err)
	}
	defer os.Remove(f.Name())
	if _, err := f.Write([]byte(secret)); err != nil {
		t.Error(err)
	}
	f.Close()

	content, err := Read(f.Name())
	if assert.NoError(t, err) {
		assert.Equal(t, secret, string(content))
	}
}

func TestKeyEncode(t *testing.T) {
	content := Encode([]byte(secret))
	assert.Equal(t, secretBase64, content)
}

func TestKeyDecode(t *testing.T) {
	content, err := Decode(secretBase64)
	if assert.NoError(t, err) {
		assert.Equal(t, secret, string(content))
	}
}
