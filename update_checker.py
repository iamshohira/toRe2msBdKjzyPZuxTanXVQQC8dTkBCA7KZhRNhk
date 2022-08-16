import os, sys
try:
    import git
    import_failed = False
except ImportError:
    import_failed = True

class UpdateChecker:
    def __init__(self):
        self.can_update = False
        self.header = "\nJEMViewer2\n\n"
        if import_failed:
            self.header += "You need to install git to manage software version.\n"
            self.header += "Please visit the manual site for more detail.\n\n"
            return
        self.repo = git.Repo(os.path.join(os.path.dirname(sys.argv[0])))
        self.current_tag = next((tag for tag in self.repo.tags if tag.commit == self.repo.head.commit), None)
        self.header += f"current version: {self.current_tag.name}"
        origin = self.repo.remote()
        try:
            origin.fetch()
        except git.exc.GitCommandError:
            self.header += "\n"
            self.header += "GitCommandError occurred.\n"
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
        self.repo.git.checkout(self.latest_tag)
        print("Update completed.")
        print("Please restart JEMViewer.")