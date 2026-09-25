from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def create_product(name, price, stock=0):
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("El nombre no puede estar vacio")
    
    try:
        price_dec = Decimal(str(price))
        stock_int = int(stock)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("El precio y el stock tienen que ser numeros validos") from None

    if price_dec < 0:
        raise ValueError("El precio no puede ser negativo")
    if stock_int < 0:
        raise ValueError("El stock no puede ser negativo")

    new_product = {
        "name": clean_name,
        "price": price_dec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), 
        "stock": stock_int,
    }

    return new_product


def validate_stock(product, units):
    try:
        units_int = int(units)
    except (ValueError, TypeError):
        raise ValueError("La cantidad debe ser un numero valido") from None
    
    if isinstance(units, float) and units != units_int:
        raise ValueError("Las unidades no pueden ser decimales")

    if units_int <= 0:
        raise ValueError("Las unidades deben ser mayores que 0")

    if product["stock"] < units_int:
        raise ValueError("Producto no disponible, cantidades insuficientes")

    return product



if __name__ == "__main__":
    valery = create_product("valery", 2300, 10)
    teresa = create_product("teresa", 150, 60)

    print(validate_stock(valery, 2.5))