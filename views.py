"""
GAVIP Example AVIS: Alerts AVI
"""
import os
import logging

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import time
from avi.models import AlertsJob

ROLES = settings.GAVIP_ROLES

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def index(request):
    """
    This view is the first view that the user sees
    We send a dictionary called a context, which contains
    'millis' and 'standalone' variables.
    """
    context = {
        "millis": int(round(time.time() * 1000)),
        "show_welcome": request.session.get('show_welcome', True)
    }
    request.session['show_welcome'] = False
    return render(request, 'avi/index.html', context)


@require_http_methods(["POST"])
def run_query(request):
    """
    This is called when the user submits their job parameters in
    their interface.

    We pull the parameters from the request POST parameters.

    We create an avi_job_request, which must be used to create
    the AlertsJob instance, so that the pipeline can excercise
    the pipeline correctly.

    We attach the job_request instance to th AlertsJob; this
    extends the AviJob class, which is required for pipeline
    processing.

    We start the job using the job_request ID, and return the
    ID to the user so they can view progress.
    """
    outfile = request.POST.get("outfile")

    job = AlertsJob.objects.create(
        outputFile=outfile
    )
    return JsonResponse({})


@require_http_methods(["GET"])
def job_result(request, job_id):
    job = get_object_or_404(AlertsJob, request_id=job_id)
    file_path = os.path.join(settings.OUTPUT_PATH, job.outputFile)
    with open(file_path, 'r') as outFile:
        # job_data = json.load(outFile)
        job_data = outFile.read()
    return render(request, 'avi/job_result.html', {'job_id': job_id,
                  'job_data': job_data})
