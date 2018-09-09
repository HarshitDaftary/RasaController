import ptvsd

# Allow other computers to attach to ptvsd at this IP address and port, using the secret
ptvsd.enable_attach("1", address = ('192.168.1.106', 1234))

# Pause the program until a remote debugger is attached
ptvsd.wait_for_attach()
