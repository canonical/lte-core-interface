# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest
from unittest.mock import patch

from ops import testing

from tests.unit.charms.lte_core_interface.v0.dummy_requirer_charm.src.charm import (
    DummyCoreRequirerCharm,
)

testing.SIMULATE_CAN_CONNECT = True

BASE_CHARM_PATH = "tests.unit.charms.lte_core_interface.v0.dummy_requirer_charm.src.charm.DummyCoreRequirerCharm"  # noqa: E501


class TestCoreRequirer(unittest.TestCase):
    def setUp(self):
        self.relation_name = "lte-core"
        self.remote_app = "lte-core-requirer"
        self.harness = testing.Harness(DummyCoreRequirerCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    # TODO: AssertionError: Expected '_on_lte_core_available' to have been called.
    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_valid_core_information_in_relation_data_when_relation_changed_then_core_available_event_emitted(  # noqa: E501
        self, patch_on_core_available
    ):
        mme_ipv4_address = "0.0.0.0"
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        remote_app_relation_data = {"mme_ipv4_address": mme_ipv4_address}

        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=self.remote_app, key_values=remote_app_relation_data
        )

        patch_on_core_available.assert_called()
        # args, _ = patch_on_core_available.call_args
        # core_available_event = args[0]

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_core_information_not_in_relation_data_when_relation_changed_then_core_available_event_not_emitted(  # noqa: E501
        self, patch_on_core_available
    ):
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=self.remote_app, key_values={}
        )

        patch_on_core_available.assert_not_called()

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_invalid_core_information_in_relation_data_when_relation_changed_then_core_available_event_not_emitted(  # noqa: E501
        self, patch_on_core_available
    ):
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        remote_app_relation_data = {"mme_ipv4_address": "not an ipv4 address"}
        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=self.remote_app, key_values=remote_app_relation_data
        )
        
        patch_on_core_available.assert_not_called()
