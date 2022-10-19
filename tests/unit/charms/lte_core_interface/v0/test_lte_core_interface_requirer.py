# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest
from unittest.mock import patch

from ops import testing

from tests.unit.charms.lte_core_interface.v0.dummy_requirer_charm.src.charm import (
    DummyLTECoreRequirerCharm,
)

testing.SIMULATE_CAN_CONNECT = True

BASE_CHARM_PATH = "tests.unit.charms.lte_core_interface.v0.dummy_requirer_charm.src.charm.DummyLTECoreRequirerCharm"  # noqa: E501


class TestLTECoreRequirer(unittest.TestCase):
    def setUp(self):
        self.relation_name = "lte-core"
        self.remote_app = "lte-core-provider"
        self.harness = testing.Harness(DummyLTECoreRequirerCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_valid_lte_core_information_in_relation_data_when_relation_changed_then_core_available_event_emitted(  # noqa: E501
        self, patch_on_lte_core_available
    ):
        mme_ipv4_address = "0.0.0.0"
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        remote_app_relation_data = {"mme_ipv4_address": mme_ipv4_address}

        self.harness.update_relation_data(
            relation_id=relation_id,
            app_or_unit=self.remote_app,
            key_values=remote_app_relation_data,
        )

        patch_on_lte_core_available.assert_called()
        args, _ = patch_on_lte_core_available.call_args
        lte_core_available_event = args[0]
        self.assertEqual(lte_core_available_event.mme_ipv4_address, mme_ipv4_address)

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_lte_core_information_not_in_relation_data_when_relation_changed_then_core_available_event_not_emitted(  # noqa: E501
        self, patch_on_lte_core_available
    ):
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=self.remote_app, key_values={}
        )

        patch_on_lte_core_available.assert_not_called()
