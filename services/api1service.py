from models.entities.Person import Person
from models.mappers.PersonMapper import get_mapper_for_person_to_create_person_response
from models.response.CreatePersonResponse import CreatePersonResponse


def create_person_handler(person_data: dict) -> CreatePersonResponse:
    person = Person(
        name=person_data['name'],
        email=person_data['email']
    )

    db_create_person(person)
    mapper = get_mapper_for_person_to_create_person_response()
    result = mapper.map(person, CreatePersonResponse)
    print(result)
    return result



def db_create_person(person: Person):
    # similuating creating of record
    print('record created successfully')

