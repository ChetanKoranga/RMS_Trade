import queue

data = [1,2,3,4,67,5,2,2343,5656]

que = queue.Queue(maxsize=0)
for i in data:
    que.put(i)



print(que.qsize())
# print(que)

c = que.get()
print(c)

print(que.qsize())