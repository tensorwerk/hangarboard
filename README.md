# Hangarboard
Hangar board is a collection of GUI utilities for visualizing and
inspecting the data stored in multiple hangar repositories. It is also
designed to guide the users for the interaction on hangar repo from a
python program or from command line. This README should be considered as
the documentation for setting up and quick start the hangar board.

## Installation
Currently hangarboard works only with docker but making it a `pip`
installable is something we have in the top of our priority list. Launch
hangarboard using prebuilt docker image:

```shell script
docker run -p 8000:8000 -v /path/to/repo1:/data/repo1 -it --rm tensorwerk/hangarboard
``` 
In case you have more than one repository, you can either map the parent
folder that has multiple repositories to `/data` in docker or map each
repository individually as given in the command above. This will bring
up the hangarboard server on `localhost:8000`. Hangarboard is in the
first release now and currently capable of only navigating you through
different repositories, arraysets inside repositories and samples inside
arraysets. However, upcoming releases should help you visualize the data
using the plugin system, check the commit history, figure out the diff
between branches (or commits) and understand different ways of
interacting with a hangar repository

