from . import api
from flask import current_app as app
from flask import request
from .response_utils import JSON_MIME_TYPE, success_, success_json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ResultProxy
import json
 
Base = declarative_base()

'''
# This is returning with quotes
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
    
        return json.JSONEncoder.default(self, obj)
'''
 
class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    state = Column(String(250), nullable=True)
    country = Column(String(250), nullable=True)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    # toJson is not working (AttributeError: 'weakref' object has no attribute '__dict__')
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) 

def get_session():
    engine = create_engine('mysql://test:test111@localhost/test')
    Base.metadata.bind = engine
    
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    
    return session

'''
    /city/get/all/cities
    http://127.0.0.1:5000/city/get/all/cities
'''
@api.route('/city/get/all/cities')
def get_all_cities():   
    
    session = get_session()    
    city_list = session.query(City).all()

    city_new_list = []
    for city in city_list:
        content = ''+str(city.id)+' - '+str(city.name)+' - '+str(city.state)+' - '+str(city.country)
        
        #print(type(city))
        #print(city.as_dict())
        
        city_new_list.append(city.as_dict())  
        #city_json = json.dumps(city, cls=AlchemyEncoder)
        #city_new_list.append(city_json)      
        #print(content)
    
    result_json = {
        'result': city_new_list,
        
        'api_error': 0
    }
    
    return success_json(result_json)

'''
    /city/add
    http://127.0.0.1:5000/city/add
    http://127.0.0.1:5000/city/add?name=Theni&state=TA&country=India
'''
@api.route('/city/add')
def add_city():
    
    name = request.args.get('name')
    state = request.args.get('state')
    country = request.args.get('country')
    
    session = get_session()
    new_city = City(name = name, state = state, country = country)
    session.add(new_city)
    session.commit()
    
    print('city['+name+' - '+state+' - '+country+'] added')
    
    result_json = {
        'result': 'ok',
        
        'api_error': 0
    }
    
    return success_json(result_json)
    
'''
    /city/update
    http://127.0.0.1:5000/city/update
    http://127.0.0.1:5000/city/update?name=Toronto&state=ON&country=Canada&id=8
'''
@api.route('/city/update')    
def update_city():
    
    id = request.args.get('id', type=int)
    name = request.args.get('name')
    state = request.args.get('state')
    country = request.args.get('country')
    
    session = get_session()
    session.query(City).filter(City.id == id).update({City.name: name, City.state : state, City.country : country}, synchronize_session=False)
    session.commit()
    
    print('city['+name+' - '+state+' - '+country+'] updated')
    
    print(ResultProxy.rowcount)
    
    if ResultProxy.rowcount == 1:
        result_json = {
            'result': 'ok',
            
            'api_error': 0
        }
        
        return success_json(result_json)
    else:
        result_json = {
            'result': 'not updated properly ',
            
            'api_error': 102
        }
                
        return success_json(result_json)    


'''
    /city/delete/id
    http://127.0.0.1:5000/city/delete/id
    http://127.0.0.1:5000/city/delete/7
'''
@api.route('/city/delete/<int:id>')  
def delete_city(id):
    
    session = get_session()
    session.query(City).filter(City.id == id).delete(synchronize_session = False)
    session.commit()
    
    print('city['+str(id)+'] deleted')   
    
    result_json = {
        'result': 'ok',
        
        'api_error': 0
    }
    
    return success_json(result_json)