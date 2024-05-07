from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List, Optional
import requests
from datetime import datetime

app = FastAPI()


# Модель для создания заказа
class OrderCreate(BaseModel):
    cust_id: int
    exec_id: int
    type_of_order: str
    expire_date: str
    price: float
    process: str
    version: int = 1


# Модель для обновления заказа
class OrderUpdate(BaseModel):
    exec_id: Optional[int] = None
    expire_date: Optional[str] = None
    process: Optional[str] = None
    version: Optional[int] = None


class Payment(BaseModel):
    order_id: int
    operation_date: str = None
    price: float = 0.00


# Эндпоинт для создания заказа
@app.post("/orders/")
async def create_order(order: OrderCreate):
    # Преобразуем данные в формат, который ожидает Django
    data = {
        "cust_id": order.cust_id,
        "exec_id": order.exec_id,
        "type_of_order": order.type_of_order,
        "expire_date": order.expire_date,
        "price": order.price,
        "process": order.process,
        "version": order.version
    }
    response = requests.post("http://localhost:8000/api/orders/", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


# Эндпоинт для получения всех заказов
@app.get("/orders/", response_model=List[OrderCreate])
async def read_orders():
    response = requests.get("http://localhost:8000/api/orders/")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


# Эндпоинт для получения информации о конкретном заказе
@app.get("/orders/{order_id}", response_model=OrderCreate)
async def read_order(order_id: int):
    response = requests.get(f"http://localhost:8000/api/orders/{order_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


# Эндпоинт для удаления заказа
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    response = requests.delete(f"http://localhost:8000/api/orders/{order_id}/")
    if response.status_code == 200:
        return {"detail": "Order deleted successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.put("/orders/{order_id}")
async def update_order(order_id: int, order_update: OrderUpdate):
    data = order_update.dict(exclude_unset=True)  # Исключаем неустановленные значения
    if data:
        data["version"] += 1  # Увеличиваем версию при обновлении

        # Если новая дата истечения заказа задана, конвертируем ее в строку
        if data.get("expire_date"):
            data["expire_date"] = datetime.strptime(data["expire_date"], "%Y-%m-%d").isoformat()

        response = requests.put(f"http://localhost:8000/api/orders/{order_id}/", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        raise HTTPException(status_code=400, detail="No fields provided for update")


# Эндпоинт для проверки и создания платежа
@app.post("/payments/")
async def create_payment(payment: Payment):
    order_id = payment.order_id
    # Получаем информацию о заказе
    response = requests.get(f"http://localhost:8000/api/orders/{order_id}/")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    order_info = response.json()

    # Проверяем, закрыт ли заказ и достаточно ли средств у заказчика
    if order_info["process"] == "Closed":
        customer_id = order_info["cust_id"]
        response_customer = requests.get(f"http://localhost:8000/api/customers/{customer_id}/")
        if response_customer.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user details")
        customer_info = response_customer.json()

        if customer_info["balance"] < order_info["price"]:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # Выполняем операцию оплаты
        customer_balance_new = customer_info["balance"] - order_info["price"]
        executor_id = order_info["exec_id"]
        response_executor = requests.get(f"http://localhost:8000/api/executors/{executor_id}/")
        if response_executor.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch executor details")
        executor_info = response_executor.json()
        executor_balance_new = executor_info["balance"] + order_info["price"]

        # Обновляем балансы
        response_customer = requests.put(f"http://localhost:8000/api/users/{customer_id}/",
                                         json={"balance": customer_balance_new})
        if response_customer.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to update customer balance")
        response_executor = requests.put(f"http://localhost:8000/api/users/{executor_id}/",
                                         json={"balance": executor_balance_new})
        if response_executor.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to update executor balance")

        # Создаем платежное событие
        payment_data = {
            "order_id": order_id,
            "operation_date": datetime.now().isoformat(),
            "price": order_info["price"]
        }
        response = requests.post("http://localhost:8000/api/payments/", json=payment_data)
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        raise HTTPException(status_code=400, detail="Order is not closed")


# Генерация OpenAPI схемы
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API title",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
