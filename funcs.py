from pathlib    import Path

import shutil


def load_db_from_external_cache(local_path: str, external_path:str, db_name:str) -> None:
    local = Path(f"{local_path}{db_name}")
    extern = Path(f"{external_path}{db_name}")
    if extern.exists():
        if not local.exists() or local.stat().st_mtime < extern.stat().st_mtime:
            local_dir = Path(local_path)
            if not local_dir.exists():
                local_dir.parent.mkdir()
            shutil.copyfile(extern, local)


def write_db_to_external_cache(local_path: str, external_path: str, db_name: str) -> None:
    local = Path(f"{local_path}{db_name}")
    extern = Path(f"{external_path}{db_name}")

    if not extern.parent.exists():
        try:
            extern.parent.mkdir()
        except IOError:
            raise IOError(f"Could not access external storage device at {extern}")

    shutil.copyfile(local, extern)
    Path(f"{local_path}{db_name}").touch()