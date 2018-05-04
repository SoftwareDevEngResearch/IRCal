from tools import black_body_interface as bbi
test = bbi.BlackBodyCommands()
test.configure_port()
b = test.read_temperature()
print(b)