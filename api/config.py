import pathlib

DOCKER_DATA_DIR = pathlib.Path('/data')
# TODO: another screen directory for python CLI based client instead of docker
# SCREEN_DIR = pathlib.Path.home().joinpath('.hangar_screen')
BOARD_DIR = DOCKER_DATA_DIR
BOARD_DIR.mkdir(parents=True, exist_ok=True)
