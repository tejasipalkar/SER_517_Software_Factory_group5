from canvasapi import Canvas
# from canvasapi.calendar_event import CalendarEvent
API_URL = "https://asu.instructure.com"
API_KEY = "7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42"
canvas = Canvas(API_URL, API_KEY)

def getevents():
    events = canvas.get_calendar_events(all_events = 1, context_codes=['course_15760'])
    for event in events:
        print(event)

getevents()
