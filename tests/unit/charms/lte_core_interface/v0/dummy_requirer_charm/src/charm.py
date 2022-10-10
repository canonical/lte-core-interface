#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


"""Charm the service."""

from ops.charm import CharmBase
from ops.main import main

from lib.charms.lte_core_interface.v0.lte_core_interface import (
    CoreAvailableEvent,
    CoreRequires,
)


class DummyCoreRequirerCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        """Init."""
        super().__init__(*args)
        self.core_requirer = CoreRequires(self, "lte-core")
        self.framework.observe(
            self.core_requirer.on.lte_core_available,
            self._on_lte_core_available,
        )

    def _on_lte_core_available(self, event: CoreAvailableEvent):
        pass


if __name__ == "__main__":
    main(DummyCoreRequirerCharm)
