
import httpx
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from tortoise.contrib.test import TestCase

from app import app
from app.tortoise_models.meeting import MeetingModel


class TestMeetingRouter(TestCase):
    ...

    async def test_api_update_meeting_title(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            create_meeting_response = await client.post(url="/v1/mysql/meetings")
            url_code = create_meeting_response.json()["url_code"]
            response = await client.patch(
                f"/v1/mysql/meetings/{url_code}/title", json={"title": "abc"}
            )

        assert response.status_code == HTTP_204_NO_CONTENT
        meeting = await MeetingModel.get(url_code=url_code)
        assert meeting.title == "abc"  # <-- 고침

    async def test_api_update_meeting_location(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            create_meeting_response = await client.post(url="/v1/mysql/meetings")
            url_code = create_meeting_response.json()["url_code"]
            location = "test location"

            response = await client.patch(
                f"/v1/mysql/meetings/{url_code}/location", json={"location": location}
            )

        assert response.status_code == HTTP_204_NO_CONTENT

    async def test_can_not_update_meeting_location_when_meeting_does_not_exists(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            url_code = "invalid_url_code"
            response = await client.patch(
                f"/v1/mysql/meetings/{url_code}/location",
                json={"location": "abc"},
            )
        assert response.status_code == HTTP_404_NOT_FOUND
