"""
Module containing API routes and handlers
"""


from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException, status
from models.wishlist import WishlistItemResponse, WishlistResponse
from auth.services import get_current_user
from models.user import UserPydantic
from typing import Annotated
from pydantic import AnyHttpUrl
from api.wishlist_services import (
    create_item,
    fetch_wishlist,
    fetch_item,
    edit_item,
    remove_item,
)


api_router = APIRouter()


@api_router.post("/add_item", response_model=WishlistItemResponse, tags=["wishlist"])
async def add_item(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[AnyHttpUrl, Form()],
    user: UserPydantic = Depends(get_current_user),
    image: UploadFile = File(None),
):
    return await create_item(
        title=title,
        description=description,
        link=link,
        user=user,
        image=image,
    )


@api_router.get("/get_wishlist", response_model=WishlistResponse, tags=["wishlist"])
async def get_item(
    page: int = 1,
    per_page: int = 3,
    user: UserPydantic = Depends(get_current_user),
):
    """
    Get wishlist item on page
    :param page: starts with 1
    :param per_page: count of items per page
    :param user:
    :return: list of items on page, current page, per_page value, total_items, total_pages
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Page out of range"
        )
    if per_page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="per_page must be > 0"
        )
    return await fetch_wishlist(page=page - 1, per_page=per_page, user=user)


@api_router.get("/get_item", response_model=WishlistItemResponse, tags=["wishlist"])
async def get_item_via_id(item_id: int):
    """
    Get item via id

    :param item_id: id of item to get
    :return: item if exists  or error
    """
    return await fetch_item(item_id)


@api_router.put("/update_item", response_model=WishlistItemResponse, tags=["wishlist"])
async def update_item(
    item_id: int,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[AnyHttpUrl, Form()],
    user: UserPydantic = Depends(get_current_user),
    image: UploadFile = File(None),
):
    return await edit_item(
        item_id=item_id,
        title=title,
        description=description,
        link=link,
        user=user,
        image=image,
    )


@api_router.delete(
    "/delete/{item_id}", response_model=WishlistItemResponse, tags=["wishlist"]
)
async def delete_item(item_id: int, user=Depends(get_current_user)):
    return await remove_item(item_id, user)
