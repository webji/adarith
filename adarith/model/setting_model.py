from sqlalchemy import Column, Integer, String, Boolean, MetaData

from . import Base

class SettingModel(Base):
    __tablename__ = 't_settings'

    id = Column(Integer, primary_key=True)
    key = Column(String(20))
    value = Column(String(32))
    enabled = Column(Boolean)
    
    def __repr__(self):
        return f"<SettingModel (key={self.key}, value={self.value}, enabled={self.enabled}>"


    @staticmethod
    def init_setting(session = None):
        initialized = session.query(SettingModel).filter_by(key='initialized').first()
        if initialized == None:
            initialized = SettingModel(key='initialized', value='False', enabled=True)
            session.add(initialized)
            session.commit()
        
        