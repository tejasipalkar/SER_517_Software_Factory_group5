from canvasapi import Canvas

class Canvas_Calendar:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def getallevents(self):
        courses = self.canvas.get_courses()
        # user = self.canvas.get_user('self')
        courses_array = []
        # user_array = []
        resultant_json_format = {"events":[]}
        for course in courses:
            courses_array.append('course_' + str(course.id))
        # user_array.append('user_' + str(user.id))
        course_events = self.canvas.get_calendar_events(all_events = 1, type = 'event', context_codes=courses_array)
        # user_events = self.canvas.get_calendar_events(all_events = 1, type = 'event', context_codes=user_array)
        # course_assignments = self.canvas.get_calendar_events(all_events = 1, type = 'assignment', context_codes=courses_array)
        for event in course_events:
            resultant_json_format["events"].append(event.__dict__['attributes'])
        # for event in user_events:
        #     resultant_json_format["events"].append(event.__dict__['attributes'])
        # for assignment in course_assignments:
        #     resultant_json_format["assignments"].append(assignment.__dict__['assignment'])

        return resultant_json_format

        # with open('calendar.json', 'w') as fp:
        #     json.dump(resultant_json_format, fp, indent = 4)

    def create_event(self, array_of_objects):
        counter = 0
        for objects in array_of_objects:
            event_dict = objects
            if self.canvas.create_calendar_event(calendar_event = event_dict):
                counter += 1

        if counter == len(array_of_objects):
            return "success"
        else:
            return "failure"

    def delete_event(self, array_ids):
        counter = 0
        for ids in array_ids:
            event = self.canvas.get_calendar_event(ids)
            if event.delete():
                counter += 1

        if counter == len(array_ids):
            return "success"
        else:
            return "failure"

    def edit_event(self,array_of_objects):
        counter = 0
        for objects in array_of_objects:
            event = self.canvas.get_calendar_event(objects['id'])
            event_dict = objects
            if event.edit(calendar_event = event_dict):
                counter += 1

        if counter == len(array_of_objects):
            return "success"
        else:
            return "failure"

cal = Canvas_Calendar("7236~o5XXfM7GrZZogzsg8xdQoODn3DdBqdwlq2DOM9qo4uD7q3e1Y79Ssi9vmObH9q42")
