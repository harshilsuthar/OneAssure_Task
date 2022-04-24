from rest_framework.viewsets import ViewSet
from .serializers import CsvUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Csv
from .utils import refine_query, get_response
from rest_framework.exceptions import APIException


class CsvUploadView(ViewSet):
    serializer_class = CsvUploadSerializer

    def create(self, request):
        """
        Validate uploaded data contains valid csv file and save its data to database
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            record_count=serializer.save()
            if record_count:
                response = get_response(message=f"{record_count} New records added successfully", status_code=201)
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                raise APIException("Record creation failed")
        except Exception as ex:
            raise APIException(detail=str(ex), code=400)

    def list(self, request):
        """
        List all data from the database with filters
        """
        try:
            query = refine_query(request.GET.dict())
            pipeline = [
                {"$match": query},
                {"$addFields": {"id": {"$toString": "$_id"}}},
                {"$project": {"_id": 0}},
            ]
            data = Csv.aggregate(pipeline, raise_exception=True)
            response = get_response(data=data)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            raise APIException(detail=str(ex), code=400)

    def delete(self, request, *args, **kwargs):
        """
        Filter and delete records
        """
        try:
            query = refine_query(request.GET.dict())
            delete_object = Csv.delete_many(query)
            delete_count = delete_object.deleted_count
            response = get_response(message=f"{delete_count} records deleted")
            return Response(
                response, status=status.HTTP_200_OK
            )

        except Exception as ex:
            raise APIException(detail=str(ex), code=400)
