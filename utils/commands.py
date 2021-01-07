import logging
import os
import subprocess
from typing import Tuple

log = logging.getLogger(__name__)


def run_command(command: str, **environment) -> Tuple[bool, str]:
    """
    Execute the command, and log the result.

    Any additional keyword arguments passed into this call
    will be added as environment variables.

    Returns a tuple of (success, output), where success is a boolean value
    that is either True or False, and output is a string.
    """
    # Get the current environment variables.
    env = os.environ.copy()

    # Now add all the environment variables we passed in that are not None.
    extra_env = {key: value for key, value in environment.items() if value is not None}
    env.update(extra_env)

    # Run the command and capture the output
    try:
        result = subprocess.run(
            [command],
            shell=True,
            capture_output=True,
            env=env,
            check=True
        )
        output = result.stderr.decode("utf-8").strip()
        success = True
    except subprocess.CalledProcessError as e:
        output = e.stderr.decode("utf-8").strip()
        success = False

    # Log and return output
    log.info(output)
    return success, output
