import json
from functools import wraps
from http import HTTPStatus
from unittest.mock import patch

from tests.data.data_constants import ITEM_ID
from tests.mocks import MockDb


def mock_decorator(*args, **kwargs):
    """Decorate by doing nothing."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# PATCH THE DECORATOR HERE
patch("evertz_io_observability.decorators.start_span", mock_decorator).start()

import handler


class TestHandler:
    @patch("handler.Db")
    def test_get_item_success(self, mock_db, get_correct_item_event):
        event, context = get_correct_item_event

        mock_db.return_value = MockDb()
        response = handler.get_item(event, context)
        assert response["statusCode"] == HTTPStatus.OK
        body = json.loads(response["body"])
        assert body == {"success": True, "text": "some test text"}
        headers = response["headers"]
        assert headers["Content-Type"] == "application/vnd.api+json"

    @patch("handler.Db")
    def test_get_item_not_found(self, mock_db, get_not_existing_item_event):
        event, context = get_not_existing_item_event

        mock_db.return_value = MockDb()
        response = handler.get_item(event, context)
        assert response["statusCode"] == HTTPStatus.NOT_FOUND
        body = json.loads(response["body"])
        assert "errors" in body
        assert body["errors"][0]["code"] == "ItemNotFound"

    @patch("handler.Db")
    def test_create_item_success(self, mock_db, create_correct_item_event):
        event, context = create_correct_item_event

        mock_db.return_value = MockDb()
        response = handler.create_item(event, context)
        assert response["statusCode"] == HTTPStatus.OK
        body = json.loads(response["body"])
        assert {"success": body["success"], "text": body["text"]} == {"success": True, "text": "Hello"}
        headers = response["headers"]
        assert headers["Content-Type"] == "application/vnd.api+json"

    @patch("handler.Db")
    @patch("uuid.uuid4")
    def test_create_item_conflict(self, mock_uuid4, mock_db, create_correct_item_event):
        event, context = create_correct_item_event

        mock_db.return_value = MockDb()
        mock_uuid4.return_value = ITEM_ID
        response = handler.create_item(event, context)
        assert response["statusCode"] == HTTPStatus.CONFLICT
        body = json.loads(response["body"])
        assert "errors" in body
        assert body["errors"][0]["code"] == "ItemConflict"
