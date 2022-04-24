import pandas
from rest_framework import serializers
from .models import Csv
from .utils import csvSplitter


class CsvUploadSerializer(serializers.Serializer):
    csv_upload = serializers.FileField()

    def create(self, validated_data):
        """
        Read CSV data, parse it to dictionary and store it
        """
        csv_upload = validated_data.get("csv_upload")
        csv_dataframe = pandas.read_csv(csv_upload)
        header, raw_header, data = csvSplitter(csv_dataframe)
        upload_data = []
        for row in data:
            str_to_tuple = eval(row)
            key_value_tuple = zip(str_to_tuple, raw_header)
            single_data = dict(map(reversed, key_value_tuple))
            upload_data.append(single_data)
        inserted_value = Csv.insert_many(upload_data)
        return len(inserted_value.inserted_ids)
