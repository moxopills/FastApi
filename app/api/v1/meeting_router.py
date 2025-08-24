from datetime import datetime
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.dtos.update_meeting_request import UpdateMeetingLocationRequest
from app.services.meeting_service_mysql import (
    service_create_meeting_mysql,
    service_get_meeting_mysql,
)

mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["mysql-meetings"])

@mysql_router.post("", response_model=CreateMeetingResponse)
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    meeting = await service_create_meeting_mysql()
    return CreateMeetingResponse(
        url_code=meeting.url_code,
        end_date=datetime.now().date(),
        start_date=datetime.now().date(),
        title="test",
        location="test",
    )


@mysql_router.get("/{meeting_url_code}", response_model=GetMeetingResponse)
async def api_get_meeting_mysql(meeting_url_code: str) -> GetMeetingResponse:
    meeting = await service_get_meeting_mysql(meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {meeting_url_code} not found",
        )
    return GetMeetingResponse(
        url_code=meeting.url_code,
        end_date=datetime.now().date(),
        start_date=datetime.now().date(),
        title="test",
        location="test",
    )


@mysql_router.patch(
    "/{meeting_url_code}/date_range", description="meeting 의 날을 range 를 설정합니다"
)
async def api_update_meeting_date_range_mysql(
    meeting_url_code: str, update_meeting_date_range_request: UpdateMeetingLocationRequest
) -> GetMeetingResponse:
    return GetMeetingResponse(
        url_code="abc",
        start_date=datetime.now().date(),
        end_date=datetime.now().date(),
        title="test",
        location="test",
    )
