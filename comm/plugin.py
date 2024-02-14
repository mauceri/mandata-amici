import logging
from amicus_interfaces import IObserver, IObservable, IPlugin
from nio.rooms import MatrixRoom
from nio.events.room_events import RoomMessageText

logger = logging.getLogger(__name__)

class Load(IObserver):
    def __init__(self,observable:IObservable=None):
        self.__observable =observable

    async def notify(self,room:MatrixRoom, event:RoomMessageText, msg:str):
        logger.info(f"***************************** L'utilisateur {event.sender} a écrit {msg} depuis ls salon {room.name}")
        # Coco répète ce qu'on lui dit
        await self.__observable.notify(room,event,f"L'utilisateur {event.sender} a écrit {msg} depuis le salon {room.name}",None, None)

    def prefix(self):
        return "!c.load"
    
class Plugin(IPlugin):
    def __init__(self,observable:IObservable):
        self.__observable = observable
        self.load = Load(self.__observable)
        logger.info(f"********************** Observateur créé {self.load.prefix()}")
        
    def start(self):
        logger.info(f"********************** Inscripton de {self.load.prefix()}")
        self.__observable.subscribe(self.load)

    async def stop(self):
        self.__observable.unsubscribe(self.load)