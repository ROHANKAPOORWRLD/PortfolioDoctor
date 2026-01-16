from fastapi import APIRouter

group_router = APIRouter()


@group_router.post("/group")
def create_group():
    pass


@group_router.patch("/group/{group_id}")
def update_group_info():
    pass


@group_router.get("/group/{group_id}")
def retrieve_group():
    pass


@group_router.get("/group/{group_id}/members")
def retrieve_group_members():
    pass


@group_router.post("/group/{group_id}/members")
def add_group_members():
    pass


@group_router.delete("/group/{group_id}/members/{user_id}")
def remove_group_members():
    pass


@group_router.delete("/group/{group_id}/members/me")
def leave_group():
    pass


@group_router.get("/me/groups")
def my_groups():
    pass
