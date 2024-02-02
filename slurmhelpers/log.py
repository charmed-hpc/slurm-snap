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

"""Configure logging for the Slurm snap Python utility functions."""

import logging
from functools import wraps
from os import PathLike
from typing import Union


def log(file: Union[str, PathLike]):
    """Set up logging for a Slurm snap utility function.

    Args:
        file: The file to record logging information.
    """

    def decorator(func):
        logging.basicConfig(
            filename=str(file),
            filemode="a",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator
