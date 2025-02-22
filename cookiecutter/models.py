"""
Models for AWS ApiGateway and Lambda request and response
"""

from typing import Optional

from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from pydantic import BaseModel, Field, Json


class Item(BaseModel):
    """Item model"""

    success: bool
    text: str


class ItemIdPathParam(BaseModel):
    """Item Id Path parameter inside ApiGateway event"""

    item_id: str


class RequestContext(BaseModel):
    """Model for request context inside ApiGateway event"""

    request_id: str = Field(alias="requestId")


class ItemModel(APIGatewayProxyEventModel):
    """ApiGateway event schema"""

    # pylint: disable=unsubscriptable-object
    body: Optional[Json[Item]]  # type: ignore[assignment]


class Headers(BaseModel):
    """Response headers"""

    class Config:
        """config for Headers"""

        populate_by_name = True

    content_type: str = Field(alias="Content-Type")


class ErrorsBody(BaseModel):
    """Errors"""

    errors: list
