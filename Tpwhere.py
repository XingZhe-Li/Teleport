import os
import sys
import json

root = os.path.dirname(__file__)
def renewjson():
    f = open(root+'/destinations.json','w')
    f.write("{\"back\":true,\"destinations\":{}}")
    f.close()

def writejson(obj):
    x = json.dumps(obj)
    f = open(root+'/destinations.json','w')
    f.write(x)
    f.close()

def writeback():
    f = open(root+'/backwhere','w')
    f.write(os.getcwd())
    f.close()

def writetp(text):
    f = open(root+'/Lasttp.cmd','w')
    f.write(text)
    f.close()

def jumpback():
    f = open(root+'/backwhere','r')
    x = f.read()
    f.close()
    writeback()
    writetp("@cd /d \""+x+"\"")

# Clean Lasttp
f = open(root+'/Lasttp.cmd','w')
f.close()

if len(sys.argv)==1:
    print("Tp is a simple Directory Jumper (Python Edition)")
    print("	Syntax: +(name) (dir)	==> Create a destination")			
    print("	Syntax: -(name)		==> Delete a destination")
    print("	Syntax: *(name) 	==> Check a destination")
    print("	Syntax: (name)  	==> Jump to destination")
    print("	Syntax: [list/*]    	==> Show all destinations")
    print("	Syntax: back		==> Jump to where before jump")
    print("Tp Created by XingZhe-Li Version 0.0.1")
else:
    # Load destinations.json
    if not os.path.isfile(root+"/destinations.json"):
        print("[Tp] destinations.json not found")
        renewjson()
        print("[Tp] auto Created destinations.json")
        sys.exit(1)
    destf = open(root+'/destinations.json','r')
    dest = destf.read()
    destf.close()
    jdest = json.loads(dest)
    if ("back" not in jdest) or ("destinations" not in jdest):
        print("[Tp] destinations.json is not workable!")
        x = input("[Tp] Renew it?(y/n)")
        if x.lower()=='y':
            renewjson()
            print("[Tp] Renewed destinations.json")
            sys.exit(1)
        else:
            print("[Tp] Exiting")
            sys.exit(1)
    
    # Ifs
    
    if sys.argv[1] in ["list","*"]:
        print("[Tp] All Destinations Recorded Are Shown Below")
        for i in jdest["destinations"]:
            print("[Tp]     {0} ==> {1}".format(i,jdest["destinations"][i]))
    elif sys.argv[1]=="back":
        if jdest["back"]==True:
            jumpback()
        else:
            print("[Tp] Back is not enabled")
    elif sys.argv[1]=='+back':
        if jdest["back"]==True:
            print("[Tp] Back is already enabled")
        else:
            print("[Tp] Enabling back")
            jdest["back"] = True
            writejson(jdest) 
    elif sys.argv[1]=='*back':
        print("[Tp] BackStatus: "+jdest["back"])
    elif sys.argv[1]=='-back':
        if jdest["back"]==False:
            print("[Tp] Back is already disabled")
        else:
            print("[Tp] Disabling back")
            jdest["back"] = False
            writejson(jdest) 
    elif sys.argv[1] in ['','+','-']:
        print('[Tp] Not Recommended by using \"\"')
    elif sys.argv[1][0]=='+':
        if len(sys.argv)==2:
            print('[Tp] Destination ==> getcwd:{0}'.format(os.getcwd()))
            sys.argv.append(os.getcwd())
        if len(sys.argv)==3:
            if not os.path.isdir(sys.argv[2]):
                print('[Tp] Warn \"{0}\" is not a directory!')
                sys.exit(1)
            
            sys.argv[2] = os.path.abspath(sys.argv[2])
            destiname = sys.argv[1].lstrip('+')
            if destiname in jdest["destinations"]:
                print("[Tp] Warn: Found {0} as {1}".format(destiname,jdest["destinations"][destiname]))
                print("[Tp] Warn: Replace it To {0}?".format(sys.argv[2]))
                x = input("[Tp] Replace it?(y/n)")
                if x.lower()=='y':
                    jdest["destinations"][destiname] = sys.argv[2]
                    writejson(jdest)
                    print('[Tp] Destination Replaced')
            else:
                jdest["destinations"][destiname] = sys.argv[2]
                writejson(jdest)
                print("[Tp] Destination Updated")
        else:
            print("[Tp] Syntax: +(name) (dir)	==> Create a destination")
    elif sys.argv[1][0]=='-':
        destiname = sys.argv[1].lstrip('-')
        if len(sys.argv)==2:
            if destiname in jdest["destinations"]:
                jdest["destinations"].pop(destiname)
                writejson(jdest)
                print("[Tp] Deleted Key:{0}".format(destiname))
            else:
                print("[Tp] Warn: {0} is not found in destinations".format(destiname))
        else:
            print("	Syntax: -(name)		==> Delete a destination")
    elif sys.argv[1][0]=='*':
        destiname = sys.argv[1].lstrip("*")
        if len(sys.argv)==2:
            if destiname in jdest["destinations"]:
                print("[Tp] {0} ==> {1}".format(destiname,jdest["destinations"][destiname]))
            else:
                print("[Tp] Warn: {0} is not found in destinations".format(destiname))
        else:
            print("	Syntax: *(name) 	==> Check a destination")
    elif len(sys.argv)==2:
        destiname = sys.argv[1]
        if destiname in jdest["destinations"]:
            print("[Tp] Jumping to {0}".format(jdest["destinations"][destiname]))
            writetp("@cd /d \"{0}\"".format(jdest["destinations"][destiname]))
            if jdest["back"]==True:
                writeback()
        else:
            print("[Tp] Warn: {0} is not found in destinations".format(destiname))
    else:
        print("[Tp] Unrecognized Syntax !")