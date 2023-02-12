import openai
import myConfig
import json

# parameters
online = True
verbose = False
openai.api_key = myConfig.getApiKey()
model_engine = "text-davinci-002"
introQuestion = "I am hungry and I would like to have a "
endQuestion = ". What can recipe can you suggest based upon the ingredients in my fridge?"


def responseMock(fp):
    with open(fp) as myJson:
        tmp = json.load(myJson)
        if isinstance(tmp, dict):
            return tmp
        else:
            return "error: " + fp + " is returned as a " +  type(tmp) + " instead of dict"


def fridge2text(verbose=False):
    myFridge = myConfig.myFridge()
    nbrFridgeItems = len(myFridge)
    myStock = "I have the following " + str(nbrFridgeItems) + " ingredients available: "
    cnt = 0
    for f in myFridge:
        cnt += 1
        if cnt < len(myFridge) - 1:
            myStock += f + ", "
        else:
            if cnt == len(myFridge) - 1:
                myStock += f + " and "
            else:
                myStock += f + "."
    return myStock


def processResponses(myObj={}, verbose=False):
    responses=[]
    nbrResponses = len(myObj.get("choices"))
    if verbose:
        print(f"nbr of responses is {nbrResponses} ")
    for r in myObj.get("choices"):
        # responses = myObj.get("choices")[0]
        if verbose:
            print("r: ", r)
        responses.append(r.get("text"))
    return responses

# prepare request
myStock = fridge2text(verbose)
print(f"\n{myStock}\n")
prompt = myStock + " " + introQuestion + input("Describe the kind of meal you want? ") + endQuestion

# send request and get response
if online:
    try:
        fullResponse = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            temperature=0.5,
        )
    except:
        print("error connecting")
        cnt = False
        cnt = input("Do you want to switch to mock data? ")
        print(cnt)
        if cnt:
            print("!! continuing with mock data - no real response")
            fullResponse = responseMock("chatGptMockResponse.json")
        else:
            print("chatgpt cannot be reached. not possible to continue")
            exit(400)
else:
    fullResponse = responseMock("chatGptMockResponse.json")


# process the response
responses = processResponses(fullResponse,verbose)
for response in responses:
    if verbose:
        print("hi chatgpt, " + prompt)
        print(type(response))
    print(response)



