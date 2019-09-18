import os
import random

import numpy as np
import hangar
from tqdm import tqdm

from hangarapi.config import SCREEN_DIR


def make_arrayset(i, repo, branch_name="master"):
    co = repo.checkout(write=True, branch=branch_name)
    aset_var = random.randint(0, 100000) + random.randint(0, 100000)
    aset_name = f"{i}_aset_{aset_var}"
    shape = (299, 299, 3)
    co.arraysets.init_arrayset(aset_name, shape=shape, dtype=np.float64)
    co.commit('init')
    co.close()
    return aset_name


def fill_data(repo, aset_name, count, branch_name='master'):
    commit_every = random.randint(30, 50)
    co = repo.checkout(write=True, branch=branch_name)
    aset = co.arraysets[aset_name]
    shape = aset.shape
    for i in tqdm(range(count)):
        aset[i] = np.random.random(shape)
        if i % commit_every == 0:
            co.commit(f"commit #{i}")
    if co.diff.status() == "DIRTY":
        co.commit('filled data')
    co.close()


nrepos = os.environ.get('NDUMMY')
if nrepos:
    for i in range(int(nrepos)):
        print(f"Making repo #{i}")
        path = SCREEN_DIR.joinpath(f'mydummyrepo_{i}')
        path.mkdir()
        repo = hangar.Repository(path)
        repo.init(user_name=f'name_{i}', user_email=f'email_{i}@abc.com', remove_old=True)
        aset_name = make_arrayset(i, repo)
        datacount = random.randint(100, 300)
        fill_data(repo, aset_name, datacount)