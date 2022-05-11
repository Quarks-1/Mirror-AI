import subprocess
while True:
    try:
        print("opening script")
        exec(open("/home/pi/Desktop/Ideate/python_script.py").read())
    except:
        print("ERROR")
        pass
    else:
        print("ERROR2")
        break