#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


"""Charm the service."""

from ops.charm import CharmBase, RelationJoinedEvent
from ops.main import main

from lib.charms.lte_core_interface.v0.lte_core_interface import (
    CoreProvides,
)


class DummyLteCoreProviderCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        """Init."""
        super().__init__(*args)
        
    # TODO: Add your code here

if __name__ == "__main__":
    main(DummyLteCoreProviderCharm)