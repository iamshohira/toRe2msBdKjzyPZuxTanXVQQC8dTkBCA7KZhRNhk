import requests
from prettytable import PrettyTable
import os, webbrowser
import pickle
import subprocess

class AddonInstaller:
    def __init__(self, addon_dir):
        self.addon_dir = addon_dir
        self.addons = None
        self.token_file = os.path.join(self.addon_dir,"notion_token")

    def activate(self, tokens):
        token, db_id = tokens.split(";")
        access_token = "secret_" + token
        db_id = db_id
        with open(self.token_file,"wb") as f:
            pickle.dump([access_token,db_id],f)

    def load_addon(self):
        if os.path.exists(self.token_file):
            with open(self.token_file,"rb") as f:
                access_token, db_id = pickle.load(f)
        else:
            print("You need to activate addon_store first.\nPlease check the manual site.")
            return False
        geturl = "https://api.notion.com/v1/databases/" + db_id + "/query" 
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }
        r = requests.post(geturl, headers=headers)
        getdata = r.json()
        res = getdata["results"]
        addons = {}
        for data in res:
            obj = data["properties"]
            try:
                if obj["Status"]["select"]["name"] == "archive":
                    continue
            except:
                pass
            try:
                name = obj["名前"]["title"][0]["plain_text"]
            except:
                continue
            try:
                filename = obj["script file"]["files"][0]["name"]
                fileurl = obj["script file"]["files"][0]["file"]["url"]
            except:
                continue
            try:
                description = obj["一言説明"]["rich_text"][0]["plain_text"]
            except:
                description = ""
            addons[name] = {
                "description": description,
                "filename": filename,
                "fileurl": fileurl,
            }
        self.addons = addons
        return True

    def list(self):
        if self.addons == None:
            if not self.load_addon():
                return
        table = PrettyTable()
        table.align = "l"
        table.field_names = ["Addon", "Description"]
        for k,v in self.addons.items():
            table.add_row([k, v["description"]])
        print(table)

    def install(self, addon_name):
        if self.addons == None:
            if not self.load_addon():
                return
        addon = self.addons[addon_name]
        urldata = requests.get(addon["fileurl"]).content
        with open(os.path.join(self.addon_dir, addon["filename"]), "wb") as f:
            f.write(urldata)

    def install_all(self):
        if self.addons == None:
            if not self.load_addon():
                return
        for k in self.addons.keys():
            self.install(k)

    def open_dir(self):
        if os.name == "nt":
            run = "start"
        else:
            run = "open"
        subprocess.run([run, self.addon_dir])

    def open_vscode(self):
        try:
            subprocess.run(["code", self.addon_dir])
        except:
            pass

