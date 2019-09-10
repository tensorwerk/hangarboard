from flask.views import MethodView
from flask import jsonify, request

from .utils import get_date


class RepositoryAPI(MethodView):

    def get(self):
        ret = {
                'data': [
                    {
                        'name': 'Project 83',
                        'desc': 'Some random Desc',
                        'last_commit_date': get_date(),
                        'commit_count': 215,
                        'branch_count': 2
                    },
                    {
                        'name': 'Visionary',
                        'desc': 'Some random Desc 2',
                        'last_commit_date': get_date(),
                        'commit_count': 21,
                        'branch_count': 3
                    }], 'success': True, 'message': ''}
        return jsonify(ret), 200

    def post(self):
        ret = {'success': True, 'message': 'Created', 'data': []}
        return jsonify(ret), 201


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
