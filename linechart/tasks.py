from celery import Celery
from celery import current_task
from celery import states
import random
import time

app = Celery('tasks', backend='redis', broker='redis://localhost')


@app.task
def compute_taskx(x, y):
    for i in range(100):
        current_task.update_state(state='PROGRESS', meta={'process_percent': "%0.2f" % i,
                                                          'total': 100})
        time.sleep(0.1)

    current_task.update_state(state=states.SUCCESS)
    return int(x)+1


@app.task
def compute_taskw(x, y):
    for i in range(100):
        #some hard task that takes time (like running a model)
        for j in range(random.randint(10, 30)):
            current_task.update_state(state=states.PENDING)
            time.sleep(0.1)


        #report the value of hard duty task
        current_task.update_state(state='PROGRESS', meta={'rand_value': random.random(),
                                                          'total': 100})
        #time.sleep(0.01) # for plot
        time.sleep(0.1) #for plot_fetch

    #finished! success we have the final value we are looking for
    current_task.update_state(state=states.SUCCESS)
    return int(x)+1
