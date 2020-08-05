import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from celery.result import AsyncResult
from linechart.tasks import compute_taskx, compute_taskw


def main(request):
    context = {}
    template = loader.get_template('linechart/main.html')
    return HttpResponse(template.render(context, request))


def simple_task(request):
    if request.method == "POST":
        start_number = request.POST.get("start-number")
        end_number = request.POST.get("end-number")

        job = compute_taskx.apply_async((start_number, end_number))

        context = {
            "job_id": job.id,
            "start_number": start_number,
            "end_number": end_number}

        template = loader.get_template('linechart/simple_progress.html')
        return HttpResponse(template.render(context, request))

    else:
        context = {}
        template = loader.get_template('linechart/simple_progress.html')
        return HttpResponse(template.render(context, request))


def random_generator(request):
    if request.method == "POST":
        job = compute_taskw.delay(1, 1)
        context = {"job_id": job.id}
        template = loader.get_template('linechart/plot.html')
        return HttpResponse(template.render(context, request))
    else:
        context = {}
        template = loader.get_template('linechart/plot.html')
        return HttpResponse(template.render(context, request))


def fetch_test(request):
    if request.method == "POST":
        job = compute_taskw.delay(1, 1)
        context = {"job_id": job.id}
        template = loader.get_template('linechart/plot_fetch.html')
        return HttpResponse(template.render(context, request))
    else:
        context = {}
        template = loader.get_template('linechart/plot_fetch.html')
        return HttpResponse(template.render(context, request))



def poll_state(request):
    response = 'Fail'
    if request.is_ajax():
        if 'job_id' in request.POST.keys() and request.POST['job_id']:
            job_id = request.POST['job_id']
            job = AsyncResult(job_id)
            response = {"state": job.state, "data": job.result}

            if job.state == 'ABORTED':
                response = {"state": job.state}
        else:
            response = 'No job_id in the request'
    else:
        response = 'This is not an ajax request'

    json_data = json.dumps(response)
    return HttpResponse(json_data, content_type='application/json')


def update_progress(request):
    response = 'Fail'
    if request.is_ajax():
        if 'job_id' in request.POST.keys() and request.POST['job_id']:
            job_id = request.POST['job_id']
            job = AsyncResult(job_id)
            response = {"state": job.state, "data": job.result}
            print(response)
            if job.state == 'ABORTED':
                response = {"state": job.state}
        else:
            response = 'No job_id in the request'
    else:
        response = 'This is not an ajax request'

    json_data = json.dumps(response)

    return HttpResponse(json_data, content_type='application/json')


def fetch_progress(request):
    response = json.loads(request.body)
    if 'job_id' in response:
        job_id = response['job_id']
        job = AsyncResult(job_id)
        response = {"state": job.state, "data": job.result}
        print(response)
        if job.state == 'ABORTED':
            response = {"state": job.state}
    else:
        response = 'No job_id in the request'

    json_data = json.dumps(response)

    return HttpResponse(json_data, content_type='application/json')
