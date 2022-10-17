#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


from ops.charm import CharmBase, RelationChangedEvent
from ops.main import main

from lib.charms.lte_core_interface.v0.lte_core_interface import CoreProvides


class DummyCoreProviderCharm(CharmBase):
    def __init__(self, *args):
        """Charm the service."""
        super().__init__(*args)
        self.core_provider = CoreProvides(self, "lte-core")
        self.framework.observe(
            self.on.lte_core_relation_changed, self._on_lte_core_relation_changed
        )

    def _on_lte_core_relation_changed(self, event: RelationChangedEvent) -> None:
        if not self.unit.is_leader():
            return
        self.core_provider.set_core_information(mme_ipv4_address="0.0.0.0")


if __name__ == "__main__":
    main(DummyCoreProviderCharm)
