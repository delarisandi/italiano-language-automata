#LEXICAL ANALYZER FINITE AUTOMATA ITALIAN LANGUAGE
#AUTHOR : STEVAN DEL ARISANDI
import string


#FA class
class FiniteAutomata:
    #self constructor
    def __init__(self, totalState):
        self.listGrammar = []
        self.totalState = totalState
        self.listState = []
        self.listTransition = {}


    #define all q0...qn state
    def initiateState(self):
        for i in range(self.totalState):
            numState = str(i)
            self.listState.append('q'+numState)

        return self.listState


    #define default q0...qn & a-z transition
    def initiateTransition(self):
        #initiate character a-z
        listCharacter = list(string.ascii_lowercase)
        #define for all state & character a-z + # and space
        for state in self.listState:
            for char in listCharacter:
                self.listTransition[(state, char)] = 'error'
            self.listTransition[(state,'#')] = 'error'
            self.listTransition[(state,' ')] = 'error'

        #define space character input in q0 in qn
        self.listTransition[('q0', ' ')] = 'q0'
        self.listTransition[('q'+str(self.totalState-1), ' ')] = 'q'+str(self.totalState-1)

        return self.listTransition


    #define all transition based on CFG
    def assignTransition(self, grammar):
        #begin with q0
        currentNum = 0
        nextNum = currentNum + 1
        grammar = grammar.lower()+' #'

        #define all transition per character based on grammar input
        for i in range(len(grammar)):
            #read first character based on grammar input condition
            if i==0:
                if (grammar[i]=='p'):
                    nextNum = 3
                elif (grammar[i]=='m'):
                    nextNum = 8
                elif (grammar[i]=='f'):
                    nextNum = 13
                elif (grammar[i]=='c'):
                    nextNum = 16
                elif (grammar[i]=='s'):
                    nextNum = 30
                elif (grammar[i]=='g'):
                    nextNum = 39
                elif (grammar[i]=='v'):
                    nextNum = 45
                elif (grammar[i]=='a'):
                    nextNum = 49
                firstNum = nextNum
                firstChar = grammar[i]

            #read next or last character based on grammar input condition
            #ends with 'a'
            if (grammar=='pizza #' and i==1):
                nextNum = 9
            elif (grammar=='chiesa #') or (grammar=='chitarra #') or (grammar=='storia #'):
                if ((grammar=='chiesa #' or grammar=='storia #') and i==4) or (grammar=='chitarra #' and i==6):
                    nextNum = 11
                elif (grammar=='chitarra #' and i==3):
                    nextNum = 20

            #ends with 'e'
            elif (grammar=='madre #') or (grammar=='mangiare #') or (grammar=='visitare #') or (grammar=='acquistare #'):
                if ((grammar=='mangiare #' or grammar=='visitare #') and i==5) or (grammar=='acquistare #' and i==7):
                    nextNum = 5
                #starts with 'ma' (special condition)
                elif ((grammar=='mangiare #' or grammar=='madre #') and i==1):
                    nextNum = 4 
                #ends with 'tare'
                elif (grammar=='visitare #' and i==4) or (grammar=='acquistare #' and i==6):
                    nextNum = 44
                #ends with 'are'
                elif (grammar=='mangiare #' and i==2):
                    nextNum = 42 
                elif (grammar=='acquistare #' and i==5):
                    nextNum = 48

            #ends with 'io'
            elif (grammar=='calcio #'):
                if i==1:
                    nextNum = 28
                elif i==3:
                    nextNum = 0

            #ends with 'o'
            elif (grammar=='fungo #') or (grammar=='colosseo #') or (grammar=='studiando #') or (grammar=='giocando #'):
                if (grammar=='fungo #' and i==3) or (grammar=='studiando #' and i==7) or ((grammar=='colosseo #' or grammar=='giocando #') and i==6):
                    nextNum = 1
                elif (grammar=='studiando #' and i==2):
                    nextNum = 34
                elif (grammar=='colosseo #' and i==1):
                    nextNum = 23
                elif (grammar=='giocando #' and i==3):
                    nextNum = 36

            #read space character condition    
            if (grammar[i]==' '):
                nextNum = self.totalState-1

            #define the current & next state to string
            currentState = 'q'+str(currentNum)
            nextState = 'q'+str(nextNum)

            #read the last character '#' of grammar input  condition
            if (grammar[i]=='#'):
                self.listTransition[(currentState, grammar[i])] = 'accept'
                self.listTransition[(currentState, firstChar)] = 'q'+str(firstNum)
            else:
                self.listTransition[(currentState, grammar[i])] = nextState

            #increment for next state iteration
            currentNum = nextNum
            nextNum = nextNum + 1

        return self.listTransition


#analyze grammar input on main based on transition list
def lexicalAnalyze(inputItaliano, inputGrammar, transition):
    #start with q0 state
    stateNow = 'q0'
    grammarNow = ''
    i = 0
    totalWord = 0
    #loop until reach the accept state
    while stateNow != 'accept':
        #read grammar input per character and store to variable
        charNow = inputGrammar[i]
        grammarNow += charNow
        prevState = stateNow

        #check if input is alphabet a-z or space only
        if (charNow in list(string.ascii_letters) or charNow==' ' or charNow=='#'):
            stateNow = transition[(stateNow, charNow)]
        else:
            message = 'Characters Input not Valid! Input must be Alphabet or Space Characters!'
            return message

        #trace all inputs per iteration
        print(' Trace :')
        print(' - Current Word --> ',grammarNow)
        print(' - Current State --> ',prevState)
        print(' - Current Char --> ', charNow)
        print(' - Next State --> ',stateNow,'\n')

        #reach the accepted state condition
        if stateNow=='q2' or stateNow=='q7' or stateNow=='q12':
            totalWord = totalWord+1
            print('+ Word ',totalWord,' Check = ',grammarNow,' --> Valid \n')
            grammarNow = ''
        #abort if not
        elif stateNow == 'error':
            totalWord = totalWord+1
            print('+ Word ',totalWord,' Check = ',grammarNow,' --> not Valid \n')
            break
        #increment for next character iteration
        i = i+1

    #final analyze
    if stateNow =='accept':
        message = 'Final Word(s) Check : {} --> Valid'.format(inputItaliano)
    else:
        message = 'Final Word(s) Check : {} --> not Valid'.format(inputItaliano)
    
    return message


#main function
if __name__ == "__main__":
    #initiate FA Class
    LexicalFA = FiniteAutomata(55)
    #initiate all known grammar
    LexicalFA.listGrammar = ['io', 'padre', 'madre', 'pizza', 'fungo', 'chiesa', 'chitarra', 'colosseo', 'calcio', 'storia',
                            'studiando', 'giocando', 'mangiare', 'visitare', 'acquistare']

    #execute method on FA Class
    state = LexicalFA.initiateState()
    transition = LexicalFA.initiateTransition()
    #assign transition for all grammar in list
    for grammar in LexicalFA.listGrammar:
        transition = LexicalFA.assignTransition(grammar)

    #input
    inputItaliano = ''
    print('LEXICAL ANALYZER FINITE AUTOMATA ITALIAN LANGUAGE')

    def help():
        print('Command List :')
        print('*to Show Grammar Dictionary                                      : type -> dictionary')
        print('*to Testing the Program with Example of Valid and non-Valid Words: type -> test')
        print('*to Exit program                                                 : type -> exit')


    #loop for input until exit
    while (inputItaliano!=exit):
        print('----------------------------------------')
        print('*to Show Command List : type -> help \n')
        inputItaliano = input('Input Italiano Word(s) : ')
        print('----------------------------------------')
        
        if (inputItaliano=='exit'):
            break
        print('Output : \n')

        if (inputItaliano=='dictionary'):
            print('*Grammar Dictionary :')
            print(LexicalFA.listGrammar,'\n')
            inputItaliano = ''
        elif (inputItaliano=='help'):
            help()
        elif (inputItaliano=='test'):
            print('*Valid Words Example :')
            defaultTesting = lexicalAnalyze('io giocando calcio', 'io giocando calcio #', transition)
            print(defaultTesting,'\n')

            print('*non-Valid Words Example :')
            defaultTesting = lexicalAnalyze('voi cucinando spaghetti', 'voi cucinando spaghetti #', transition)
            print(defaultTesting,'\n')
        else:     
            #convert to lexical format --> 'string #'
            inputGrammar = inputItaliano.lower()+" #"

            #lexical analyze
            finalAnalyze = lexicalAnalyze(inputItaliano, inputGrammar, transition)
            print(finalAnalyze,'\n')
