# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest
from ipaddress import AddressValueError

import pytest
from ops import testing

from tests.unit.charms.lte_core_interface.v0.dummy_provider_charm.src.charm import (
    DummyLTECoreProviderCharm,
)

testing.SIMULATE_CAN_CONNECT = True

BASE_CHARM_DIR = "tests.unit.charms.lte_core_interface.v0.dummy_requirer_charm.src.charm.DummyLTECoreRequirerCharm"  # noqa: E501


class TestCoreProvider(unittest.TestCase):
    def setUp(self):
        self.relation_name = "lte-core"
        self.remote_app_name = "lte-core-requirer"
        self.remote_unit_name = f"{self.remote_app_name}/0"
        self.harness = testing.Harness(DummyLTECoreProviderCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_given_unit_is_leader_and_relation_is_created_when_set_mme_address_then_data_is_added_to_application_databag(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        mme_ipv4_address = "0.0.0.0"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=self.remote_app_name
        )

        self.harness.add_relation_unit(relation_id, self.remote_unit_name)

        relation_data = self.harness.get_relation_data(
            relation_id=relation_id, app_or_unit=self.harness.charm.app.name
        )
        self.assertEqual(relation_data["mme_ipv4_address"], mme_ipv4_address)

    def test_given_unit_is_not_leader_and_relation_is_created_when_set_mme_address_then_data_is_not_added_to_application_databag(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=False)
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=self.remote_app_name
        )

        self.harness.add_relation_unit(relation_id, self.remote_unit_name)

        relation_data = self.harness.get_relation_data(
            relation_id=relation_id, app_or_unit=self.harness.charm.app.name
        )

        self.assertEqual(relation_data, {})

    def test_given_mme_address_is_not_valid_when_update_relation_data_then_value_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        mme_ipv4_address = "invalid ipv4 address"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=self.remote_app_name
        )
        self.harness.update_relation_data(
            relation_id=relation_id,
            app_or_unit=self.remote_app_name,
            key_values={"mme_ipv4_address": mme_ipv4_address},
        )
        with pytest.raises(AddressValueError) as e:
            self.harness.charm.lte_core_provider.set_lte_core_information(
                mme_ipv4_address=mme_ipv4_address
            )

        self.assertEqual(str(e.value), "Invalid MME IPv4 address.")

    def test_given_relation_not_created_when_charm_author_calls_set_lte_core_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        mme_ipv4_address = "0.0.0.0"

        with pytest.raises(RuntimeError):
            self.harness.charm.lte_core_provider.set_lte_core_information(
                mme_ipv4_address=mme_ipv4_address
            )
