# lte-core-interface

This library contains the Requires and Provides classes for handling the `lte-core`
interface.

The purpose of the library is to relate a charmed EPC (Provider) with charmed simulated enodeB and
user equipment (UEs) (Requirer). The interface will share the IP address of the MME
(Mobility Management Entity) from EPC to the charm which contains the corresponding
simulated enodeBs and UEs.

> :warning: Do not deploy this charm. It is meant to only be used as a charm library.

## Getting Started

From a charm directory, fetch the library using `charmcraft`:

```shell
charmcraft fetch-lib charms.lte_core_interface.v0.lte_core_interface
```

Add the following libraries to the charm's `requirements.txt` file:

- jsonschema

### Provider charm

The provider charm is the one providing information about the LTE core network
for another charm that requires this interface.

#### Example

```python

from ops.charm import CharmBase, RelationJoinedEvent
from ops.main import main

from charms.lte_core_interface.v0.lte_core_interface import (
    LTECoreProvides,
)


class DummyLTECoreProviderCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.lte_core_provider = LTECoreProvides(self, "lte-core")
        self.framework.observe(
            self.on.lte_core_relation_joined, self._on_lte_core_relation_joined
        )

    def _on_lte_core_relation_joined(self, event: RelationJoinedEvent) -> None:
        if not self.unit.is_leader():
            return
        mme_ipv4_address = "some code for fetching the mme ipv4 address"
        self.lte_core_provider.set_lte_core_information(mme_ipv4_address=mme_ipv4_address)


if __name__ == "__main__":
    main(DummyLTECoreProviderCharm)
```

### Requirer charm

The requirer charm is the one requiring to connect to an instance of the LTE core
from another charm that provides this interface.

#### Example

```python

from ops.charm import CharmBase
from ops.main import main

from charms.lte_core_interface.v0.lte_core_interface import (
    LTECoreAvailableEvent,
    LTECoreRequires,
)


class DummyLTECoreRequirerCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.lte_core_requirer = LTECoreRequires(self, "lte-core")
        self.framework.observe(
            self.lte_core_requirer.on.lte_core_available,
            self._on_lte_core_available,
        )

    def _on_lte_core_available(self, event: LTECoreAvailableEvent):
        mme_ipv4_address = event.mme_ipv4_address
        <Do something with the mme_ipv4_address>


if __name__ == "__main__":
    main(DummyLTECoreRequirerCharm)
```
