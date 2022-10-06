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
# TODO: code
```

### Provider charm

The provider charm is the one providing information about the core network
for another charm that requires this interface.

#### Example

```python
# TODO: code
```