from sqlalchemy import create_engine
from models.models import Base

engine = create_engine('mysql+pymysql://lugzan_hunt_py:lugzanHuntPy123456@lugzan.beget.tech/lugzan_hunt_py?charset=utf8mb4')
Base.metadata.create_all(engine)