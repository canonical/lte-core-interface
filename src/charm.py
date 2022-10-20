#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


"""THIS CHARM IS NOT SUPPOSED TO BE DEPLOYED."""

from ops.charm import CharmBase
from ops.main import main


class PlaceholderCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        """Init."""
        super().__init__(*args)


if __name__ == "__main__":
    main(PlaceholderCharm)
