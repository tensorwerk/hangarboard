import hangar


def get_valid_repo(path):
    try:
        repo = hangar.Repository(path)
        # TODO: fix hangar's version compatibility check
        if repo.initialized and repo.version >= '0.3.0':
            return repo
    except RuntimeError:
        pass
    return None


def create_repo(path, username, email, desc):
    repo = hangar.Repository(path)
    if repo.initialized:
        return False, "Repository with same name exist"
    # TODO: Allow remove old from webUI
    try:
        repo.init(username, email)
    except Exception as e:
        return False, str(e)
    return True, "Repository created successfully"
