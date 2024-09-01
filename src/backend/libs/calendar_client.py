from libs.nylas_client import nylas
from libs.calendar_prettifier import prettify

def getAllCalendars(grant_id):
    calendars = nylas.calendars.list(grant_id)
    return calendars

def getAllEvents(grant_id):
    main_calendar_id = getAllCalendars(grant_id)[0][0].id

    _events = nylas.events.list(
        grant_id,
        query_params={
        "calendar_id": main_calendar_id
        }
    )

    events = []
    for event in _events[0]:
        events.append(prettify(event))

    return events

def createEvent(grant_id, name: str, start_time: int, end_time: int):
    events = nylas.events.create(
        grant_id,
        request_body={
            "title": name,
            "when": {
            "start_time": start_time,
            "end_time": end_time
            },
        },
        query_params={
            "calendar_id": getAllCalendars(grant_id)[0][0].id
        }
    )

    return events