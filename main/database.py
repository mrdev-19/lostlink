import os
from deta import Deta
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

#load env var

load_dotenv(".env")

DETA_KEY=os.getenv("DETA_KEY")
deta=Deta(DETA_KEY)

ldb=deta.Base("Lost")
rdb=deta.Base("Found")
cred=deta.Base("Creds")
admin=deta.Base("Admin")

def emailexists(email):
    dev=fetch_all_users()
    emails=[user["email"] for user in dev]
    for user in dev:
        if(user["email"]==email):
            return True
    else:
        return False

def insert_user(username,password,email,number):
    cred.put({"key":username,"password":password,"email":email,"number":number,"curkey":""})

def insert_admin(username,password,email,number):
    admin.put({"key":username,"password":password,"email":email,"number":number})

def authenticate(username,password):
    var=1
    dev=fetch_all_users()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(username==user["key"] and user["password"]==password):
            return True
            var=0
    if(var):
        return False

def ad_authenticate(username,password):
    var=1
    dev=fetch_all_admins()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(username==user["key"] and user["password"]==password):
            return True
            var=0
    if(var):
        return False

def fetch_all_instances():
    dev=entries.fetch()
    res=dev.items
    return res

def fetch_all_users():
    res=cred.fetch()
    return res.items

def fetch_all_admins():
    res=admin.fetch()
    return res.items

def fetch_all_entries(username):
    data=[]
    dev=entries.fetch()
    res=dev.items
    for user in res:
        if user["username"]==username:
            data.append({"Entry":user["data"],"Date":user["date"]})
    return data

def insert_entry(username,date,name,place,mailid,other,lof):
    if(lof=="lost"):
        return ldb.put({"date": date,"name": name,"place": place,"email":mailid,"username":username,"other": other,"info":"","fileid":filename})
    else:
        return rdb.put({"date": date,"name": name,"place": place,"email":mailid,"username":username,"other": other,"info":""})

def all_lost():
    dev=ldb.fetch()
    dev=dev.items
    return dev

def all_found():
    dev=rdb.fetch()
    dev=dev.items
    return dev

def f_change_status(data,key):
    found=all_lost()
    for user in found:
        print(user)
        if(user["name"]==key):
            print("data found dude")
            user["status"]=data

def l_change_status(username,upd):
    updates={"status":upd}
    ldb.update(updates,username)

def f_change_status(username,upd):
    updates={"status":upd}
    rdb.update(updates,username)

def forgot_pass(email,otp):
    dev=fetch_all_users()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(user["email"]==email):
            mkey=user["key"]
            change={"curkey":otp}
            cred.update(change,mkey)