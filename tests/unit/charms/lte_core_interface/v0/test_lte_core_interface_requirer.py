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
        self.maxDiff = None

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_lte_core_information_in_relation_data_is_empty_when_relation_changed_then_on_lte_core_available_not_called(  # noqa: E501
        self, patch_on_lte_core_available
    ):
        mme_ipv4_address = ""
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        remote_app_relation_data = {"mme_ipv4_address": mme_ipv4_address}
        expected_log = "Provider relation data did not pass JSON schema validation."  # noqa: E501

        with self.assertLogs() as captured:
            self.harness.update_relation_data(
                relation_id=relation_id,
                app_or_unit=self.remote_app,
                key_values=remote_app_relation_data,
            )
            self.assertEqual(expected_log, captured.records[0].getMessage())

        patch_on_lte_core_available.assert_not_called()

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_valid_lte_core_information_in_relation_data_when_relation_changed_then_lte_core_available_event_is_emitted(  # noqa: E501
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

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_lte_core_information_not_in_relation_data_when_relation_changed_and_schema_validation_fails_then_core_available_event_not_emitted(  # noqa: E501
        self, patch_on_lte_core_available
    ):
        wrong_mme_ipv4_address = "invalid ip address"
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        remote_app_relation_data = {"mme_ipv4_address": wrong_mme_ipv4_address}

        self.harness.update_relation_data(
            relation_id=relation_id,
            app_or_unit=self.remote_app,
            key_values=remote_app_relation_data,
        )

        patch_on_lte_core_available.assert_not_called()

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_lte_core_information_not_in_relation_data_when_relation_changed_then_core_available_event_not_emitted(  # noqa: E501
        self, patch_on_lte_core_available
    ):
        relation_id = self.harness.add_relation(self.relation_name, remote_app=self.remote_app)
        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=self.remote_app, key_values={}
        )

        patch_on_lte_core_available.assert_not_called()

    @patch(f"{BASE_CHARM_PATH}._on_lte_core_available")
    def test_given_valid_lte_core_information_in_relation_data_when_relation_changed_then_lte_core_available_event_has_the_correct_info(  # noqa: E501
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

        args, _ = patch_on_lte_core_available.call_args
        lte_core_available_event = args[0]
        self.assertEqual(lte_core_available_event.mme_ipv4_address, mme_ipv4_address)
