from flask.views import MethodView
from flask import jsonify, request

from .config import SCREEN_DIR
from .utils import get_valid_repo, create_repo, get_arraysets, get_samples


# TODO: Logging

class RepositoryAPI(MethodView):

    def get(self):
        data = []
        for d in SCREEN_DIR.iterdir():
            if not d.is_dir():
                continue
            repo = get_valid_repo(d)
            if repo:
                # TODO: Create a hangar interface for all hangar interactions
                cmt_details = repo.log(return_contents=True)
                # TODO: make sure pop returns the latest
                try:
                    top = cmt_details['order'].pop()
                except IndexError:
                    cmt_time = None
                else:
                    cmt_time = cmt_details['specs'][top]['commit_time']
                repo_details = {
                    'repo_name': d.stem,
                    'desc': d.stem,
                    'last_commit_date': cmt_time,
                    'commit_count': len(cmt_details['order']),
                    'branch_count': len(repo.list_branches()),
                    'hangar_version': repo.version
                }
                data.append(repo_details)
        if data:
            ret = {'data': data, 'success': True, 'message': ''}
        else:
            ret = {'data': [], 'success': False, 'message': "Found no valid hangar repositories"}
        return jsonify(ret), 200

    def post(self):
        """ Creating repository or Cloning """
        if not request.json:
            message = "provide required parameters"
            ret = {'success': False, 'message': message, 'data': []}
            return jsonify(ret), 400
        try:
            repo_name = request.json['repo_name']
            desc = request.json['desc']
            username = request.json['username']
            email = request.json['email']
        except KeyError:
            message = "provide required parameters"
            ret = {'success': False, 'message': message, 'data': []}
            return jsonify(ret), 400
        path = SCREEN_DIR.joinpath(repo_name)
        if not path.exists():
            try:
                path.mkdir()
            except Exception as e:
                print(e)
                message = "Unknown error while creating repo directory"
                ret = {'success': False, 'message': message, 'data': []}
                return jsonify(ret), 500
        status, message = create_repo(path, username, email, desc)
        ret = {'success': status, 'message': message, 'data': []}
        return jsonify(ret), 201

    def put(self):
        """repo pull and partial clone """
        pass

    def delete(self):
        # TODO: allow deletion of repo from UI
        raise NotImplementedError


class ArraysetAPI(MethodView):

    def get(self):
        repo_name = request.args['repo_name']
        branch_name = request.args.get('branch_name', 'master')
        path = SCREEN_DIR.joinpath(repo_name)
        if not path.exists():
            message = "Repository does not exist"
            ret = {'success': False, 'message': message, 'data': []}
            return jsonify(ret), 400
        asets = get_arraysets(path, branch_name)
        data = []
        for aset in asets:
            aset_details = {
                "arrayset_name": aset.name,
                "variable": aset.variable_shape,
                # TODO: find a better conversion
                "dtype": str(aset.dtype),
                "shape": list(aset.shape),
                "sample_count": len(aset)
            }
            data.append(aset_details)
        ret = {'success': True, 'message': '', 'data': data}
        return jsonify(ret), 200


class SampleAPI(MethodView):

    def get(self):
        repo_name = request.args['repo_name']
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        branch_name = request.args.get('branch_name', 'master')
        arrayset_name = request.args['arrayset_name']
        path = SCREEN_DIR.joinpath(repo_name)
        if not path.exists():
            message = "Repository does not exist"
            ret = {'success': False, 'message': message, 'data': []}
            return jsonify(ret), 400
        data, message = get_samples(path, branch_name, arrayset_name, limit, offset)
        if data:
            ret = {'success': True, 'message': message, 'data': data}
        else:
            ret = {'success': False, 'message': message, 'data': []}
        return jsonify(ret), 200


class HistoryAPI(MethodView):
    """ History of commits """

    def get(self):
        pass


class DiffAPI(MethodView):

    def get(self):
        pass

