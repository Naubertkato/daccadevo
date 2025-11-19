import pytest
import json

import daccadevo.submitDACCAD as sd
from daccadevo.submitDACCAD import default_cli_wrapper, CLI_wrapper

@pytest.fixture
def base_json():
	json_val = None
	with open("tests/testGraph0_0_0.json","r") as file:
		json_val = json.loads(file.read())
	return json_val

@pytest.fixture
def inhib_json():
	json_val = None
	with open("tests/testGraph0_0_1.json","r") as file:
		json_val = json.loads(file.read())
	return json_val

@pytest.fixture
def base_array():
	dna_stability = [1.0,1.0,1.0]
	connections = [10,1,0.0,0.0,0.0,1,0.0,0.0,0.0]
	inhibitions = 27*[0.0]
	return dna_stability+connections+inhibitions

@pytest.fixture
def array_inhib(base_array):
	index = 3+9+9+9 # 2 -| (0 -> 0)
	base_array[index] = 1
	return base_array

@pytest.fixture
def broken_array_inhib(array_inhib):
	index = 3+9+9+9+3 # 2 -| (1 -> 0), non existant
	array_inhib[index] = 1
	return array_inhib

@pytest.mark.parametrize('arr,result',
                             [("base_array","base_json"), ("array_inhib","inhib_json")])
def test_generation(arr, result, request):
	json_val = json.loads(default_cli_wrapper.generateFullJson(request.getfixturevalue(arr),nNodes=3))
	assert json_val == request.getfixturevalue(result)

@pytest.mark.parametrize('arr,result',
                             [('base_array',0), ('array_inhib',1), ('broken_array_inhib',2)])
def test_inhibition(arr, result, request):
	a = request.getfixturevalue(arr)
	assert len(sd.findAllInhibitions(a,nNodes=3)) == result # raw number of inhibitors
	assert sd.findAllInhibitorsAndConcsLegacy(a,nNodes=3) == sd.findAllInhibitorsAndConcs(a,nNodes=3) # only valid inhibitors

@pytest.mark.parametrize('arr,result',
                             [('base_array',0), ('array_inhib',0), ('broken_array_inhib',1)])
def test_invalid_inhibitions(arr, result, request):
	a = request.getfixturevalue(arr)
	assert len(sd.invalidInhibitions(a, nNodes = 3)) == result

def test_call_cli(array_inhib, tmpdir):
	"""
	Checks that calls to DACCAD are properly handled
	"""
	import os
	p = tmpdir.mkdir("test")
	jsonf = p.join("test.json")
	testconf = p.join("test.conf")
	n_points = 10
	testconf.write_text(f"numberOfPoints = {n_points}", encoding="utf-8")
	wrapper = CLI_wrapper()
	dataResult = wrapper.submitPENSystem(array_inhib, nNodes = 3, 
		daccad_config_file = os.fspath(testconf), jsonFileName = os.fspath(jsonf))
	assert len(dataResult) == n_points




