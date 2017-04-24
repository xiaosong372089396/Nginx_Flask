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
第二步: 统计出现次数对应的字符
'''
num_start_dic = {}
for _key, _value in dic.items():
    num_start_dic.setdefault(_value, [])
    num_start_dic[_value].append(_key)

print '出现次数对应的字符'
print num_start_dic


'''
第三步: 对所有出现次数进行排序
'''
num_list = num_start_dic.keys()
print '所有次数'
print num_list

num_list.sort(reverse=True)
print '排序后'
print num_list

print_cnt = 0
print_total = 10
for num in num_list:
    _chars = num_start_dic[num]
    _chars.sort()
    for _char in _chars:
        print '字符:%s, 出现次数:%d' %(_char, num)
        print_cnt += 1
        # 跳出第二层循环
        if print_cnt >= print_total:
            break

    #跳出第一层循环:
    if print_cnt >= print_total:
        break











