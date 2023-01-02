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
    
    for matchedTarget in matchedTargets:
            match = 0
            for rule in matchedTarget.getRules():
                for userRule in userInput.getRules():
                    if rule == userRule:
                        match += 1
            matchesRules[matchedTarget.getTarget()] = round((match / len(matchedTarget.getRules())) * 100)
    return matchesRules
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
    for i in matchedTargets:
       proposes.append(str(i.getOneRule()))
    proposes_set = set(proposes)
    proposes_list = list(proposes_set)
    return proposes_list[0:4]

"""-------------------------------------------Logic----------------------"""

app = Flask(__name__)
@app.route("/")
def home_1():
    return render_template('home.html')
@app.route("/ask")
def home():
    return render_template('index.html')
@app.route("/get")
def getRespone():
    message = request.args['message']
    reply = askQuestion(message)
    return jsonify(reply)
@app.route("/getPropose")
def getPropose():
    list_proposes = getProposes()
    return ", ".join(list_proposes)
if __name__ == "__main__":
    app.run(debug=True)