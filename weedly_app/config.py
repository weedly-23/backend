import os

basedir = os.path.dirname(__file__)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '', '../weedly.db')

SQLALCHEMY_DATABASE_URI = 'postgresql://example:example@127.0.0.1:5432/mydatabase'


'''      POSTGRES_PASSWORD: example
      POSTGRES_USER: example
      POSTGRES_DB: mydatabase
          ports:
      - 8080:8080
      
'''
