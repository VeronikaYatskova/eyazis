from agents import AgentBase, agents
from typing import List

from .message_loop import MessageResponseLoop
from .interfaces import Message, Response

from help import get_words, to_normal

class MessageListener:
  agents: List[AgentBase]
  keywords: list

  def __init__(self):
    self.agents = agents
    self.loop: MessageResponseLoop = None

    self.commands = {
      ('Hello'): self.agents[0].execute, #HelloAgent
      ('добрый', 'день'): self.agents[0].execute, #HelloAgent
      ('добрый', 'вечер'): self.agents[0].execute, #HelloAgent
      ('добрый', 'утро'): self.agents[0].execute, #HelloAgent
      ('салют'): self.agents[0].execute, #HelloAgent
      ('халло'): self.agents[0].execute, #HelloAgent
      ('хай'): self.agents[0].execute, #HelloAgent
      ('фильм', 'серия'): self.agents[1].execute, #FindMovieAgent
      ('яой'): self.agents[2].execute, #SurpriseAgent
      ('фильм', 'рейтинг'): self.agents[3].execute, #FindMovieAgentRaiting
      ('фильм', 'жанр'): self.agents[4].execute, #FindMovieAgentGenre
      ('film', 'year'): self.agents[5].execute, #FindMovieAgentYear
      ('жалко'): self.agents[6].execute, #PittyAgent
      ('помощь'): self.agents[7].execute, #HelpAgent
      ('помочь'): self.agents[7].execute, #HelpAgent
      ('что', 'уметь'): self.agents[7].execute, #HelpAgent
    }
  
  def executeMovieAgent(self, input_string: list, *args: list):
    answer = 'hello, my friend.'
    print(input_string)
    for keys in self.commands.keys():
      check = []
      if type(keys) is tuple:
        for key in keys:
          if key in input_string:
            check.append(1)
          else:
            check.append(0)
      else:
        if keys in input_string:
            check.append(1)
        else:
          check.append(0)

      if all(check):
        answer = self.commands[keys](*args)
        break
      else:
        answer = "Я не знаю ответ"
    return answer
  
  def executeAgent(self, input_string: list, *args: list, body):
    
    if "art critic" in body.lower():
        answer = "The Sorcerer is a famous painting painted by the Italian artist Leonardo da Vinci. This work of art was created in the early 16th century and is still one of the most admired and significant paintings in the world." \
"The painting The Dandy depicts a young man known as a dandy or black-headed dandy. He is sitting on a branch holding a growing flower bud. The black-headed dandy symbolizes innocence and purity, and reveals the beauty and fragility of nature." \
"The main feature of this painting is the use of oil paints on the board, which allows you to achieve rich color and depth in the image. Attention to detail and realism create a sense of liveliness and animation of the painting character" \
"Despite the beauty of the painting Chegol, its history is no less interesting. It has been in many noble collections at various times and was also stolen and then returned to the Museo dell'Arte Italiana in Milan. It epitomizes the timelessness and purity of art, continuing to delight and inspire generations of people since its creation."
    
    if "film" and "year" in body.lower():
      answer = ""
    return answer

  def setLoop(self, messageResponseLoop: MessageResponseLoop):
    self.loop = messageResponseLoop


  async def done(self, response: Response):
    print(response.message)
    await self.loop.handleResponse(response)

  async def execute(self, message: Message):
    id = message.id
    body = message.message

    words, words_en = get_words(body, False, 'en')
    words = to_normal(words)

    input_dict = dict()
    input_dict['words_en'] = words_en
    input_dict['body'] = body

    answer = self.executeAgent(words, input_dict, body)

    response = Response(id, answer)
    await self.done(response)