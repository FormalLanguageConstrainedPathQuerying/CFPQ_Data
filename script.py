import boto3
import json


ACCESS_KEY = "AKIA326NG25W2XT6TBAZ"
SECRET_KEY = "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"


def get_dataset(access_key, secret_key):
    s3 = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    keys = []
    file_name_old = str()
    dataset = dict()
    answer = dict()

    for key in s3.list_objects(Bucket='cfpq-data')['Contents']:
        keys.append(key['Key'])

    for key in keys:
        file_name, graph_name = key.split('/')
        if file_name != file_name_old and file_name_old != "":
            answer[file_name_old] = dataset
            dataset = {}
        spleeeet = graph_name.split('.')
        arch_ext, file_ext = spleeeet[-2] + '.' + spleeeet[-1], spleeeet[-3]
        for i in range(3):
            spleeeet.pop(-1)
        if spleeeet[-1] == 'txt':
            spleeeet.pop(-1)
        graph_name = ".".join(spleeeet)
        tmp = dict()
        tmp['version_id'] = s3.head_object(Bucket="cfpq-data", Key=key)['VersionId']
        tmp['file_extension'] = "." + file_ext
        tmp['archive_extension'] = "." + arch_ext
        dataset[graph_name] = tmp
        file_name_old = file_name

    answer[file_name_old] = dataset
    return answer


if __name__ == "__main__":
    with open('config.json', 'w') as file:
        json.dump(get_dataset(ACCESS_KEY, SECRET_KEY), file, indent=4)
