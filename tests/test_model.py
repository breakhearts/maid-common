import pytest
import os
import sys
import shutil
from sqlalchemy import Column, Integer, String, Float
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from model import DBHelper

temp_dir = "test_model_temp"
__dbhelper = DBHelper("sqlite:///%s" % os.path.join(temp_dir, "test.db"))

class MockModel(__dbhelper.get_base_class()):
    __tablename__ = "mock_table"
    id = Column(Integer, primary_key=True)
    str_column = Column(String)
    float_column = Column(Float)


@pytest.fixture(scope="module")
def dbhelper(request):
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    __dbhelper.create_tables()
    def fin():
        shutil.rmtree(temp_dir)
        return
    request.addfinalizer(fin)
    return __dbhelper


class TestDBHelper:
    def test_create(self, dbhelper):
        dbhelper.create_tables()

    def test_op(self, dbhelper):
        dbhelper.insert_one(MockModel(str_column="AAAA", float_column="3.2"))
        t = dbhelper.load_one(MockModel, "str_column", "AAAA")
        assert t.float_column == 3.2
        t.float_column = 4.3
        dbhelper.update_one(MockModel, t, "str_column", "AAAA")
        t = dbhelper.load_one(MockModel, "str_column", "AAAA")
        assert  t.float_column == 4.3
        dbhelper.delete_one(MockModel, "str_column", "AAAA")
        t = dbhelper.load_one(MockModel, "str_column", "AAAA")
        assert not t
        dbhelper.close_engine()
