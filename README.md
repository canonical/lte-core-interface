# lte-core-interface

This charm library contains the Requires and Provides classes for handling the `lte-core`
interface.

> :warning: Do not deploy this charm. It is meant to only be used as a charm library.

## Getting Started
From a charm directory, fetch the library using `charmcraft`:

```shell
charmcraft fetch-lib charms.lte_core_interface.v0.lte_core_interface
```

Add the following libraries to the charm's `requirements.txt` file:
- jsonschema

### Requirer charm

The requirer charm is the one requiring to connect to an instance of the core
from another charm that provides this interface.

#### Example

```python

from ops.charm import CharmBase
from ops.main import main

from charm.lte_core_interface.v0.lte_core_interface import (
    CoreAvailableEvent,
    CoreRequires,
)


class DummyCoreRequirerCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.lte_core_requirer = CoreRequires(self, "lte-core")
        self.framework.observe(
            self.lte_core_requirer.on.core_available,
            self._on_core_available,
        )

    def _on_core_available(self, event: CoreAvailableEvent):
        print(event.mme_ipv4_address)


if __name__ == "__main__":
    main(DummyCoreRequirerCharm)

```

### Provider charm

The provider charm is the one providing information about the core network
for another charm that requires this interface.

#### Example

```python

from ops.charm import CharmBase
from ops.main import main

from charm.lte_core_interface.v0.lte_core_interface import (
    CoreProvides,
)


class DummyCoreProviderCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.core_provider = CoreProvides(self, "lte-core")
        self.framework.observe(
            self.on.lte_core_relation_joined, self._on_lte_core_relation_joined
        )

    def _on_lte_core_relation_joined(self, event: RelationJoinedEvent):
        if self.unit.is_leader():
            self.core_provider.set_core_information(
                mme_ipv4_address="mme ipv4 address from the core"
            )


if __name__ == "__main__":
    main(DummyCoreProviderCharm)
```