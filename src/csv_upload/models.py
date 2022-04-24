from djongo import models
from django.conf import settings

CsvCollection = settings.DB.csv


class Csv(models.Model):
    _id = models.ObjectIdField(primary_key=True)

    @staticmethod
    def insert_many(csv_list):
        output = CsvCollection.insert_many(csv_list)
        return output

    @staticmethod
    def aggregate(pipeline, raise_exception=False):
        """
        To find objects from database
        raises 404 not found error if object not found for given query
        """

        csv_data = CsvCollection.aggregate(pipeline)
        return csv_data

    @staticmethod
    def delete_many(query):
        delete_object = CsvCollection.delete_many(query)
        return delete_object

    class Meta:
        db_table = "csv"
