import contextlib

import sys

from flask import request
from io import StringIO

from cache_registry.api.views import ApiView
from cache_registry.sync.commands import (
    bdr,
    fgases,
    fgases_debug_noneu,
    licences,
    ods,
    sync_collections_title
)

from cache_registry.match import run, flush, verify, unverify, test, manual


@contextlib.contextmanager
def stdout_redirect(where):
    sys.stdout = where
    try:
        yield where
    finally:
        sys.stdout = sys.__stdout__


class MgmtCommand(ApiView):
    command_func = None

    def get(self, **kwargs):
        kwargs = kwargs or request.args.to_dict()
        with stdout_redirect(StringIO()) as output:
            try:
                success = self.command_func(**kwargs)
                message = ''
            except Exception as ex:
                success = False
                message = repr(ex)

        output.seek(0)
        message = output.read() + message

        return {'success': success, 'message': message}


class SyncFgasesView(MgmtCommand):
    command_func = staticmethod(fgases)


class SyncFgasesDebugNoneuView(MgmtCommand):
    command_func = staticmethod(fgases_debug_noneu)


class SyncODSView(MgmtCommand):
    command_func = staticmethod(ods)


class SyncLicencesView(MgmtCommand):
    command_func = staticmethod(licences)

class SyncCollectionsTitleView(MgmtCommand):
    command_func = staticmethod(sync_collections_title)


class SyncBdr(MgmtCommand):
    command_func = staticmethod(bdr)


class MatchRun(MgmtCommand):
    command_func = staticmethod(run)


class MatchFlush(MgmtCommand):
    command_func = staticmethod(flush)
