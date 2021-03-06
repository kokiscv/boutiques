#!/usr/bin/env python

import os
from unittest import TestCase
from boutiques import __file__ as bfile
import boutiques as bosh
import mock
from boutiques_mocks import mock_zenodo_search, MockZenodoRecord


def mock_get():
    mock_record = MockZenodoRecord(1472823, "Example Boutiques Tool", "",
                                   "https://zenodo.org/api/files/"
                                   "e5628764-fc57-462e-9982-65f8d6fdb487/"
                                   "example1_docker.json")
    return mock_zenodo_search([mock_record])


class TestEvaluate(TestCase):

    def set_examples(self):
        example1_dir = os.path.join(os.path.dirname(bfile), "schema",
                                    "examples", "example1")
        self.desc = os.path.join(example1_dir, "example1_docker.json")
        self.invo = os.path.join(example1_dir, "invocation.json")

    def set_examples_json_obj(self):
        example1_dir = os.path.join(os.path.dirname(bfile), "schema",
                                    "examples", "example1")
        self.desc = open(os.path.join(example1_dir,
                         "example1_docker.json")).read()
        self.invo = open(os.path.join(example1_dir, "invocation.json")).read()

    def set_examples_from_zenodo(self):
        example1_dir = os.path.join(os.path.dirname(bfile), "schema",
                                    "examples", "example1")
        self.desc = "zenodo.1472823"
        self.invo = os.path.join(example1_dir, "invocation.json")

    def test_evaloutput(self):
        self.set_examples()
        query = bosh.evaluate(self.desc, self.invo, "output-files/")
        expect = {'logfile': 'log-4-coin;plop.txt',
                  'output_files': 'output/*_exampleOutputTag.resultType',
                  'config_file': './config.txt'}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "output-files/id=logfile")
        expect = {'logfile': 'log-4-coin;plop.txt'}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "output-files/id=log-file")
        expect = {}
        assert(query == expect)

    def test_evaloutput_json_obj(self):
        self.set_examples_json_obj()
        query = bosh.evaluate(self.desc, self.invo, "output-files/")
        expect = {'logfile': 'log-4-coin;plop.txt',
                  'output_files': 'output/*_exampleOutputTag.resultType',
                  'config_file': './config.txt'}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "output-files/id=logfile")
        expect = {'logfile': 'log-4-coin;plop.txt'}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "output-files/id=log-file")
        expect = {}
        assert(query == expect)

    @mock.patch('requests.get', return_value=mock_get())
    def test_evaloutput_from_zenodo(self, mock_get):
        self.set_examples_from_zenodo()
        query = bosh.evaluate(self.desc, self.invo, "output-files/")
        expect = {'logfile': 'log-4-coin;plop.txt',
                  'output_files': 'output/*_exampleOutputTag.resultType',
                  'config_file': './config.txt'}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "output-files/id=logfile")
        expect = {'logfile': 'log-4-coin;plop.txt'}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "output-files/id=log-file")
        expect = {}
        assert(query == expect)

    def test_evalinput(self):
        self.set_examples()
        query = bosh.evaluate(self.desc, self.invo, "inputs/")
        expect = {'str_input_list': ["fo '; echo FAIL", 'bar'],
                  'str_input': 'coin;plop',
                  'config_num': 4,
                  'num_input': None,
                  'file_input': './setup.py',
                  'enum_input': 'val1',
                  'list_int_input': [1, 2, 3],
                  'flag_input': None}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo,
                              "inputs/type=Flag,id=flag_input",
                              "inputs/type=Number")
        expect = [{'flag_input': None},
                  {'config_num': 4,
                   'num_input': None,
                   'list_int_input': [1, 2, 3]}]
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "inputs/id=strinputs")
        expect = {}
        assert(query == expect)

        query = bosh.evaluate(self.desc, self.invo, "inputt/nonsense=strinputs")
        expect = {}
        assert(query == expect)

    def test_evalgroups(self):
        self.set_examples()
        query = bosh.evaluate(self.desc, self.invo, "groups/")
        expect = {'an_example_group': {'num_input': None,
                                       'enum_input': 'val1'}}
        assert(query == expect)

        query = bosh.evaluate(self.desc,
                              self.invo,
                              "groups/mutually-exclusive=True")
        expect = {'an_example_group': {'num_input': None,
                                       'enum_input': 'val1'}}
        assert(query == expect)
