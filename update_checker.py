import os, sys, pickle
import requests
import webbrowser
from file_handler import envs

try:
    import git
    import_failed = False
except ImportError:
    import_failed = True

class UpdateChecker:
    def __init__(self):
        self.can_update = False
        self.urls = None
        self.header = "\nJEMViewer 2\n"
        try:
            self.load_url()
        except:
            self.header += "Network error\n"
            self.header += "Please check your network connection.\n\n"
            return
        if import_failed:
            self.header += "You need to install git to manage software version.\n"
            self.header += "Please visit the manual site for more detail.\n\n"
            return
        self.repo = git.Repo(os.path.join(os.path.dirname(sys.argv[0])))
        self.current_tag = next((tag for tag in self.repo.tags if tag.commit == self.repo.head.commit), None)
        if self.current_tag == None:
            self.header += f"Unknown version: {self.repo.head.commit.hexsha}\n\n"
            return
        self.header += f"current version: {self.current_tag.name}"
        origin = self.repo.remote()
        try:
            origin.fetch(prune=True, prune_tags=True)
        except git.exc.GitCommandError:
            self.header += "\n"
            self.header += "GitCommandError has occurred.\n"
            self.header += "Please check your network connection.\n\n"
            return
        tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_datetime)
        self.latest_tag =tags[-1]
        if self.current_tag == self.latest_tag:
            self.header += " (latest)\n\n"
        else:
            self.header += "\n"
            self.header += f"Version {self.latest_tag.name} is now available.\n"
            current_major = self.current_tag.name.split('.')[1]
            latest_major = self.latest_tag.name.split('.')[1]
            if current_major == latest_major:
                self.header += "Type JEMViewer.update() to update the software.\n\n"
                self.can_update = True
            else:
                self.header += "Please visit the manual site to upgrade the software.\n\n"
    
    def update(self):
        if self.urls != None:
            webbrowser.open_new(self.urls["updatelog"])
        if self.can_update:
            self.repo.git.checkout(self.latest_tag,force=True)
            print("Update completed.")
            print("Please restart JEMViewer.")
        else:
            print("This is the latest version.")
        
    def load_url(self):
        token_file = os.path.join(envs.ADDON_DIR, "notion_token")
        if not os.path.exists(token_file): return
        with open(token_file,"rb") as f:
            access_token, db_id = pickle.load(f)
        geturl = "https://api.notion.com/v1/databases/" + db_id + "/query" 
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }
        r = requests.post(geturl, headers=headers)
        getdata = r.json()
        res = getdata["results"]
        self.urls = {}
        for data in res:
            obj = data["properties"]
            try:
                if obj["Status"]["select"]["name"] != "archive":
                    continue
            except:
                pass
            try:
                name = obj["名前"]["title"][0]["plain_text"]
            except:
                continue
            try:
                url = obj["一言説明"]["rich_text"][0]["plain_text"]
            except:
                url = ""
            self.urls[name] = url
        return True

    def manual(self):
        if self.urls != None:
            webbrowser.open_new(self.urls["toppage"])
        else:
            print("You need to activate addon_store first.\nPlease check the manual site.")