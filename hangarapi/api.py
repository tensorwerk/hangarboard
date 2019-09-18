from flask.views import MethodView
from flask import jsonify, request

from .config import SCREEN_DIR
from .utils import get_valid_repo, create_repo


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
                top = cmt_details['order'][0]
                cmt_time = cmt_details['specs'][top]['commit_time']
                repo_details = {
                    'name': d.stem,
                    'desc': d.stem,
                    'last_commit_date': cmt_time,
                    'commit_count': len(cmt_details['order']),
                    'branch_count': len(repo.list_branches())
                }
                data.append(repo_details)
        if data:
            ret = {'data': data, 'success': True, 'message': ''}
        else:
            ret = {'data': [], 'success': False, 'message': "Found no valid hangar repositories"}
        return jsonify(ret), 200

    def post(self):
        if not request.json:
            message = "provide required parameters"
            ret = {'success': False, 'message': message, 'data': []}
            return jsonify(ret), 400
        try:
            repo_name = request.json['name']
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

    def delete(self):
        # TODO: allow deletion of repo from UI
        raise NotImplementedError


class ArraysetAPI(MethodView):

    def get(self):
        repo_name = request.args['repo_name']
        ret = {'success': True, 'message': '', 'data': [
            {
                'name': f'{repo_name}_MNIST_image',
                'variable': False,
                'dtype': 'uint8',
                'shape': [28, 28],
                'sample_count': 60000
            },
            {
                'name': f'{repo_name}_MNIST_target',
                'variable': True,
                'dtype': 'int64',
                'shape': [100],
                'sample_count': 60000
            }
        ]}
        return jsonify(ret), 200


class SampleAPI(MethodView):

    def get(self):
        ret = {'success': True, 'message': '', 'data': []}
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        for i in range(offset, offset + limit):
            each = {
                'name': i,
                'shape': [5, 4]
            }
            ret['data'].append(each)
        return jsonify(ret), 200


class VersionAPI(MethodView):

    def get(self):
        ret = {'success': True, 'message': '', 'data': []}
        return jsonify(ret), 200