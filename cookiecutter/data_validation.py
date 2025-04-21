from typing import Any, Mapping
from context import logger

def validate_item_data(item_data: Mapping[str, Any]) -> bool:
    """
    Validate the incoming item data.
    :param item_data: data to store with item
    :return: True if valid, False otherwise
    """
    # For example, check if required fields are present
    required_fields = ["success", "text"]
    for field in required_fields:
        if field not in item_data:
            raise ValueError
    return
        