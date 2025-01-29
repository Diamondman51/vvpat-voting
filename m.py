# import random

# class M:
#     mem = [[str(random.randint(0, 9)) for _ in range(10)] for _ in range(3)]

#     def get(self):
#         r = random.choice(self.mem)
#         M.mem.remove(r)
#         print(self.mem)
#         return r

# m_1 = M()
# m_2 = M()
# m_3 = M()
# m_4 = M()

# m_1.req = 2
# print(m_1.req)
# m_1.get()
# m_2.get()
# m_3.get()
# m_4.get()



import time


for i in range(60000000):
    # time.sleep(1)
    # print(i, )
    # time.sleep(1)
    print(f"Hello {i}", end='\r')