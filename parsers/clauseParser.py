

import json
import os

from model.clause import Clause



class ClauseParser:


    def __init__(self):
        self.__clauses = list()

    def __parseInputFile(self, inputFile):
        # checking if the input file exists
        if os.path.isfile(inputFile) is False:
            return "notfoud"

        # reading the file
        with open(inputFile, "r", encoding="utf-8") as file:
            file = json.load(file)

            # reading the que and ans, appending to a list
            for clause in file:
                cl = Clause()
                cl.addClause(
                    clause=file[clause]['question'],
                    negative=file[clause]['answer']['negative'],
                    positive=file[clause]['answer']['positive']
                )
                self.__clauses.append(cl)

        return self.__clauses

    def getClauseBase(self, inputFile):
        return self.__parseInputFile(inputFile)
