from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def create_product(name, price, stock=0):
    if not isinstance(name, str):
        raise ValueError("El nombre tiene que ser texto")
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


def create_order(customer, items):
    if not isinstance(customer, str):
        raise ValueError("El nombre tiene que ser un texto valido")
    clean_customer = customer.strip()
    if not clean_customer:
        raise ValueError("El nombre no puede estar vacio")

    units_by_product = {}

    for product, units in items:
        validate_stock(product, units)
        name = product["name"]
        if name in units_by_product:
            units_by_product[name][1] += int(units)
        else:
            units_by_product[name] = [product, int(units)]

    items_list = []
    total = Decimal("0")

    for product, units in units_by_product.values():
        validate_stock(product, units)
        subtotal = product["price"] * units
        total += subtotal
        items_list.append({
            "name": product["name"],
            "units": units,
            "price": product["price"],
            "subtotal": subtotal,
        })

    return {"customer": clean_customer, "items": items_list, "total": total}


def order_summary(order):
    print(f"Cliente: {order['customer']}")
    for item in order["items"]:
        print(f"{item['name']} x{item['units']} - ${item['price']} = ${item['subtotal']}")
    print(f"TOTAL: ${order['total']}")


if __name__ == "__main__":
    valery = create_product("valery", 3700, 10)
    teresa = create_product("teresa", 130, 60)
    order_summary(create_order("angel", [(valery, 3), (teresa, 6)]))