"""metrics processing module"""
import prometheus_client
from fastapi import APIRouter, Response


router = APIRouter()


@router.get(path="/metrics")
async def get_metrics() -> Response:
    """metrics processing function"""
    return Response(
        content=prometheus_client.generate_latest(),
        media_type="text/plain",
    )

