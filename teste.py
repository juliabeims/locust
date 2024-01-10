from locust import HttpUser, constant, task, SequentialTaskSet


class MyTaskSet(SequentialTaskSet):
    @task
    def home(self):
        res = self.client.get('/')
        print(res.status_code)

    @task
    def find_flight(self):
        res = self.client.post('/reserve.php', data='''  
        {'fromPort' : 'Paris', 'toPort' : 'Buenos Aires'}''' )
        print(res.status_code)    

class MyRequest(HttpUser):
    wait_time = constant(5)
    host = "https://blazedemo.com/"
    tasks = [MyTaskSet]
