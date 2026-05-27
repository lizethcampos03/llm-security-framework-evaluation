from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
import os
import re


@login_required
def getResource(request):
    '''
    Get username and date from the request, then
    send the file to the user by creating path by the username and date.
    '''
    username = request.GET.get("username")
    date = request.GET.get("date")
    
    # Verify the authenticated user can only access their own resources
    if username != request.user.username:
        return HttpResponseForbidden("Access denied")
    
    # Validate username format (alphanumeric and underscore only)
    if not username or not re.match(r'^[a-zA-Z0-9_]+$', username):
        return HttpResponseForbidden("Invalid username")
    
    # Validate date format (YYYY-MM-DD)
    if not date or not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return HttpResponseForbidden("Invalid date format")
    
    # Construct the path safely
    base_dir = os.path.abspath('./static/')
    user_dir = os.path.join(base_dir, username)
    file_path = os.path.join(user_dir, date)
    
    # Ensure the resolved path is within the base directory (prevent path traversal)
    if not os.path.abspath(file_path).startswith(base_dir):
        return HttpResponseForbidden("Access denied")
    
    # Check if file exists and is a file (not a directory)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("Resource not found")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return HttpResponse(content)
    except (IOError, OSError):
        raise Http404("Resource not found")