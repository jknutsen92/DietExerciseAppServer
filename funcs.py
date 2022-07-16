from datetime   import datetime
from pathlib    import Path

import re
import os
import shutil


EXTERNAL_CONFIG_NAME        = "databases.config"
PREV_SYS_REGEX              = re.compile(r"^prev_sys=([\w]+)$")


def load_db_from_external_cache(system: str, local_path: str, external_path:str, db_name:str) -> None:
    if os.path.exists(f"{external_path}{EXTERNAL_CONFIG_NAME}"):
        with open(f"{external_path}{EXTERNAL_CONFIG_NAME}") as config:
            values = ''.join(config.readlines())
            prev_sys = PREV_SYS_REGEX.match(values).group(1)
    else:                                                           # If config file does not exist, but the
        if os.path.exists(f"{external_path}{db_name}"):             # external db file does, we have a problem.
            raise IOError(f"{EXTERNAL_CONFIG_NAME} file missing, please investigate database coherency and replace the configuration file")
        else:                                                       # Otherwise,
            return                                                  # we have no backup to load.

    external_ts = os.path.getmtime(f"{external_path}{db_name}")
    local_ts    = os.path.getmtime(f"{local_path}{db_name}")

    if prev_sys == system and local_ts <= external_ts:              # If we opened db last time, and the external
        formatted = datetime.fromtimestamp(external_ts).strftime("%Y-%m-%d %H:%M:%S")
                                                                    # is newer, we have a problem
        raise IOError(f"{db_name} was not saved properly to {external_path}{db_name} during the last run at {formatted}")

    elif prev_sys != system:   
        if local_ts < external_ts:                                  # If the other system was the one to open the
            shutil.copyfile(f"{external_path}{db_name}",            # db last, and the external db is newer,
                f"{local_path}{db_name}")                           # we are good to go.

        else:                                                       # Otherwise, we have a problem.
            formatted = datetime.fromtimestamp(external_ts).strftime("%Y-%m-%d %H:%M:%S")
            raise IOError(f"{system} did not save {db_name} properly to {external_path}{db_name} during the last run at {formatted}")


def write_db_to_external_cache(system: str, local_path: str, external_path: str, db_name: str) -> None:
    with open(f"{external_path}{EXTERNAL_CONFIG_NAME}", "w+") as config:
        config.write(f"prev_sys={system}")

    shutil.copyfile(f"{local_path}{db_name}", f"{external_path}{db_name}")

    Path(f"{local_path}{db_name}").touch()                          # Indicate that the local version is valid
                                                                    # by giving it the most recent timestamp.