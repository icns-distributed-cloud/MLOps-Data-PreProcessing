import httpx




def update_pre_status(db_id, path, filename, preProcessState=1):
    response = httpx.post(f'http://163.180.117.186:18088/api/predataset/post/updateprestatus', json={'preDatasetId': db_id, 'path': path, 'fileName': filename, 'preProcessState': preProcessState})

    return response

