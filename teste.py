from locust import HttpUser, constant, task, SequentialTaskSet
from bs4 import BeautifulSoup


class MyTaskSet(SequentialTaskSet):    
    @task
    def home(self):
        expected_response = 200
        with self.client.get('/', catch_response=True,name='blazedemo') as result:
            if expected_response == result.status_code:
                result.success()
                soup = BeautifulSoup(result.text,'html.parser')
                self.select_data = {}
                for select_tag in soup.find_all('select'):
                    select_name = select_tag.get('name')
                    option = select_tag.find('option')
                    option_value = option.get('value')
                    if select_name is not None and option_value is not None:
                        self.select_data[select_name] = option_value

                print(self.select_data)
            else:
                result.failure()

    @task
    def find_flight(self):
        expected_response = 200
        with self.client.post('/reserve.php', catch_response=True , name ="reserve" ,data=self.select_data) as response:
            if expected_response == response.status_code:
                response.success()
                soup = BeautifulSoup(response.text,'html.parser')
                form_tag = soup.find('form')
                
                self.input_data = {}

                # Iterando sobre as tags <input> dentro da tag <form>
                for input_tag in form_tag.find_all('input'):
                    input_name = input_tag.get('name')
                    input_value = input_tag.get('value')
                    
                    # Adicionando ao dicionário se ambos name e value estiverem presentes
                    if input_name is not None and input_value is not None:
                        self.input_data[input_name] = input_value

                # Exibindo o dicionário resultante
                print(self.input_data)
                
            else:
                response.failure()
    
    @task
    def purchase(self):
        expected_response = 200
        with self.client.post('/purchase.php', catch_response=True, name='purchase', data=self.input_data) as response:
            if expected_response == response.status_code:
                response.success()
            else:
                response.failure()

    @task
    def confirmation(self):
        expected_response = 200
        purchase_data = {
            '_token': '',
            'inputName': 'JULIA DA SILVA',
            'address': 'Rua Guilherme Miguel de Souza, 123,',
            'city': 'Florianópolis',
            'state': 'SC',
            'zipCode': 88037340,
            'cardType': 'visa',
            'creditCardNumber': 55555555555,
            'creditCardMonth': 11,
            'creditCardYear': 2017,
            'nameOnCard': 'Julia Silva',
            'rememberMe': 'on'
        }

        with self.client.post('/confirmation.php', catch_response=True, name='confirmation', data=purchase_data) as response:
            if expected_response == response.status_code:
                response.success()
            else:
                response.failure()


class MyRequest(HttpUser):
    wait_time = constant(5)
    host = "https://blazedemo.com/"
    tasks = [MyTaskSet]
