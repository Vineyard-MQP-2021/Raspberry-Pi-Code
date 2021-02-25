import os

switcher = {
    "1": "hawk1.wav",
    "2": "hawk2.wav",
    "3": "hawk3.wav",
    "4": "hawk4.wav"
}

with open("cycler.txt", "r+") as f:
    num = f.read()
    file = switcher.get(num, None)
    url = 'sounds/' + file
    os.system('vlc %s vlc://quit &' % url)
    new_num = str(int(num) + 1)
    if new_num == "5":
        new_num = "1"
    f.seek(0)
    f.write(new_num)
    f.truncate()
    f.close()
