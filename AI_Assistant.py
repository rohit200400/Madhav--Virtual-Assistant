from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# speech engine initialization
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id) # 0-Male  1-Female
activationWord = 'computer' # single word

# configure browser 
# # Set path
browserPath = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
webbrowser.register('brave',None, webbrowser.BackgroundBrowser(browserPath))

# Wolfram Alpha client
appId = 'TY787T-Q2J3KG7QP8'
wolframClient = wolframalpha.Client(appId)

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def speak(text,rate=120):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()

def search_wikipedia(search =''):
    searchResults = wikipedia.search(search)

    if not searchResults:
        print('No result in wikipedia.')
        return 'No result recived from wikipedia.'
    try: 
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])

    print(wikiPage.title)
    summary = str(wikiPage.summary)
    return(summary)

def search_wolframalpha(keyword=''):
    response = wolframClient.query(keyword)
  
    # @success: Wolfram Alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods

    # Query not resolved
    if response['@success'] == 'false':
        speak('I could not compute')
    # Query resolved
    else: 
        result = ''
        # Question
        pod0 = response['pod'][0]
        # May contain answer (Has highest confidence value) 
        # if it's primary or has the title of result or definition, then it's the official result
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove bracketed section
            return result.split('(')[0]
        else:
            # Get the interpretation from pod0
            question = listOrDict(pod0['subpod'])
            # Remove bracketed section
            question = question.split('(')[0]
            # Could search wiki instead here? 
            return question


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for Command')
    speak('Listening for command')

    with sr.Microphone() as source:
        listener.pause_threshold = 1
        input_speech = listener.listen(source)
        print('Microphone block')

    try:
        print('Reconizing speech...')
        query = listener.recognize_google(input_speech,language='hn')
        print(f'The input query was: {query}')
    except Exception as exception:
        print('Please repeate. I didn\'t catch that.')
        speak('Please repeate. I didn\'t catch that.' )
        print(exception)
        return 'None'
    return query

# Main loop 
if __name__ == '__main__':
    speak('Hello World')

    while True:

        query =parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)
            if len(query)==0 : break
        if query[0] == 'say':
            query.pop(0)
            if  'hello' in query:
                speak ('Greetings All')
            else:
                query.pop(0)
                speech = ' '.join(query)
                speak(speech)
        
        # Navigation to browser 
        if query[0]== 'go' and query[1] == 'to':
            speak('Opening...')
            search = ' '.join(query[2:])
            webbrowser.get('brave').open_new(search)

        # Wikipedia
        if query.count('wikipedia')>0:
            search = ' '.join(query[query.index('wikipedia'):])
            speak('searching wikipedia.')
            result =  search_wikipedia(search)
            speak(result)

        # Wolfram Alpha - computational engine
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to compute')
        
        # exiting the application
        if query[0] == 'exit':
            break
