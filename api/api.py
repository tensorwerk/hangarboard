from collections import defaultdict

from flask.views import MethodView
from flask import jsonify, request

from .config import BOARD_DIR
from .hinterface import Hinterface
from .utils import get_logger


logger = get_logger(__name__)


# TODO: Handle exceptions

class RepositoryAPI(MethodView):

    def get(self):
        logger.info("Repository GET call")
        data = []
        for d in BOARD_DIR.iterdir():
            try:
                interface = Hinterface(d)
            except Exception:
                logger.warning(f"Ignoring directory or file {d}")
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
        logger.debug(f"Return Data: {ret}")
        return jsonify(ret), 200


class ArraysetAPI(MethodView):

    def get(self):
        logger.info("Arrayset GET call")
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
        logger.info(f"Found {len(data)} arraysets")
        ret = {'success': True, 'message': '', 'data': data}
        logger.debug(f"Return Data: {ret}")
        return jsonify(ret), 200


class SampleAPI(MethodView):

    def get(self):
        logger.info("Samples GET call")
        repo_name = request.args['repo_name']
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        branch_name = request.args.get('branch_name', 'master')
        arrayset_name = request.args.get('arrayset_name')
        path = BOARD_DIR.joinpath(repo_name)
        interface = Hinterface(path, branch_name, arrayset_name)
        data = []
        for arrayset_name, sample_names in interface.sample_names:
            current = {}
            logger.info(f"Arrayset {arrayset_name} has {len(sample_names)} samples")
            current['arrayset_name'] = arrayset_name
            current['sample_names'] = sample_names[offset:offset + limit]
            data.append(current)
        message = "Fetched sample names successfully"
        if data:
            ret = {'success': True, 'message': message, 'data': data}
        else:
            ret = {'success': False, 'message': message, 'data': []}
        logger.debug(f"Return Data: {ret}")
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
        # repo = utils.get_valid_repo(path)
        # co = repo.checkout(branch=master_branch)
        # diff = co.diff.branch(dev_branch)
        # # master.diff.branch('dummy2').diff.added.samples.keys()
        # ret = {'success': True, 'message': '', 'data': diff}
        # return jsonify(ret), 200#
