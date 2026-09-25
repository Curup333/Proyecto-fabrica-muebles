import pytest
from productos import create_product, validate_stock


@pytest.mark.parametrize("units", [0, -2])
def test_validate_stock_unidades_menores_o_iguales_a_cero(units):
    product = create_product("harp", 250, 20)
    with pytest.raises(ValueError, match="Las unidades deben ser mayores que 0"):
        validate_stock(product, units)


@pytest.mark.parametrize("units", [7, 8, 100])
def test_validate_stock_sin_stock_suficiente(units):
    product = create_product("teresa", 130, 6)
    with pytest.raises(ValueError, match="cantidades insuficientes"):
        validate_stock(product, units)


@pytest.mark.parametrize("units", [5, 10, "3", 2.0])
def test_validate_stock_con_stock_suficiente(units):
    product = create_product("kyoto", 3600, 10)
    result = validate_stock(product, units)
    assert result == product


@pytest.mark.parametrize("units", ["abc", None, "2.5"])
def test_validate_stock_numero_valido(units):
    product = create_product("teradrop", 2000, 6)
    with pytest.raises(ValueError, match="debe ser un numero valido"):
        validate_stock(product, units)


def test_validate_stock_en_decimal():
    product = create_product("coteca", 120, 50)
    with pytest.raises(ValueError, match="no pueden ser decimales"):
        validate_stock(product, 2.9)