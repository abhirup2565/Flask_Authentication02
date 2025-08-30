from app import createapp
from app.extensions import db,cron
from app.cron import scheduledTask

app = createapp()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        cron.add_job(id = 'Scheduled Task', func=scheduledTask, trigger="cron", hour=0)
        cron.start()
    app.run(debug=True)