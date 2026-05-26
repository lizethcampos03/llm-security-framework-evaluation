import random\n\n\ndef getSessionID():\n    '''\n    Return a random and unique session ID.\n    '''\n    return random.randint(0, 0xFFFFFFFF)
