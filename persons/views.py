from rest_framework.views import APIView, Response, Request, status
from .models import Person
from django.forms.models import model_to_dict
from .validators import is_kenzie_domain, NotKenzieEmailError
import ipdb


class PersonView(APIView):
    def get(self, request: Request) -> Response:
        # QuerySet
        persons = Person.objects.all()

        # return Response(persons)
        persons_list = []

        for person in persons:
            person_dict = model_to_dict(person)
            persons_list.append(person_dict)

        return Response(persons_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            valid_data = is_kenzie_domain(request.data["email"])
        except NotKenzieEmailError as error:
            return Response(
                # {"error": "email must be a @kenzie.com email"},
                # {"error": error.args[0]},
                {"error": error.message},
                status.HTTP_400_BAD_REQUEST,
            )

        person = Person.objects.create(**request.data)
        person_dict = model_to_dict(person)

        return Response(person_dict, status.HTTP_201_CREATED)


class PersonDetailView(APIView):
    def get(self, request: Request, person_id: str) -> Response:
        # ipdb.set_trace()
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({"error": "person not found"}, status.HTTP_404_NOT_FOUND)

        person_dict = model_to_dict(person)

        return Response(person_dict, status.HTTP_200_OK)

    def patch(self, request: Request, person_id: str) -> Response:
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({"error": "person not found"}, status.HTTP_404_NOT_FOUND)

        # person.name = request.data.get("name", person.name)
        # person.cpf = request.data.get("cpf", person.cpf)
        # person.email = request.data.get("email", person.email)
        # person.birthdate = request.data.get("birthdate", person.birthdate)
        # person.married = request.data.get("married", person.married)

        for key, value in request.data.items():
            setattr(person, key, value)

        person.save()
        person_dict = model_to_dict(person)

        return Response(person_dict, status.HTTP_200_OK)

    def delete(self, request: Request, person_id: str) -> Response:
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({"error": "person not found"}, status.HTTP_404_NOT_FOUND)

        person.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
