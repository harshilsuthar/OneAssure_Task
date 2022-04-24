def get_response(data={}, message="", status_code=200, errors=[]):
    """
    Generates common response struture
    """
    response = {
        "data": data,
        "message": message,
        "status_code": status_code,
        "errors": errors,
    }
    return response


def csvSplitter(csv_data):
    """
    From CSV data seperate header, raw_header and data
    """
    try:
        data = []
        raw_header = tuple(csv_data.head())
        header = str(raw_header)
        if len(tuple(csv_data.head())) == 1:
            headindex = header.rfind(",")
            header = header[:headindex] + "" + header[headindex + 1 :]
            header = header.replace("'", "")
        else:
            header = header.replace("'", "")

        # seperating values from csv
        for row in csv_data.values:
            if len(tuple(row)) == 1:
                row = str(tuple(row))
                rowindex = row.rfind(",")
                row = row[:rowindex] + "" + row[rowindex + 1 :]
                data.append(row)
            else:
                row = str(tuple(row))
                data.append(row)
        return header, raw_header, data
    except Exception as ex:
        print(ex)
        return None, None, None


def refine_query(query):
    """
    Make query more general like if collection contains data in int format and search data send as string then
    search for string data as well as int data.
    """
    for key, value in query.items():
        try:
            eval_value = eval(value)
            query[key] = {"$in": [value, eval_value]}
        except:
            pass
    return query
