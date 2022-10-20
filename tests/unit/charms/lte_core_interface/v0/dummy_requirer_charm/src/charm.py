#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


"""Charm the service."""

from charms.lte_core_interface.v0.lte_core_interface import (
    LTECoreAvailableEvent,
    LTECoreRequires,
)
from ops.charm import CharmBase
from ops.main import main


class DummyLTECoreRequirerCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        """Init."""
        super().__init__(*args)
        self.lte_core_requirer = LTECoreRequires(self, "lte-core")
        self.framework.observe(
            self.lte_core_requirer.on.lte_core_available,
            self._on_lte_core_available,
        )

    def _on_lte_core_available(self, event: LTECoreAvailableEvent):
        pass


if __name__ == "__main__":
    main(DummyLTECoreRequirerCharm)
