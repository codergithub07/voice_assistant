import speech_recognition as sr
import pyttsx3
import platform
from gtts import gTTS
import subprocess
import webbrowser
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Setting Chrome as Browser
chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

mic_list = []

def speak(text, t_rate = 165):
    # engine.setProperty('rate', t_rate)
    # engine.say(text)
    # engine.runAndWait()
    tts = gTTS(text, lang='en', slow=False)
    tts.save('audio.mp3')
    os.system('mpg321 audio.mp3')

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     mic_list.append(name)


def command():
    listener = sr.Recognizer()
    print('Taking Command')
    # if (mic_list[2] == "Headset (Phantom 850 Hands-Free"):
    #     audio_in = sr.Microphone(device_index=2)
    # else:
    #     audio_in = sr.Microphone(device_index=1)

    with sr.Microphone() as mic:        #audio_in
        listener.pause_threshold = 1
        listener.energy_threshold = 1800
        speech = listener.listen(mic)

    try:
        print("Recognizing...")
        query = listener.recognize_google(speech, language='en_in')
        print(f"Command I understood is :- {query}")
    
    except Exception as e:
        print(e)
        return 'None'
    
    return query


if __name__ == '__main__':

    speak(' Hello, I am jarvis.')
    # speak(' boll bhosdi ke kya chat-wanna hay')

    while True:
        query = command().lower()  # type: ignore

        if 'hello' in query:
            speak('Greetings....')

        elif 'go to' in query:
            query = command().lower().split()  # type: ignore
            if '.com' in query[-1]:
                webbrowser.get('chrome').open_new(query[-1])
            else:
                print(f"Can't go to {query[-1]}")

        elif 'play' in query:

            if 'play de taali' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\De Taali.mp3')
                break

            elif 'play alone to' in query or 'play alone two' in query or 'play alone 2' in query or 'play alone too' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Alone 2.mp3')
                break

            elif 'play baby' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Baby.mp3')
                break

            elif 'play bhool bhulaiyaa to title track' in query or 'play bhool bhulaiyaa two title track' in query or 'play bhool bhulaiyaa 2 title track' in query or 'play bhool bhulaiyaa too title track' in query or 'play bhul bhulaiya to title track' in query or 'play bhul bhulaiya two title track' in query or 'play bhul bhulaiya 2 title track' in query or 'play bhul bhulaiya too title track' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Bhool Bhulaiyaa 2 Title Track (320 kbps).mp3')
                break

            elif 'play brothers anthem' in query or 'play brother anthem' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Brothers Anthem - Brothers 320 Kbps.mp3')
                break

            elif 'play demons' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Demons (320 kbps).mp3')
                break

            elif 'play deva deva' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Deva Deva.mp3')
                break

            elif 'play dooriyan' in query or 'play dooriyaa' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Dooriyan (320 kbps).mp3')
                break

            elif 'play eenie meenie' in query or 'eeni meeni' in query or 'enie meenie' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Eenie Meenie.mp3')
                break

            elif 'play ek ajnabee' in query or 'ek ajnabi' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Ek Ajnabee Haseena Se Mulakat Ho Gai Full Song __ Valentine day Special (320 kbps).mp3')
                break

            elif 'play falling' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Falling.mp3')
                break

            elif 'play favourite girl' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Favorite-Girl.mp3')
                break

            elif 'ghodey pe sawaar' in query or 'ghode pe sawar' in query or 'ghode per sawar' in query:
                speak('Sir, I will need to shut down in order to let you listen this song')
                os.startfile('D:\\Songs\\Ghodey Pe Sawaar.mp3')
                break

        elif  'exit' in query:
            break