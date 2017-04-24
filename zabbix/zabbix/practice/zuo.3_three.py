#!/usr/bin/env python
# -*- coding:utf-8 -*-

read_me = ''' first of all, i want make it clear that i can not claim understanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express my understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected! '''

count_dic = {}
num = [chr(i) for i in range(ord("a"),ord("j")+1)]
dic= {}
for i in read_me:
    #遍历字符串
    count_dic.setdefault(i, 0)
    #dict中是否存在i, 没有默认值为0
    count_dic[i] += 1
    #如果dict中,i值存在，统计加1
for key,value in count_dic.items():
    #遍历字典，获取key,value值
    for o in num:
        if key == o:
            #判断dict，key是否等同序列
            dic[key] = value
            #如果相等，dict,key就是,判断存在的key,值是遍历value
print dic


####方法二：
read_me = ''' first of all, i want make it clear that i can not claim understanding this holy book in just a few weeks, and i would not dare comment on this sacred book, in addition, i don't think i can give you a full picture of the holy bible in just few words.i can not preach anything here. what i want to do here is to express my understanding by sharing two events described in this book. the fist story i want to share is abandoned tower of babel.according to the bibel,people use the same language to communicate with each other in ancient times.with the soaring vanity,they decided to build a heaven-reaching tower to show off their achievement, god knows, he change the human language into different kinds and make it difficult for people to communicate with each other,hence the failure of building tower of babel.this story tells people,never do things in selfishness, but make a life out of enternal glory.the other story,before jesus christ was crucified,he said, father,forgive them, for they know not what they do. with great love, he shouldered all the sins of people. what can we learn from this story?we live in this world thanks to the love of god, for this reanson, we should make our lives glorious to honor our god.finally,i want to sum up by saying that only if we put our lives in the eternal love of god,can we live a perfect life, and what you appealed is what god expected! '''
str1 = str(read_me)
num = [chr(i) for i in range(ord("a"), ord("j")+1)]
for i in num:print i, ':', str1.count(i)

    
