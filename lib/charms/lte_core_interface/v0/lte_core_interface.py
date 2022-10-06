# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Library for the `lte-core` relation.

This library contains the Requires and Provides classes for handling the `lte-core`
interface.

## Getting Started
From a charm directory, fetch the library using `charmcraft`:

# TODO: change this to the real URL once the library is published
```shell
charmcraft fetch-lib charms.lte_core.v0.lte_core
```

# TODO: need for additional libraries in requirements.txt?

### Requirer charm
The requirer charm is the one requiring to connect to an instance of the core
from another charm that provides this interface.

# TODO: fill requirer example

### Provider charm
The provider charm is the one providing information about the core network
for another charm that requires this interface.

# TODO fill requirer example
"""

# TODO change to fstrings?


import logging

from jsonschema import exceptions, validate  # type: ignore[import]
from ops.charm import CharmBase, CharmEvents, RelationChangedEvent
from ops.framework import EventBase, EventSource, Handle, Object

# The unique Charmhub library identifier, never change it
LIBID = "3fbbdca922ec4ddd9598c3382034ad61"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1


logger = logging.getLogger(__name__)

REQUIRER_JSON_SCHEMA = {
    # TODO: Check URL
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "`lte-core` requirer root schema",
    "type": "object",
    "description": "The `lte-core` root schema comprises the entire requirer databag for this interface.",  # noqa: E501
    "examples": [
        {
            "mme_ipv4_address": "127.0.0.1",  # noqa: E501
        }
    ],
    "properties": {
        "mme_ipv4_address": {
            "type": "string",
        },
    },
    "required": [
        "mme_ipv4_address",
    ],
    "additionalProperties": True,
}


class CoreAvailableEvent(EventBase):
    """Charm event emitted when a core is available."""

    def __init__(self, handle: Handle, mme_ipv4_address: str):
        """Init."""
        super().__init__(handle)
        self.mme_ipv4_address = mme_ipv4_address

    def snapshot(self) -> dict:
        """Returns snapshot."""
        return {"mme_ipv4_address": self.mme_ipv4_address}

    def restore(self, snapshot: dict) -> None:
        """Restores snapshot."""
        self.mme_ipv4_address = snapshot["mme_ipv4_address"]


class CoreRequirerCharmEvents(CharmEvents):
    """List of events that the core requirer charm can leverage."""

    core_available = EventSource(CoreAvailableEvent)


class CoreRequires(Object):
    """Class to be instantiated by the charm requiring the core."""

    on = CoreRequirerCharmEvents()

    def __init__(self, charm: CharmBase, relationship_name: str):
        """Init."""
        super().__init__(charm, relationship_name)
        self.charm = charm
        self.relationship_name = relationship_name
        self.framework.observe(
            charm.on[relationship_name].relation_changed, self._on_relation_changed
        )

    @staticmethod
    def _relation_data_is_valid(remote_app_relation_data: dict) -> bool:
        try:
            validate(instance=remote_app_relation_data, schema=REQUIRER_JSON_SCHEMA)
            return True
        except exceptions.ValidationError as e:
            logger.error("Invalid relation data: %s", e)
            return False

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handler triggered on relation changed event.

        Args:
            event: Juju event (RelationChangedEvent)

        Returns:
            None
        """
        relation = self.model.get_relation(self.relationship_name)
        if not relation:
            logger.warning("No relation with name %s", self.relationship_name)
            return
        if not relation.app:
            logger.warning("No remote application in relation: %s", self.relationship_name)
            return
        remote_app_relation_data = relation.data[relation.app]
        if not self._relation_data_is_valid(dict(remote_app_relation_data)):
            logger.warning(
                "Provider relation data did no pass JSON Schema validation: \n%s",
                event.relation.data[event.app],  # type: ignore[index]
            )
            return
        self.on.core_available.emit(
            mme_ipv4_address=remote_app_relation_data["mme_ipv4_address"],
        )


class CoreProvides(Object):
    """Class to be instantiated by the charm providing the core."""

    def __init__(self, charm: CharmBase, relationship_name: str):
        """Init."""
        super().__init__(charm, relationship_name)
        self.relationship_name = relationship_name
        self.charm = charm

    @staticmethod
    def mme_ipv4_address_is_valid(mme_ipv4_address: str) -> bool:
        """Returns whether mme ipv4 address is valid."""
        # TODO ip address validation
        pass

    def set_core_information(self, mme_ipv4_address: str):
        """Sets mme_ipv4_address in the application relation data.

        Args:
            mme_ipv4_address: MME ipv4 address
        Returns:b
            None
        """
        if not self.charm.unit.is_leader():
            raise RuntimeError("Unit must be leader to set application relation data.")
        if not self.mme_ipv4_address_is_valid(mme_ipv4_address):
            raise ValueError("Invalid MME ipv4 address.")
        relation = self.model.get_relation(self.relationship_name)
        if not relation:
            raise RuntimeError("Relation %s not created yet", self.relationship_name)
        relation.data[self.charm.app].update({"mme_ipv4_address": mme_ipv4_address})
