from hangar import Repository


class Hinterface(object):
    """
    Interface class to interact with hangar repositories. It enables
    the APIs to ignore the internals of hangar and can utilize the high
    level functions
    """

    def __init__(self, path, branch='master', arrayset_name=None, sample_name=None):
        if not path.exists():
            raise FileNotFoundError("Repository does not exist")
        self.repo = Repository(path)
        # TODO: fix hangar's version compatibility check
        if not self.repo.initialized:
            raise RuntimeError("Repository not initialized")
        self.branch = branch
        self.arrayset_name = arrayset_name
        self.sample_name = sample_name
        self.rcheckout = self.repo.checkout(branch=self.branch)

    @classmethod
    def create_repo(cls, path, username, email, desc=None, create_path=True):
        # TODO: Remove if it is not necessary
        if not path.exists() and create_path:
            path.mkdir()
        repo = Repository(path)
        repo.init(username, email)

    @property
    def repo_details(self):
        cmt_details = self.repo.log(return_contents=True)
        # TODO: make sure pop returns the latest
        try:
            top = cmt_details['order'].pop()
        except IndexError:
            cmt_time = None
        else:
            cmt_time = cmt_details['specs'][top]['commit_time']
        return {
            "commit_time": cmt_time,
            "total_commit_count": len(cmt_details["order"]),
            "branch_count": len(self.repo.list_branches())
            "hangar_version": self.repo.version
        }

    @property
    def arraysets(self):
        if self.arrayset_name:
            yield self.rcheckout.arraysets[self.arrayset_name]
        else:
            return self.rcheckout.arraysets.values()

    @property
    def sample_names(self):
        if self.arrayset_name:
            aset = self.rcheckout[self.arrayset_name]
            yield aset.name, list(aset.keys())
        else:
            for aset in self.rcheckout.arraysets.values():
                yield aset.name, list(aset.keys())

    def get_samples(self, plugin_name=None):
        pass




