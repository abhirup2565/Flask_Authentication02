import requests

 #CRON JOB
def scheduledTask():
    try:
        response=requests.delete('http://127.0.0.1:5000/clearblockList')
        print(response.json())
    except Exception as e:
        print("could not execute cron job ",str(e))