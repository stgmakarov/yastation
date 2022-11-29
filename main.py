import yaml
from api import YandexAPI
from utils import create_scenario
from config import NEEDED_SCENARIOS, NEEDED_SCENARIOS_LOGICS

with open("config.yaml", "r") as stream:
    try:
        conf = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

LOGIN = conf['username']
PASSWORD = conf['password']


class Application:
    api = None
    speaker = None
    speakers = None
    scenarios = None

    def __init__(self, login, password):
        self.api = YandexAPI(login, password)
        self.speakers = self.api.get_speakers()
        self.scenarios = self.api.get_scenarios()

    def reload_scenarios(self):
        self.scenarios = self.api.get_scenarios()

    def init_speaker(self):
        if len(self.speakers) > 1:
            print("Выберите устройство: ")
            for (i, speaker) in enumerate(self.speakers):
                print(str(i + 1) + ". " + speaker['name'])

            number = int(input("Номер: ")) - 1
        else:
            number = 0
        self.speaker = self.speakers[number]['id']

    def init_scenarios(self):
        existing_scenarios = [scenario['name'] for scenario in self.scenarios]
        for scenario in NEEDED_SCENARIOS:
            if scenario in existing_scenarios: continue
            if scenario in NEEDED_SCENARIOS_LOGICS:
                logic = NEEDED_SCENARIOS_LOGICS[scenario]
                self.api.add_scenario(create_scenario(scenario, self.speaker, logic))
        self.reload_scenarios()

    def start(self):
        self.init_speaker()
        self.init_scenarios()
        while True:
            print("Выберете действие:")
            print("1. Старт")
            print("2. Стоп")
            print("3. Следующий трек")
            print("4. Предыдущий трек")
            print("5. Тише")
            print("6. Громче")
            print("7. Включи песню")
            print("8. Скажи текст")
            print("0. Выход")
            number = int(input("Номер: ")) - 1
            if number == -1:
                break;
            if number == 6:
                name = input("Название: ")
                self.api.play_song(self.speaker, name,
                                   [scenario['id'] for scenario in self.scenarios if scenario['name'] == 'Включи'][0])
                continue
            if number == 7:
                txt = input("Текст: ")
                self.api.repeat_text(self.speaker, txt,
                                   [scenario['id'] for scenario in self.scenarios if scenario['name'] == 'Повтори'][0])
                continue
            scenario = NEEDED_SCENARIOS[number]
            id = ''
            for exscenario in self.scenarios:
                if exscenario['name'] == scenario:
                    id = exscenario['id']
            self.api.exec_scenario(id)
            print("Done")


if __name__ == "__main__":
    app = Application(LOGIN, PASSWORD)
    app.start()
