from dataclasses import field
import os
import time

# # print(os.path.abspath(os.path.dirname(__file__) + 'upload/' + str(time.time())))

# file = open(os.path.abspath(os.path.dirname(__file__) + 'uploadfiles/' + str(time.time())), 'w+')
# file.write('hhhhh')
# file.close()

uploads = os.path.abspath(os.path.dirname(__file__))
print(uploads)