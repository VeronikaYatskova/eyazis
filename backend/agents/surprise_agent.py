from .agnet_base import AgentBase

class SurpriseAgent(AgentBase):
  def __init__(self):
    super().__init__()

  def execute(self, input_dict: dict) -> str: # Сюрприз агент
    answer = 'Держи ссылку на прекрасное фильма: https://anime-go.online/195-skuchnyj-mir-gde-ne-suschestvuet-samoj-idei-pohabnyh-shutok.html'
    return answer