"""
This file is just for testing purpose
"""

whole_msg = "//Thanks kjfd ma kfjhk gdfh kl   ma  Boss"
msg_without_cmd = whole_msg.split(maxsplit=1)[0]
print(msg_without_cmd)


from uuid import uuid4

for i in range(1000000000000):
    print(uuid4())
