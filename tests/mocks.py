from typing import Any, Mapping

from db import Db, ItemKeys, ItemType
from errors import ItemConflict, ItemNotFound
from tests.data.data_constants import ITEM_ID, TENANT_ID


class MockDb(Db):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_item(item_type: ItemType, tenant_id: str, item_id: str, fields=None) -> dict[str, Any]:
        if (
            ItemKeys.get_keys(item_type=ItemType.ITEM, tenant_id=TENANT_ID, item_id=ITEM_ID).primary
            == ItemKeys.get_keys(item_type=ItemType.ITEM, tenant_id=tenant_id, item_id=item_id).primary
        ):
            return {"success": True, "text": "some test text"}
        else:
            raise ItemNotFound(item_type.value, tenant_id, item_id)

    @staticmethod
    def put_item(item_type: ItemType, tenant_id: str, item_id: str, item_data: Mapping[str, Any] = None):
        if (
            ItemKeys.get_keys(item_type=ItemType.ITEM, tenant_id=TENANT_ID, item_id=ITEM_ID).primary
            != ItemKeys.get_keys(item_type=ItemType.ITEM, tenant_id=tenant_id, item_id=item_id).primary
        ):
            return {"success": True, "text": "Hello"}
        else:
            raise ItemConflict(item_type.value, tenant_id, item_id)
