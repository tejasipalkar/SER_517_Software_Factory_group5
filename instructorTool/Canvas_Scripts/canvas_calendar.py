from canvasapi import Canvas

class Canvas_Calendar:
    def __init__(self, api_key):
        self.API_URL = "https://asu.instructure.com"
        self.canvas = Canvas(self.API_URL, api_key)

    def getallevents(self, id):
        courses_array = ['course_'+ str(id)]
        resultant_json_format = {"events":[], "assignments":[]}
        course_events = self.canvas.get_calendar_events(all_events = 1, type = 'event', context_codes=courses_array)
        course_assignments = self.canvas.get_calendar_events(all_events = 1, type = 'assignment', context_codes=courses_array)
        for event in course_events:
            resultant_json_format["events"].append(event.__dict__['attributes'])
        for assignment in course_assignments:
            resultant_json_format["assignments"].append(assignment.__dict__['assignment'])

        return resultant_json_format

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

    def edit_assignment(self,array_of_objects, course_id):
        counter = 0
        course = self.canvas.get_course(course_id)
        for objects in array_of_objects:
            assignment = course.get_assignment(objects['id'])
            assignment_dict = objects
            if assignment.edit(assignment = assignment_dict):
                counter += 1

        if counter == len(array_of_objects):
            return "success"
        else:
            return "failure"
