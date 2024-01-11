from locust import HttpUser, task, events, constant
from locust_plugins.listeners.jmeter import JmeterListener


class DemoBlazeUser(HttpUser):
    host = "https://www.demoblaze.com"
    wait_time = constant(5)

    @task
    def t(self):
        self.client.get("/")


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    JmeterListener(env=environment, testplan="examplePlan")