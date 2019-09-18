import pathlib

DOCKER_DATA_DIR = pathlib.Path('/data')
# TODO: another screen directory for python CLI based client instead of docker
# SCREEN_DIR = pathlib.Path.home().joinpath('.hangar_screen')
SCREEN_DIR = DOCKER_DATA_DIR
SCREEN_DIR.mkdir(parents=True, exist_ok=True)
