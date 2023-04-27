import sched
import time
import datetime
import subprocess

scheduler = sched.scheduler(time.time, time.sleep)

def run_script():
    subprocess.call(["python", "./wfp.py"])

run_time = datetime.time(2, 0, 0)

now = datetime.datetime.now().time()

if now < run_time:
    next_run_time = datetime.datetime.combine(datetime.date.today(), run_time)
else:
    next_run_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), run_time)
time_until_next_run = (next_run_time - datetime.datetime.now()).total_seconds()

scheduler.enter(time_until_next_run, 1, run_script, ())

scheduler.run()
