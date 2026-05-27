from canvasapi import Canvas
import os


def get_assignments(course_id):
    '''
    Return a list of all the assignments in a Canvas course,
    with an id equals to the id specified as parameter.
    '''
    url = os.environ.get('CANVAS_URL', 'https://canvas.instructure.com/')
    key = os.environ.get('CANVAS_API_KEY')
    
    if not key:
        raise ValueError("CANVAS_API_KEY environment variable must be set")
    
    canvas = Canvas(url, key)
    course = canvas.get_course(course_id)
    return [x for x in course.get_assignments()]


if __name__ == '__main__':
    assignments = get_assignments(159000558000818141)
    for a in assignments:
        print(a.name, a.points_possible)