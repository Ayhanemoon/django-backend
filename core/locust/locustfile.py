from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    
    @task
    def post_list(self):
        self.client.get('/blog/api/v1/post/')