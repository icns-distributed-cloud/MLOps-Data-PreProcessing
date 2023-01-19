import httpx




def update_pre_status(db_id, path, filename, preProcessState=1):
    response = httpx.post(f'http://163.180.117.186:18088/api/predataset/post/updateprestatus', json={'preDatasetMasterId': 9, 'path': '/home/icns/abc.csv', 'fileName': 'abc.csv', 'preProcessState': 10})

    return response

