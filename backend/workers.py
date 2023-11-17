from celery import Celery
from app import app

celery = Celery(
    app.import_name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)#celery object
celery.autodiscover_tasks(['tasks'], related_name='tasks', force=True)

class ContextTask(celery.Task):#class to run celery tasks in app context
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
