#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


from charms.lte_core_interface.v0.lte_core_interface import LTECoreProvides
from ops.charm import CharmBase, RelationJoinedEvent
from ops.main import main


class DummyLTECoreProviderCharm(CharmBase):
    def __init__(self, *args):
        """Charm the service."""
        super().__init__(*args)
        self.lte_core_provider = LTECoreProvides(self, "lte-core")
        self.framework.observe(self.on.lte_core_relation_joined, self._on_lte_core_relation_joined)

    def _on_lte_core_relation_joined(self, event: RelationJoinedEvent) -> None:
        if not self.unit.is_leader():
            return
        self.lte_core_provider.set_lte_core_information(mme_ipv4_address="0.0.0.0")


if __name__ == "__main__":
    main(DummyLTECoreProviderCharm)
