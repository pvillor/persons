from rest_framework.views import APIView, Response, Request, status
from .models import Person
from django.forms.models import model_to_dict


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
        print("=" * 100)
        print(request.data)
        print("=" * 100)

        person = Person.objects.create(**request.data)
        person_dict = model_to_dict(person)

        return Response(person_dict, status.HTTP_201_CREATED)
