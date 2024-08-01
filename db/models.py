from db import Base
from sqlalchemy import Column, Integer, String, BigInteger


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger)
    message_text = Column(String(255))
