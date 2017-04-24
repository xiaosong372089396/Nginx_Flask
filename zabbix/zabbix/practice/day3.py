#!/usr/bin/env python
# -*- coding:utf-8 -*-

read_me = ''' first of all, i want make it clear that i can not claim understanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express my understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected! '''

dic = {}
for i in read_me:
    dic.setdefault(i,0)
    dic[i] += 1

print "每个字符对于的次数"
print dic



'''
第二步:dict => list
'''
dic_list = dic.items()


'''
第三步:list, 冒泡
1,tuple 可以进行比较的
2,可以用元组中的某个元素代码元组,和其他元组比较
'''
for j in range(len(dic_list) - 1):
    for i in range(len(dic_list) - 1):
        if dic_list[i][1] > dic_list[i + 1][1]:
            #a,b = b,a
            dic_list[i], dic_list[i + 1] = dic_list[i + 1],dic_list[i]

'''
拿出TOP 10
'''
print dic_list[-1:-11:-1]

'''
1,获取每个字符对应的次数
2,获取列表
3,队列表排序(冒泡排序)
4,拿出TOP 10
5,冒泡排序优化
6,TOP N的优化
7,TOP N有相同数量的字符的优化
'''
