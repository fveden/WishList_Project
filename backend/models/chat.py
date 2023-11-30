from tortoise import Model, fields
from pydantic import BaseModel
from models.user import UserResponse
from datetime import datetime
from typing import Optional, List


class Chat(Model):
    id = fields.IntField(pk=True)
    wishlist_item = fields.OneToOneField(
        "models.WishlistItem", related_name="chat", on_delete=fields.CASCADE
    )


class MessageResponse(BaseModel):
    id: int
    user: Optional[int] = None
    text: str
    reply_to: Optional[int] = None
    timestamp: datetime


class ChatMessage(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="messages", on_delete=fields.SET_NULL, null=True
    )
    chat = fields.ForeignKeyField(
        "models.Chat", related_name="messages", on_delete=fields.CASCADE
    )
    text = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField(auto_now=True)
    reply_to = fields.ForeignKeyField(
        "models.ChatMessage",
        related_name='replies',
        null=True,
        on_delete=fields.SET_NULL,
    )

    async def to_response(self, owner, recipient) -> MessageResponse:
        print(self.user_id, owner.id, recipient.id)
        user = None if (self.user_id != owner.id and self.user_id != recipient.id) else self.user_id
        return MessageResponse(
            id=self.id,
            user=user,
            text=self.text,
            reply_to=self.reply_to_id,
            timestamp=self.timestamp,
        )





class ChatResponse(BaseModel):
    id: int
    wishlist_item: int
    messages: list[MessageResponse]