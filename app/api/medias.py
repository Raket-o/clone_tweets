"""media route processing module"""
from fastapi import APIRouter, File, Request, UploadFile

from fastapi.responses import FileResponse

from app.database.transactions import add_medias_db

router = APIRouter(prefix="/medias", tags=["medias"])


@router.post(
    path="/", response_description="", response_model="", status_code=201
)
async def add_medias(
    request: Request, file: UploadFile = File(...)
) -> dict[str, bool | int] | None:
    """the function adds media to the database"""
    api_key = request.headers.get("api-key")

    file_location = f"app/medias/{file.filename}"

    res = await add_medias_db(api_key=api_key, file_name=file.filename)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return res


@router.get(
    path="/{file_name}",
    response_description="",
    response_model="",
    status_code=200,
)
async def get_medias(file_name: str) -> FileResponse:
    """the function outputs a media file"""
    file_location = f"app/medias/{file_name}"
    return FileResponse(file_location)
