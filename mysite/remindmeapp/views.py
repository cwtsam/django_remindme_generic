from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

#from RTVC import demo_cli
import random
import asyncio
import time
import wolframalpha # to calculate strings into formula 

status_variable="Null"
Rem_response=""
Rem_source=""
generic_audio = "hello"

loop=asyncio.get_event_loop()
def pushremiders(args1):
    global status_variable
    global Rem_source,Rem_response
    print("asyncio process is going on")
    #asource=demo_cli.maux(args1[1],123)
    Rem_response = args1[1]
    #Rem_source=asource  
    Rem_source = generic_audio 
    time.sleep(args1[0])
    status_variable="ready"
    print("printing argument to push")
    print(args1[1])
    print(asource)

def process_text(input): 
    try: 
        
        if 'search' in input or 'play' in input: 
            # a basic web crawler using selenium 
            x=search_web(input) 
            return x, generic_audio
        
        elif 'hi' in input or 'hello' in input or 'good morning' in input or 'hey' in input :
            speak= "Hello, how are you?"
            return speak, generic_audio
        
        elif 'how about you' in input or 'about you' in input:
            speak="Feeling good, what would you like to do?"
            return speak, generic_audio
        
        elif 'fine' in input or 'well' in input or 'good' in input or 'okay' in input or 'ok' in input:
            speak="Good to hear, what can I do for you?"
            return speak, generic_audio

        elif "define yourself" in input :
            speak='''Hello, I am KIN. A virtual assistant. You can ask me to perform 
            various tasks such as reminding you to do things, calculations and so on'''
            return speak, generic_audio
            
        elif "who are you" in input : 
            speak="Who do you think?"
            return speak,generic_audio

        elif "who made you" in input or "created you" in input: 
            speak = "I have been created by Augmented Human lab."
            return speak,generic_audio

        elif "augmented human lab" in input:# just 
            speak = """Augmented Human Lab is the Best Research Lab."""
            return speak,generic_audio

        elif "calculate" in input.lower(): 
            
            # write your wolframalpha app_id here 
            app_id = "2VJHAQ-WKWG7K755R"
            client = wolframalpha.Client(app_id) 

            indx = input.lower().split().index('calculate') 
            query = input.split()[indx + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text 
            
            return "The answer is "+answer,generic_audio
        
        elif 'weather' in input:
            speak="Sunny but it’s not a good idea to go out now"
            return speak,generic_audio
        
        elif 'shakespeare' in input:
            speak="To be or not to be, that is the question..."
            return speak,generic_audio
        
        elif 'play' in input and 'song' in input:
            speak="Playing a song for you"
            return speak,generic_audio
        
        elif 'remind me' in input:
            global text1
            text1=input
            chat_response= "In how many minutes?"
            return chat_response,generic_audio
        
        elif 'minutes' in input or 'minute' in input:
            chat_response= "Okay I'll remind you buddy"
          
            str1=input
            tim = [int(s) for s in str1.split() if s.isdigit()]
            print(tim[0])
            print("global text :"+ text1)

            indx=text1.lower().replace("remind me","Hey reminding you")
            #indx="hey reminding you"
            print(indx)
            args1=[tim[0]*30,indx]
            
            loop.run_in_executor(None,pushremiders,args1)
          
            return chat_response,generic_audio
        
        elif "good night" in input or "bye" in input or "good bye" in input:
            return "See you later",generic_audio
        
        elif "thank" in input:
            return "You're welcome",generic_audio

        else:
            
            return "Say that again?","hello"

    except :
        
        return "Invalid Conversation","hello"

def search_web(Output): 
    
    if 'youtube' in Output.lower(): 
        
        indx = Output.lower().split().index('youtube') 
        query = Output.split()[indx + 1:] 
        x="http://www.youtube.com/results?search_query =" + '+'.join(query) 
        return x
    
    elif 'wikipedia' in Output.lower(): 
         
       
        indx = Output.lower().split().index('wikipedia') 
        query = Output.split()[indx + 1:] 
        x="https://en.wikipedia.org/wiki/" + '_'.join(query)
        return x
    
    else: 
        if 'google' in Output: 
            indx = Output.lower().split().index('google') 
            query = Output.split()[indx + 1:] 
            x="https://www.google.com/search?q =" + '+'.join(query)
            return x
            
        elif 'search' in Output: 
            indx = Output.lower().split().index('google') 
            query = Output.split()[indx + 1:] 
            x="https://www.google.com/search?q =" + '+'.join(query)
            return x 

        else: 

            x="https://www.google.com/search?q =" + '+'.join(Output.split()) 

        return x
        

def Chatbot(text):
    chatresponse,audio_source=process_text(text)
    return chatresponse,audio_source

def home(request, template_name="home.html"):
    context = {'title': 'KIN'} ## passes context to template home.html
    return render(request, template_name, context) ## allow rendering of the home page

@csrf_exempt
def get_response(request):
    response = {'status': None}
    global status_variable
    global Rem_source,Rem_response

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        print("frontend fetch reminder response")
        print(message)
        message=message.lower()
        #m1=data[]
        #print("this is message.reminded")
        #print(message.reminded)
        if status_variable=="ready" and message == "remindercheck_false":
    
            chat_response=Rem_response
            audio_source=Rem_source
            #chat_response="reminderminder"
            #audio_source = "hello"
            print("Printing Ready reminder variables inside post request :")
            print(chat_response)
            print(audio_source)

            response['message'] = {'reminder': True,'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
            response['status'] = 'ok'

        elif message == "remindercheck_true":
            chat_response="backend reminded"
            audio_source="hello"
            response['message'] = {'reminder': False,'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
            response['status'] = 'ok'
            status_variable = "Null"
                        
        else:
            #data = json.loads(request.body.decode('utf-8'))
            #message = data['message'] # string message from user
            #print(message)
            print("normal chat request")
            chat_response,audio_source=Chatbot(message)
            #chat_response="hello THERE"
            #audio_source = demo_cli.maux(chat_response,176)
            #audio_source = "demo_output_1651651"
            print(chat_response)
            print(audio_source)
            response['message'] = {'reminder': False,'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
            response['status'] = 'ok'
            status_variable = "Null"

    else:
        response['error'] = 'no post data found'

    return HttpResponse(json.dumps(response), content_type="application/json") 
             

           
            
            

