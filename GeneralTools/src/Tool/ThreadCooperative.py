# -*- coding:utf8 -*-


import time
from threading import Thread
from threading import Event
from threading import Condition
from queue import Queue

'''
# 重置event，使得所有该event事件都处于待命状态
event.clear()

# 等待接收event的指令，决定是否阻塞程序执行
event.wait()

# 发送event指令，使所有设置该event事件的线程执行
event.set()
'''
class ThreadEvent(Thread):
    def __init__(self, name, event):
        super().__init__()
        self.name = name
        self.event = event

    def run(self):
        print('Thread: {} start at {}'.format(self.name, time.ctime(time.time())))
        # 等待event.set()后，才能往下执行
        self.event.wait()
        print('Thread: {} finish at {}'.format(self.name, time.ctime(time.time())))


def TestEvent():
    threads = []
    event = Event()

    # 定义五个线程
    [threads.append(ThreadEvent(str(i), event)) for i in range(1,5)]

    # 重置event，使得event.wait()起到阻塞作用
    event.clear()

    # 启动所有线程
    [t.start() for t in threads]

    print('等待5s...')
    time.sleep(5)

    print('唤醒所有线程...')
    event.set()


'''
# 类似lock.acquire()
cond.acquire()

# 类似lock.release()
cond.release()

# 等待指定触发，同时会释放对锁的获取,直到被notify才重新占有琐。
cond.wait()

# 发送指定，触发执行
cond.notify()
'''

class Hider(Thread):
    def __init__(self, cond, name):
        super(Hider, self).__init__()
        self.cond = cond
        self.name = name

    def run(self):
        time.sleep(1)  #确保先运行Seeker中的方法
        self.cond.acquire()

        print(self.name + ': 我已经把眼睛蒙上了')
        self.cond.notify()
        self.cond.wait()
        print(self.name + ': 我找到你了哦 ~_~')
        self.cond.notify()

        self.cond.release()
        print(self.name + ': 我赢了')


class Seeker(Thread):
    def __init__(self, cond, name):
        super(Seeker, self).__init__()
        self.cond = cond
        self.name = name

    def run(self):
        self.cond.acquire()
        self.cond.wait()
        print(self.name + ': 我已经藏好了，你快来找我吧')
        self.cond.notify()
        self.cond.wait()
        self.cond.release()
        print(self.name + ': 被你找到了，哎~~~')


def TestCondition():
    cond = Condition()
    seeker = Seeker(cond, 'seeker')
    hider = Hider(cond, 'hider')
    seeker.start()
    hider.start()



'''
# maxsize默认为0，不受限，一旦>0，而消息数又达到限制，q.put()也将阻塞
q = Queue(maxsize=0)

# 阻塞程序，等待队列消息。
q.get()

# 获取消息，设置超时时间
q.get(timeout=5.0)

# 发送消息
q.put()

# 等待所有的消息都被消费完
q.join()

# 以下三个方法，知道就好，代码中不要使用

# 查询当前队列的消息个数
q.qsize()

# 队列消息是否都被消费完，True/False
q.empty()

# 检测队列里消息是否已满
q.full()
'''

class Student(Thread):
    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue

    def run(self):
        while True:
            # 阻塞程序，时刻监听老师，接收消息
            msg = self.queue.get()
            # 一旦发现点到自己名字，就赶紧答到
            if msg == self.name:
                print("{}：到！".format(self.name))


class Teacher:
    def __init__(self, queue):
        self.queue=queue

    def call(self, student_name):
        print("老师：{}来了没？".format(student_name))
        # 发送消息，要点谁的名
        self.queue.put(student_name)


def TestQueue():
    queue = Queue()
    teacher = Teacher(queue=queue)
    s1 = Student(name="小明", queue=queue)
    s2 = Student(name="小亮", queue=queue)
    s1.start()
    s2.start()

    print('开始点名~')
    teacher.call('小明')
    time.sleep(1)
    teacher.call('小亮')



if __name__ == '__main__':
    TestCondition()