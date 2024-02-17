import logging
from amicus_interfaces import IObserver, IObservable, IPlugin
from nio.rooms import MatrixRoom
from nio.events.room_events import RoomMessageText
import os

logger = logging.getLogger(__name__)

class Get(IObserver):
    def __init__(self,observable:IObservable=None):
        self.__observable =observable

    def get_file_name(chemin):
        return os.path.basename(chemin)


    async def notify(self,room:MatrixRoom, event:RoomMessageText, path:str):
        logger.info(f"***************************** L'utilisateur {event.sender} a écrit {path} depuis ls salon {room.name}")
        filename = os.path.basename(path)
        await self.__observable.notify(room,event,f"Fichier /data/plugins.yaml",path, filename)

    def prefix(self):
        return "!c.get"
    
class Reload(IObserver):
    def __init__(self,observable:IObservable=None):
        self.__observable =observable

    def get_file_name(chemin):
        return os.path.basename(chemin)

    async def notify(self,room:MatrixRoom, event:RoomMessageText, path:str):
        logger.info(f"***************************** L'utilisateur {event.sender} a demandé un rechargement")
        await self.__observable.notify(room,event,self.prefix(),None, None)

    def prefix(self):
        return "!c.reload"
    
class Plugin(IPlugin):
    def __init__(self,observable:IObservable):
        self.__observable = observable
        self.get = Get(self.__observable)
        logger.info(f"********************** Observateur créé {self.get.prefix()}")
        self.reload = Reload(self.__observable)
        logger.info(f"********************** Observateur créé {self.reload.prefix()}")
        
    def start(self):
        logger.info(f"********************** Inscripton de {self.get.prefix()}")
        self.__observable.subscribe(self.get)
        logger.info(f"********************** Inscripton de {self.reload.prefix()}")
        self.__observable.subscribe(self.reload)

    async def stop(self):
        self.__observable.unsubscribe(self.get) 
        self.__observable.unsubscribe(self.reload)