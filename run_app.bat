@echo off

rem Change directory to frontend/ticket
cd frontend\ticket

rem Run npm run serve
start npm run serve

rem Change directory to backend
cd ../../backend

rem Open a new terminal and run celery beat
start "" cmd /k celery -A workers.celery beat --max-interval 1 -l info

rem Open a new terminal and run celery worker
start "" cmd /k celery -A workers.celery worker -l info -P gevent

rem Open a new terminal and run python main.py
start "" cmd /k python main.py
