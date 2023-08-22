"""error response module"""
from fastapi import HTTPException, status


async def send_error(error_message: str) -> None:
    txt = {"result": False, "error_type": "str", "error_message": error_message}
    """error response module function"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=txt,
    )
