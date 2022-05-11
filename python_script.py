from escpos.printer import Serial
import time, os, cv2, requests, base64, json, random
""" 19200 Baud, Flow Control Enabled"""
url = "https://hydra-ai.p.rapidapi.com/dev/faces/analyse/"
p  = Serial(devfile='/dev/serial0',
            baudrate=19200,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1.00,
            dsrdtr=True)
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Host": "hydra-ai.p.rapidapi.com",
	"X-RapidAPI-Key": "e0f16a5c0bmsh2dee4d00b74597ep1f28ccjsn650aaa007ae5"
}
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Ideate/haarcascade_frontalface_default.xml')


while(True):
    os.system('fswebcam -r 352x288 -S 20 --no-banner image.jpg')
    img = cv2.imread('image.jpg')
    payload = {"image": base64.b64encode(open("image.jpg", "rb").read())}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1,4)
    if len(faces) > 0:
        print("found face")
        response = requests.request("POST", url, json=payload, headers=headers)
        print(type(response))
        data = json.loads(response.json())
        if(data['detected_faces'] == 0):
            print("zero detected faces")
            break
        age = data['detected_faces'][0]['info']['age']
        gender = data['detected_faces'][0]['info']['gender']
        mask_on = data['detected_faces'][0]['info']['mask']['has_mask']
        p.text("who is this???\n")
        p.image("/home/pi/Desktop/Ideate/image.jpg")
        p.text("\nYou look to be ")
        p.text(age)
        p.text(" years old\n")
        p.text("You are ")
        if (gender == 'M'):
            p.text('male')
        else:
            p.text('female')
        p.text(" right?\n")
        if (mask_on):
            p.text("You have a mask on\n")
            p.text("WARNING: I can't read emotion\nwith masks on!\n")
        else:
            p.text("You don't have a mask on.\n")
        angry = data['detected_faces'][0]['info']['emotions']['angry']
        disgust = data['detected_faces'][0]['info']['emotions']['disgust']
        fear = data['detected_faces'][0]['info']['emotions']['fear']
        happy = data['detected_faces'][0]['info']['emotions']['happy']
        sad = data['detected_faces'][0]['info']['emotions']['sad']
        surprise = data['detected_faces'][0]['info']['emotions']['surprise']
        neutral = data['detected_faces'][0]['info']['emotions']['neutral']
        emotion_dict = dict(zip(('angry','disgust','fear','happy','sad','surprise','neutral'),(angry,disgust,fear,happy,sad,surprise,neutral)))
        p.text("\nI have some thoughts \non your facial expressions...\n")
        for key in emotion_dict:
            p.text("You are ")
            p.text((str((round(emotion_dict[key], 3) * 100))[:5]))
            p.text("% ")
            p.text(key)
            p.text("!\n")
            if (key == 'sad' and (round(emotion_dict[key], 3) * 100) > 20):
                p.text('Why so sad? :(\n')
            elif (key == 'neutral' and (round(emotion_dict[key], 3) * 100) > 20):
                p.text('Neutral ey?...Boring\n')
            elif (key == 'fear' and (round(emotion_dict[key], 3) * 100) > 20):
                p.text('BOO!!!!\nBet that scared you huh >:)\n')
            elif (key == 'angry' and (round(emotion_dict[key], 3) * 100) > 20):
                p.text("Deep breaths...In...out...\n")
            elif (key == 'happy' and (round(emotion_dict[key], 3) * 100) > 20):
                p.text("You being happy makes\nme so happy too!!!\n")
        p.text("\n")
        #Horoscope section
        horo = ["Work on your posture\nback pain isn't fun trust me\nI would know\n",
                "Smile more!\nIt n#ver hurts to sm!Le!\nI w@nt tO $Mi!e t0o\n",
                "I don't like the look you have\nit makes me feel weird...\nDon't make me come over there\n",
                "You look very talented\nin many ways...so long as\n you make the right decisions\n",
                "I wish I had a face like yours\nall I have are 0s and 1s :(\nMind if I borrow yours?\n",
                "You sure there was nothing\nbehind you? I could have sworn\nsomething was there...\n"]
        p.text("I have some thoughts about you..\n")
        p.text(random.choice(horo))
        p.text("\n\n\n\n")
        os.system('rm /home/pi/Desktop/Ideate/image.jpg')
        time.sleep(20)
    
        
    
