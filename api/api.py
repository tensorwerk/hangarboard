from collections import defaultdict

from flask.views import MethodView
from flask import jsonify, request

from .config import BOARD_DIR
from .hinterface import Hinterface


# TODO: Logging

class RepositoryAPI(MethodView):

    def get(self):
        data = []
        for d in BOARD_DIR.iterdir():
            if not d.is_dir():
                # TODO: Remove this check later
                continue
            try:
                interface = Hinterface(d)
            except RuntimeError as e:
                # TODO: ignoring for now but do something here
                continue
            repo_details = interface.repo_details
            repo_details['repo_name'] = d.stem
            repo_details['desc'] = d.stem
            data.append(repo_details)
        # TODO: make a reply crafter
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
        path = BOARD_DIR.joinpath(repo_name)
        # TODO: Catch exceptions
        Hinterface.create_repo(path, username, email, desc)
        status = True
        message = "Repository created successfully"
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
        path = BOARD_DIR.joinpath(repo_name)
        interface = Hinterface(path, branch_name)

        data = []
        for aset in interface.arraysets:
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
        arrayset_name = request.args.get('arrayset_name')
        path = BOARD_DIR.joinpath(repo_name)
        interface = Hinterface(path, branch_name, arrayset_name)
        data = {}
        for arrayset_name, sample_names in interface.sample_names:
            data[arrayset_name] = sample_names
        message = "Fetched sample names successfully"
        if data:
            ret = {'success': True, 'message': message, 'data': data}
        else:
            ret = {'success': False, 'message': message, 'data': []}
        return jsonify(ret), 200


class HistoryAPI(MethodView):
    """ History of commits """

    def get(self):
        repo_name = request.args['repo_name']
        path = BOARD_DIR.joinpath(repo_name)
        interface = Hinterface(path)
        data = interface.repo.log(return_contents=True)
        ret = {'success': True, 'message': '', 'data': data}
        return jsonify(ret), 200


class SearchAPI(MethodView):
    """ Search for Samples """

    def get(self):
        repo_name = request.args['repo_name']
        arrayset_name = request.args.get('arrayset_name')
        branch_name = request.args.get('branch_name', 'master')
        substr = request.args.get('substr')
        path = BOARD_DIR.joinpath(repo_name)
        interface = Hinterface(path, branch_name, arrayset_name)
        # TODO: make this searchable array outside and should not execute it always
        # TODO: handle if substr is None
        # TODO: check the efficiency of the search
        srch_dict = defaultdict(list)
        for aset in interface.arraysets:
            for key in aset.keys():
                srch_dict[key].append(aset.name)

        search_results = defaultdict(list)
        for i in srch_dict.keys():
            if i.startswith(substr):
                for aset in srch_dict[i]:
                    search_results[aset.name].append(i)

        data = []
        for key, value in search_results.items():
            data.append({
                'arrayset_name': key,
                'sample_names': value
            })

        ret = {'success': True, 'message': '', 'data': data}
        return jsonify(ret), 200


class DiffAPI(MethodView):

    def get(self):
        repo_name = request.args['repo_name']
        master_branch = request.args['master_branch_name']
        dev_branch = request.args['dev_branch_name']
        path = BOARD_DIR.joinpath(repo_name)
        if not path.exists():
            message = "Repository does not exist"
            ret = {'success': False, 'message': message, 'data': []}
            return jsonify(ret), 400
        repo = utils.get_valid_repo(path)
        co = repo.checkout(branch=master_branch)
        diff = co.diff.branch(dev_branch)
        # master.diff.branch('dummy2').diff.added.samples.keys()
        ret = {'success': True, 'message': '', 'data': diff}
        return jsonify(ret), 200
