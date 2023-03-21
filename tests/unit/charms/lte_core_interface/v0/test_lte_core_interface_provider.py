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
        self.remote_app_name = "dummy-lte-core-requirer"
        self.remote_unit_name = f"{self.remote_app_name}/0"
        self.harness = testing.Harness(DummyLTECoreProviderCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_given_unit_is_leader_when_relation_is_created_then_data_is_added_to_application_databag(  # noqa: E501
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

    def test_given_multiple_requirers_when_relation_is_created_then_data_is_added_to_application_databag(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        mme_ipv4_address = "0.0.0.0"
        relation_1_remote_app_name = "srsran-1"
        relation_1_remote_unit_name = "srsran-1/0"
        relation_1_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=relation_1_remote_app_name
        )
        self.harness.add_relation_unit(relation_1_id, relation_1_remote_unit_name)
        relation_2_remote_app_name = "srsran-2"
        relation_2_remote_unit_name = "srsran-2/0"
        relation_2_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=relation_2_remote_app_name
        )
        self.harness.add_relation_unit(relation_2_id, relation_2_remote_unit_name)

        relation_2_data = self.harness.get_relation_data(
            relation_id=relation_1_id, app_or_unit=self.harness.charm.app.name
        )
        self.assertEqual(relation_2_data["mme_ipv4_address"], mme_ipv4_address)

    def test_given_unit_is_not_leader_when_relation_is_created_then_data_is_not_added_to_application_databag(  # noqa: E501
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
        with pytest.raises(AddressValueError) as e:
            self.harness.charm.lte_core_provider.set_lte_core_information(
                mme_ipv4_address=mme_ipv4_address,
                relation_id=relation_id,
            )

        self.assertEqual(str(e.value), "Invalid MME IPv4 address.")

    def test_given_not_valid_mme_ipv4_address_when_set_lte_core_information_then_value_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        mme_ipv4_address = "invalid ipv4 address"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=self.remote_app_name
        )

        with pytest.raises(AddressValueError):
            self.harness.charm.lte_core_provider.set_lte_core_information(
                mme_ipv4_address=mme_ipv4_address,
                relation_id=relation_id,
            )
