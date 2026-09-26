import pytest
from productos import create_product, validate_stock
from decimal import Decimal

# Validar stock
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


#Validar producto
def test_create_product_valido():
    product = create_product(" valery ", 2.345, "10")
    assert product["name"] == "valery"
    assert product["price"] == Decimal("2.35")
    assert product["stock"] == 10


def test_create_product_stock_por_defecto():
    product = create_product("teresa", 130)
    assert product["stock"] == 0


def test_create_product_precio_y_stock_cero():
    product = create_product("valery", 0, 0)
    assert product["price"] == 0
    assert product["stock"] == 0


@pytest.mark.parametrize("vacio", ["", " "])
def test_create_product_vacio_o_espacio(vacio):
    with pytest.raises(ValueError, match="no puede estar vacio"):
        create_product(vacio, 2000, 10)


def test_create_product_no_es_texto():
    with pytest.raises(ValueError, match="tiene que ser texto"):
        create_product(None, 130, 6)


@pytest.mark.parametrize("invalido", ["abc", None])
def test_create_product_precio_invalido_con_stock_valido(invalido):
    with pytest.raises(ValueError, match="tienen que ser numeros validos"):
        create_product("teresa", invalido, 10)


@pytest.mark.parametrize("invalido", ["abc", None, "2.5"])
def test_create_product_stock_invalido_con_precio_valido(invalido):
    with pytest.raises(ValueError, match="tienen que ser numeros validos"):
        create_product("teresa", 130, invalido)


@pytest.mark.parametrize("negativo", [-1, "-0.01"])
def test_create_product_precio_negativo_con_stock_valido(negativo):
    with pytest.raises(ValueError, match="precio"):
        create_product("teresa", negativo, 30)


@pytest.mark.parametrize("negativo", [-1, "-10"])
def test_create_product_stock_negativo_con_precio_valido(negativo):
    with pytest.raises(ValueError, match="stock"):
        create_product("teresa", 130, negativo)