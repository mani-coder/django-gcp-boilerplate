# views.py
# Standard Library Imports
import asyncio
import logging
import time

# Third Party Library Imports
from django.http import StreamingHttpResponse
from django.shortcuts import render

# App Imports
from utils.sse import format_message  # Assuming this is your utility for formatting messages


logger = logging.getLogger(__name__)


# Ensure the view is async for SSE
async def streamer_test(request):
    num_events = int(request.GET.get("num_events", 10))

    async def event_generator():
        for count in range(num_events):
            yield format_message(f"{count}. New message at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            await asyncio.sleep(1)

    return StreamingHttpResponse(event_generator(), content_type="text/event-stream")


def streamer_test_page(request):
    return render(request, "streamer_test.html")
