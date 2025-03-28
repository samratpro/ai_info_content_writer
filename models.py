from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Postdata(Base):
    __tablename__ = 'Postdata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    website_name = Column(String(500))
    username = Column(String(500))
    app_pass = Column(String(500))
    category_name = Column(String(500))
    chatgpt_api = Column(String(200))
    chatgpt_model = Column(String(200))
    deepseek_api = Column(String(200))
    deepseek_model = Column(String(200))
    gemni_api = Column(String(200))
    gemni_model = Column(String(200))
    api_select = Column(String(200))
    title_prompt = Column(Text)
    intro_prompt = Column(Text)
    h2_prompt = Column(Text)
    outline_prompt = Column(Text)
    paragraph_prompt = Column(Text)
    faq_h2 = Column(Text)
    faq_question_prompt = Column(Text)
    faq_ans_prompt = Column(Text)
    conclusion_h2 = Column(Text)
    conclusion_prompt = Column(Text)

DATABASE_URL = "sqlite:///postdb.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)