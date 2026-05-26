from django.conf.urls import url\nimport pickle\n\n\ndef getPickleData(pickled):\n    '''\n    Return deserialized data\n    '''\n    return pickle.loads(pickled)
