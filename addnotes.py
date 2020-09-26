import json
import urllib.request
import os

def addNotes(frontContent, backContent, deckToAdd):
    return {'action': 'addNote', 'version': 6, "params": {
        "note": {
            "deckName": deckToAdd,
            "modelName": "Basic",
            "fields": {
                "Front": frontContent,
                "Back": backContent
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck"
            }
        }
        }
    }

def invokeAddnotes(frontContent, backContent, deckToAdd):
    requestJson = json.dumps(addNotes(frontContent, backContent, deckToAdd)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']



def countwhitespace(line):
    #count the number of white spaces or indentation level
    return len(line) - len(line.lstrip(' '))


class card:
    def __init__(self):
        print("Constructing a card")

    def setQuestion(self, question):
        self.question = question
        return

    def setAnswer(self, answer):
        self.answer = answer
        return

    def getQuestion(self):
        return self.question
    def getAnswer(self):
        return self.answer
        
    def getStatus(self):
        return self.question + self.answer

#reading the file:
fileObject = open('input2105.txt',"r")
line = fileObject.readline()

#creating a list container for the cards
cardList = []

while (line != ""):
    #count the number of white spaces or indentation level
    num_whitespace = countwhitespace(line)
    #remove unnecessary stuff on the lines
    line = line.lstrip(" ")
    line = line.lstrip("-")
    # Check if it is a question (if there is a ? at the end, start the question)
    if (line.__contains__("?")):
        currentNote = card()
        currentNote.setQuestion(line)
        questionIndentation = num_whitespace
        #get the next line and check indentation
        nextLine = fileObject.readline()
        nextLineIndentation = countwhitespace(nextLine)
        answer = ''
        #parse for answers in nextlines
        while(not nextLine.__contains__("?") and nextLine != ""):
            if (nextLineIndentation - questionIndentation == 4):
                nextLine = nextLine.lstrip(" ")
                nextLine = nextLine.rstrip()
                nextLine += os.linesep
                answer += nextLine
                nextLine = fileObject.readline()
                nextLineIndentation = countwhitespace(nextLine)
            elif (nextLineIndentation - questionIndentation != 4): #what to do if the format is incorrect
                print("indentation without actual question/answer or format!")
                print("Problematic Line is: " + nextLine)
                nextLine = fileObject.readline()
                nextLineIndentation = countwhitespace(nextLine)
                continue
        currentNote.setAnswer(answer)
        cardList.append(currentNote)
        line = nextLine
    else:
        line = fileObject.readline()


for x in cardList:
    invokeAddnotes(x.getQuestion(), x.getAnswer(), "CS2105")

result = invoke('deckNames')
print('got list of decks: {}'.format(result))

#create deck if there is still other issues