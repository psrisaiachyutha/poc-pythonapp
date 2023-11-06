from mapper.object_mapper import ObjectMapper

from models.entities.Person import Person
from models.response.CreatePersonResponse import CreatePersonResponse


def get_mapper_for_person_to_create_person_response() -> ObjectMapper:
    mapper = ObjectMapper()
    mapper.create_map(Person, CreatePersonResponse)
    return mapper
