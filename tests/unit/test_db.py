import pytest
from errors import ItemNotFound
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from db import Db, ItemType, ItemConflict
from boto3.dynamodb.conditions import Attr

TENANT_ID = "test_tenant"
ITEM_ID = "test_item"
ITEM_DATA = {"success": True, "text": "Test data"}

class TestDb:
    @patch("db.restricted_table")
    def test_put_item_success(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table

        Db.put_item(ItemType.ITEM, TENANT_ID, ITEM_ID, ITEM_DATA)

        mock_table.put_item.assert_called_once_with(
            Item={
                "pk": f"{TENANT_ID}#item#{ITEM_ID}",
                "item_id": ITEM_ID,
                "data": ITEM_DATA,
            },
            ConditionExpression=Attr("pk").not_exists(),
        )

    @patch("db.restricted_table")
    def test_put_item_conflict(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table
        mock_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "ConditionalCheckFailedException"}}, "PutItem"
        )

        with pytest.raises(ItemConflict):
            Db.put_item(ItemType.ITEM, TENANT_ID, ITEM_ID, ITEM_DATA)

    @patch("db.restricted_table")
    def test_get_item_success(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table
        mock_table.get_item.return_value = {"Item": {"data": ITEM_DATA}}

        result = Db.get_item(ItemType.ITEM, TENANT_ID, ITEM_ID)

        assert result == ITEM_DATA

    @patch("db.restricted_table")
    def test_get_item_not_found(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table
        mock_table.get_item.return_value = {}

        with pytest.raises(ItemNotFound):
            Db.get_item(ItemType.ITEM, TENANT_ID, ITEM_ID)

    @patch("db.restricted_table")
    def test_update_item_success(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table

        Db.update_item(ItemType.ITEM, TENANT_ID, ITEM_ID, ITEM_DATA)

        mock_table.put_item.assert_called_once_with(
            Item={
                "pk": f"{TENANT_ID}#item#{ITEM_ID}",
                "item_id": ITEM_ID,
                "data": ITEM_DATA,
            },
            ConditionExpression=Attr("pk").not_exists(),
        )

    @patch("db.restricted_table")
    def test_update_item_conflict(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table
        mock_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "ConditionalCheckFailedException"}}, "PutItem"
        )

        with pytest.raises(ItemConflict):
            Db.update_item(ItemType.ITEM, TENANT_ID, ITEM_ID, ITEM_DATA)

    @patch("db.restricted_table")
    def test_delete_item_success(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table

        Db.delete_item(ItemType.ITEM, TENANT_ID, ITEM_ID)

        mock_table.delete_item.assert_called_once_with(
            Item={
                "pk": f"{TENANT_ID}#item#{ITEM_ID}",
                "item_id": ITEM_ID,
            },
            ConditionExpression=Attr("pk").not_exists(),
        )

    @patch("db.restricted_table")
    def test_delete_item_error(self, mock_restricted_table):
        mock_table = MagicMock()
        mock_restricted_table.return_value = mock_table
        mock_table.delete_item.side_effect = ClientError(
            {"Error": {"Code": "ConditionalCheckFailedException"}}, "DeleteItem"
        )

        with pytest.raises(ItemConflict):
            Db.delete_item(ItemType.ITEM, TENANT_ID, ITEM_ID)      
