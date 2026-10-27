import pytest

def test_property_predictor():
    from property_prediction import PropertyPredictor, Molecule
    mol = Molecule("CCO")
    with pytest.raises(NotImplementedError):
        PropertyPredictor.calculate(mol)

def test_correct_input_property_predictor():
    from property_prediction import PropertyPredictor
    with pytest.raises(ValueError):
        PropertyPredictor.calculate("CCO")
