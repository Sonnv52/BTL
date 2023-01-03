from flask import Flask, render_template, request, jsonify
knowledgeBaseFile = ".\data\knowledge.json"
clauseBaseFile = ".\data\clause.json"
from model.knowledge import Knowledge
from parsers.clauseParser import ClauseParser
from parsers.knowledgeParser import KnowledgeBaseParser
"""-------------------------------------------Logic----------------------"""
knowlages = KnowledgeBaseParser()
clauses = ClauseParser()
knowlageBase = knowlages.getKnowledgeBase(knowledgeBaseFile)
clauseBase = clauses.getClauseBase(clauseBaseFile)
"""Khai báo"""
matchedTargets = list()
matchesRules = dict()
userInput = Knowledge()
"""Làm mới"""
def renew():
    matchedTargets.clear()
    matchesRules.clear()
    userInput.clearRules()
"""kiểm tra và thêm luật"""
def add():
    for know in knowlageBase:
        for rule in know.getRules():
            for user in userInput.getRules():
                if(rule == user):
                    matchedTargets.append(know)
                    break
    matchesRules_temp = dict()
    for matchedTarget in matchedTargets:
            match = 0
            for rule in matchedTarget.getRules():
                for userRule in userInput.getRules():
                    if rule == userRule:
                        match += 1
            matchesRules_temp[matchedTarget.getTarget()] = round((match / len(matchedTarget.getRules())) * 100)
    matchesRules_temp = sorted(matchesRules_temp.items(), key = lambda item : -item[1])
    matchesRules = matchesRules_temp
    return matchesRules
def addForPropose() :
    matchedTargets.clear()
    for know in knowlageBase:
        for rule in know.getRules():
            for user in userInput.getRules():
                if(rule == user):
                    matchedTargets.append(know)
                    break
    matchKnowledge = {}
    for matchedTarget in matchedTargets:
            match = 0
            for rule in matchedTarget.getRules():
                for userRule in userInput.getRules():
                    if rule == userRule:
                        match += 1
            matchKnowledge[matchedTarget] = round((match / len(matchedTarget.getRules())) * 100)
    return matchKnowledge
"""trả lời"""
def askQuestion(mess):
    print(mess)
    if(mess.strip() == "bye"):
        renew()
        return "Tạm biệt bạn"
    input = mess.split(",")
    for u in input:
        userInput.addRule("user",u.lower())
    
    return add()
"""Đề xuất"""
def getProposes():
    proposes = list()
    count_target = 0
    targets = list(sorted(addForPropose().items(), key=lambda item : -item[1]))
    print(targets)
    if (len(targets) >=2) :
        while (count_target < 2) :
            proposes.append(targets[count_target][0].getOneRule())
            proposes.append(targets[count_target][0].getOneRule())
            count_target +=1
    else :
        proposes.append(targets[count_target][0].getOneRule())
        proposes.append(targets[count_target][0].getOneRule())
    print(proposes)
    proposes_list = list(set(proposes))
    return proposes_list

"""-------------------------------------------Logic----------------------"""

app = Flask(__name__)
@app.route("/")
def home_1():
    return render_template('home.html')
@app.route("/ask")
def home():
    return render_template('index.html')
@app.route("/get")
def getResponse():
    message = request.args['message']
    reply = askQuestion(message)
    return jsonify(reply)
@app.route("/getPropose")
def getPropose():
    list_proposes = getProposes()
    print(list_proposes)
    return ", ".join(list_proposes)
if __name__ == "__main__":
    app.run(debug=True)