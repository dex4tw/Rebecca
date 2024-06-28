"""
    Rebecca AI
    ~ bot for domain lol
    https://github.com/dex4tw
"""
import os, sys, requests, json, asyncio, websockets, threading, toml, time
import google.generativeai as PaLM
from google.generativeai.types import HarmCategory, HarmBlockThreshold

' Configure PaLM '
os.system('cls')
print("Starting PaLM...")
# PaLM.configure(api_key="AIzaSyB4QWpn2T1TAqljyPleHGYxf1L-6j3jnWw")
PaLM.configure(api_key="AIzaSyBy-K4GJ859rVsF1uYHbwTh_2kDIh5ycBM")
Model = PaLM.GenerativeModel('gemini-1.5-flash')
Chat = Model.start_chat(history=[])
Prompt = open(os.getcwd()+"/bin/prompt.txt").read()
Jailbreak = Chat.send_message(Prompt, stream=True, safety_settings={
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
})
Jailbreak.resolve()

' Rebecca Objects '
Config = toml.load(open(os.getcwd()+"/bin/config.toml"))
AuthHeaders = {"Authorization": "Bot "+Config["Token"]}

' Reminder '
def Remind():
    print("Started reminder")
    while True:
        time.sleep(180)
        Jailbreak = Chat.send_message(Prompt, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        })
        Jailbreak.resolve()
        print("Reminded Becca")
threading.Thread(target=Remind).start()

' Init Rebecca '
os.system('cls')
async def Rebecca():
    async def send_heartbeat(Websocket):
        while True:
            await Websocket.send(json.dumps({"op": 1, "d": None}))
            await asyncio.sleep(41.25)

    async with websockets.connect("wss://gateway.discord.gg") as Websocket:
        asyncio.create_task(send_heartbeat(Websocket))
        await Websocket.send(json.dumps({'op': 2,'d': {'token': Config["Token"],'intents': 513,'properties': {'$os': 'Linux','$browser': 'None','$device': 'Ubuntu'}}}))

        while True:
            try:
                response = await Websocket.recv()
                data = json.loads(response)
                event = data.get('t')
            except:
                os.execv(sys.executable, ['py'] + sys.argv)

            ' Handle Websocket Response '
            if event == 'READY':
                print('Rebecca is up')
            elif event == "MESSAGE_CREATE":
                def respond():
                    message = data.get('d')
                    author = message["author"]
                    content = message["content"]
                    messageid = message["id"]
                    channelid = message["channel_id"]
                    guildid = message['guild_id']
                    
                    ' Blacklisting '
                    if author['id'] == "1238680815534080100":
                        return
                    if channelid not in Config["Channels"]:
                        return
                    if content == "*fix":
                        Jailbreak = Chat.send_message(Prompt, stream=True, safety_settings={
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        })
                        Jailbreak.resolve()
                        return
                    elif content == "*restart":
                        os.execv(sys.executable, ['py'] + sys.argv)
                    
                    ' Init Response '
                    try:
                        print("Responding to:", content)
                        response = Chat.send_message(f"Keep your responses a medium length\n{author['username']} says: {content}", stream=True, safety_settings={
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        })
                        response.resolve()
                        requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", json={"content": response.text, "message_reference": {'guild_id': guildid, 'channel_id': channelid, 'message_id': messageid}}, headers=AuthHeaders)
                    except PaLM.types.BrokenResponseError:
                        os.execv(sys.executable, ['py'] + sys.argv)
                    except PaLM.types.StopCandidateException:
                        print("Failed to finish response")
                    except Exception as e:
                        print(e)
                    
                threading.Thread(target=respond).start()
asyncio.run(Rebecca())