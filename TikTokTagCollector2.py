from TikTokApi import TikTokApi
from nested_lookup import nested_lookup
import itertools
import collections
import re

from flask import Flask, render_template, request, json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def variables():
    global results
    global api
    global posts
    results = 5 #How many posts should be scanned?
    api = TikTokApi.get_instance()
    posts = api.trending(count=results, custom_verifyFp="")
    return(results, api, posts)

def average(list1):
    return(sum(list1)/len(list1))

@app.route('/getTrendingTags', methods=['GET'])
def getTrendingTags():
    variables()

    diggWeight = 1
    shareWeight = 1
    commentWeight = 1
    playWeight = 1
    authorFollowerCountWeight = 50
    tagList = []
    trafficList = []
    sortedList = {}
    finishedTagList = []
    
    for post in posts:
        #Collect post followers and stats
        authorFollowerCount = (nested_lookup('followerCount', post)[0])**(1 / authorFollowerCountWeight)
        diggCount = nested_lookup('diggCount', post)
        shareCount = nested_lookup('shareCount', post)
        commentCount = nested_lookup('commentCount', post)
        playCount = nested_lookup('playCount', post)
        
        #Make lists based on tags, traffic, videoduration
        tags = nested_lookup('hashtagName', post)
        tagList.append(tags)
        traffic = round((sum(diggCount * diggWeight +
                       shareCount * shareWeight +
                       commentCount * commentWeight +
                       playCount) * playWeight) * authorFollowerCount, 2)
        trafficList.append(traffic)
    #Combine the different lists into one dictionary
    t = 0
    #print('\n')
    for i in trafficList:
        sortedList[i] = tagList[t]
        #print(i, sortedList[i], '\n')
        t += 1
    sortedList2 = {}
    #For hvert tag som hvert object, skal der laves nye lister for hvert tag
    #(j og i + t er byttet om for at lave dataene mere praktiske)
    for i in sortedList:
        t = 0
        for j in [*sortedList[i]]:
            sortedList2[j] = i + t
            t += 1

    res = {}
    for i in sortedList2:
        if i in res:
            #Tilføj i's værdi til i
            res[i] += sortedList2.values()[i]
        else:
            #Tilføj i til listen
            res[i] = sortedList2[i]
    res = dict(sorted(res.items(), key=lambda item: item[1]))
    for i in res:
        if i != None and i != "":
            finishedTagList.append(str("#" + i + " "))
    #Print result
    for x in range(len(finishedTagList)): 
        print(finishedTagList[x], end='')
    return(json.dumps(res))

@app.route('/getDuration', methods=['POST'])
def getDuration():
    variables()
    durationList = []
    for post in posts:
        durations = nested_lookup('duration', post)
        durationList.append(average(durations))
    print(average(durationList))
    return(average(durationList))

@app.route('/getRatio', methods=['GET'])
def getRatio():
    variables()
    ratioList = []
    for post in posts:
        ratio = nested_lookup('ratio', post)
        t = 0
        for i in ratio:
            ratio[t] = re.sub('\D', '', ratio[t])
            t += 1
        ratioList.append(int(ratio[0]))
    print(average(ratioList))
    return(average(ratioList))

@app.route('/getSignature', methods=['GET'])
def getSignature():
    variables()
    signatureList = []
    for post in posts:
        signature = nested_lookup('signature', post)
        signatureList.append(signature)
    for x in range(len(signatureList)):
        for j in signatureList[x]:
            print(j, end='')
    return(average(signatureList))

if __name__=="__main__":
    app.run()

"""
getTrendingTags()

print("\n")
getDuration()
print("\n")
getRatio()
print("\n")

getSignature()
print("\n")"""
