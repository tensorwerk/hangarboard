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


def get_arraysets_from_branch(path, branch_name):
    repo = hangar.Repository(path)
    if not repo.initialized:
        return False, "Repository not initialized"
    co = repo.checkout(branch=branch_name)
    return list(co.arraysets.values())


def get_arrayset(path, branch_name, arrayset_name):
    repo = hangar.Repository(path)
    if not repo.initialized:
        return False, "Repository not initialized"
    co = repo.checkout(branch=branch_name)
    return co.arraysets[arrayset_name]


def get_samples(path, branch_name, arrayset_name, limit, offset):
    repo = hangar.Repository(path)
    if not repo.initialized:
        return False, "Repository not initialized"
    co = repo.checkout(branch=branch_name)
    # TODO: if arrayset not found
    try:
        aset = co.arraysets[arrayset_name]
    except KeyError:
        return False, "Arrayset does not exist"
    data = []
    for key in aset.keys():
        if offset > 0:
            offset -= 1
            continue
        data.append({"name": key, "shape": list(aset[key].shape)})
        limit -= 1
        if limit < 1:
            break
    return data, "Samples fetched successfully"
