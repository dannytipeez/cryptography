
try:
    import twint, time, datetime, pyAesCrypt, os
except ImportError as e:
    print("Failed importing module.." + str(e))

filePath = "/home/chi3f/dannywrld/python/secret.txt"

# This is the payload function
def FirePayload(filePath, encryptPass):
    print("ACTIVATED PAYLOAD!!!")
    bufferSize = 64 * 1024 # encryption/decryption buffer
    pyAesCrypt.encryptFile(filePath, (filePath+'.aes'), encryptPass, bufferSize) #encrypt
    print("File encryption completed!")
    #pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", password, bufferSize)  decrypt
    try:
        os.remove(filePath)
    except OSError:
        print("Error occured")
    
    print("SWITCH ACTIVATED - LOCKDOWN MODE ENTERED")
    exit()

# Checks for the keyphrase on Twitter, checks if the time is up
def CheckKey(c, delayTime, filePath, encryptPass, targetTime):
    try:
        twint.run.Search(c)
    except ValueError:
        print("Something bad happen")
        GetTargets()
    tweets = twint.output.tweets_list
    if not tweets:
        if (time.time() >= targetTime): FirePayload(filePath, encryptPass)
        else:
            print("No results, trying again after delay")
            time.sleep(delayTime)
            CheckKey(c, delayTime, filePath, encryptPass, targetTime)
    else:
        print("Deadswitch De-Activated, Entered Safe Mode")
        exit()

# Gets the information to run the loop, such as the keyword, file to encrypt, and how long to run
def GetTargets():
    c = twint.Config()
    startTime = input("Date to start searching (format: %Y-%m-%d)\n>")
    try: datetime.datetime.strptime(startTime, '%Y-%m-%d')
    except ValueError:
        print("That's not a date, try again (format: %Y-%m-%d)")
        GetTargets()
    c.Since = startTime
    c.Search = input("Keyphrase to disarm switch?\n>")
    c.Username = input("Twitter account to watch?\n>")
    delayTime = int(input("Time in seconds to wait between checking the account?\n>"))
    #filePath = input("File to encrypt if switch fires?\n>")
    encryptPass = input("Password to encrypt file?\n>")
    targetTime = (time.time() + (int(input("How many minutes to run before firing?\n>"))*60))
    c.Hide_output = True
    c.Store_object = True
    CheckKey(c, delayTime, filePath, encryptPass, targetTime)

GetTargets()
