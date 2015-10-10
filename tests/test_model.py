import pytest
import os
import sys
import shutil
from sqlalchemy
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from model import DBHelper

temp_dir = "test_model_temp"
__dbhelper = DBHelper("sqlite:///%s" % os.path.join(temp_dir, "test.db"))

class MockModel(__dbhelper.get_base_class()):
    __table__ = "mock_table"
    id =


@pytest.fixture(scope="module")
def dbhelper(request):
    __dbhelper.create_tables()
    def fin():
        shutil.rmtree(temp_dir)
        return
    request.addfinalizer(fin)
    return __dbhelper


class TestDBHelper:
    def test_create(self, dbhelper):
        dbhelper.create_tables()
