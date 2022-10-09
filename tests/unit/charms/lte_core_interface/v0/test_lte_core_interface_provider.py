# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


from ipaddress import AddressValueError
import unittest

import pytest
from ops import testing

from tests.unit.charms.lte_core_interface.v0.dummy_provider_charm.src.charm import (
    DummyCoreProviderCharm,
)

testing.SIMULATE_CAN_CONNECT = True

BASE_CHARM_DIR = "tests.unit.charms.lte_core_interface.v0.dummy_requirer_charm.src.charm.DummyCoreRequirerCharm"  # noqa: E501


class TestCoreProvider(unittest.TestCase):
    def setUp(self):
        self.relation_name = "lte-core"
        self.harness = testing.Harness(DummyCoreProviderCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_given_unit_is_leader_and_remote_unit_joined_relation_when_set_mme_address_then_data_is_added_to_application_databag(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        remote_app = "lte-core-requirer"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )
        mme_ipv4_address = "0.0.0.0"

        self.harness.charm.core_provider.set_core_information(mme_ipv4_address=mme_ipv4_address)
        relation_data = self.harness.get_relation_data(
            relation_id=relation_id, app_or_unit=self.harness.charm.app.name
        )

        self.assertEqual(relation_data["mme_ipv4_address"], mme_ipv4_address)

    def test_given_unit_is_leader_and_relation_is_not_created_when_set_core_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        mme_ipv4_address = "0.0.0.0"
        with pytest.raises(RuntimeError) as e:
            self.harness.charm.core_provider.set_core_information(
                mme_ipv4_address=mme_ipv4_address
            )

        self.assertEqual(str(e.value), "Relation lte-core not created yet.")

    def test_given_unit_is_not_leader_and_relation_created_when_set_core_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=False)
        remote_app = "lte-core-requirer"
        self.harness.add_relation(relation_name=self.relation_name, remote_app=remote_app)

        with pytest.raises(RuntimeError) as e:
            self.harness.charm.core_provider.set_core_information(mme_ipv4_address="0.0.0.0")

        self.assertEqual(str(e.value), "Unit must be leader to set application relation data.")

    def test_given_mme_address_is_not_valid_when_set_core_information_then_value_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        remote_app = "lte-core-requirer"
        mme_ipv4_address = "not an ipv4 address"
        self.harness.add_relation(relation_name=self.relation_name, remote_app=remote_app)
        with pytest.raises(AddressValueError) as e:
            self.harness.charm.core_provider.set_core_information(
                mme_ipv4_address=mme_ipv4_address
            )

        self.assertEqual(str(e.value), "Invalid MME IPv4 address.")
