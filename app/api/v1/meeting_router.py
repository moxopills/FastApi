from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.dtos.update_meeting_request import (
    MEETING_DATE_MAX_RANGE,
    UpdateMeetingDateRangeRequest,
    UpdateMeetingLocationRequest,
    UpdateMeetingTitleRequest,
)
from app.services.meeting_service_mysql import (
    service_create_meeting_mysql,
    service_get_meeting_mysql,
    service_update_meeting_date_range_mysql,
    service_update_meeting_location_mysql,
    service_update_meeting_title_mysql,
)

mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["mysql-meetings"])


@mysql_router.post("", response_model=CreateMeetingResponse)
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    meeting = await service_create_meeting_mysql()
    return CreateMeetingResponse(
        url_code=meeting.url_code,
        end_date=None,
        start_date=None,
        title="",
        location="",
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
        end_date=meeting.end_date,
        start_date=meeting.start_date,
        title=meeting.title,
        location=meeting.location,
    )


# ✅ Meeting 날짜 범위 업데이트
@mysql_router.patch(
    "/{meeting_url_code}/date_range", description="meeting의 날짜 range 를 설정합니다."
)
async def api_update_meeting_date_range_mysql(
    meeting_url_code: str,
    update_meeting_date_range_request: UpdateMeetingDateRangeRequest,
) -> GetMeetingResponse:
    if update_meeting_date_range_request.exceeds_max_range():
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"start {update_meeting_date_range_request.start_date} "
                f"and end {update_meeting_date_range_request.end_date} "
                f"should be within {MEETING_DATE_MAX_RANGE.days} days"
            ),
        )

    meeting_before_update = await service_get_meeting_mysql(meeting_url_code)
    if meeting_before_update is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {meeting_url_code} not found",
        )

    if meeting_before_update.start_date or meeting_before_update.end_date:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"meeting: {meeting_url_code} "
                f"start: {meeting_before_update.start_date} "
                f"end: {meeting_before_update.end_date} are already set"
            ),
        )

    meeting_after_update = await service_update_meeting_date_range_mysql(
        meeting_url_code,
        update_meeting_date_range_request.start_date,
        update_meeting_date_range_request.end_date,
    )
    assert meeting_after_update

    return GetMeetingResponse(
        url_code=meeting_after_update.url_code,
        start_date=meeting_after_update.start_date,
        end_date=meeting_after_update.end_date,
        title=meeting_after_update.title,
        location=meeting_after_update.location,
    )


@mysql_router.patch(
    "/{meeting_url_code}/title",
    description="meeting의 title을 설정합니다.",
    status_code=HTTP_204_NO_CONTENT,
)
async def api_update_meeting_title_mysql(
    meeting_url_code: str, update_meeting_title_request: UpdateMeetingTitleRequest
) -> None:
    updated = await service_update_meeting_title_mysql(
        meeting_url_code, update_meeting_title_request.title
    )
    if not updated:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {meeting_url_code} not found",
        )
    return None


@mysql_router.patch(
    "/{meeting_url_code}/location",
    description="meeting의 location을 설정합니다.",
    status_code=HTTP_204_NO_CONTENT,
)
async def api_update_meeting_location_mysql(
    meeting_url_code: str, update_meeting_location_request: UpdateMeetingLocationRequest
) -> None:
    updated = await service_update_meeting_location_mysql(
        meeting_url_code, update_meeting_location_request.location
    )
    if not updated:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {meeting_url_code} not found",
        )
    return None
