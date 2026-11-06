import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Загрузка данных из JSON
with open("src/fastapiprac/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Модель данных
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool

# Задание 1: Получить все книги
@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]

# Задание 1: Получить книгу по ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    return None

# Задание 2: Добавить новую книгу
@app.post("/books", response_model=Book)
async def create_book(book: Book):
    data["books"].append(book.model_dump())
    with open("src/fastapiprac/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return book

# Задание 3: Удалить книгу по ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            removed = data["books"].pop(i)
            with open("src/fastapiprac/data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {"message": "Книга удалена", "book": removed}
    return {"message": "Книга не найдена"}

# Модель для обновления (все поля необязательные)
class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    genre: str | None = None
    price: float | None = None
    in_stock: bool | None = None

# Задание 4: Обновить книгу по ID
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: BookUpdate):
    for book in data["books"]:
        if book["id"] == book_id:
            update_data = book_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                book[key] = value
            with open("src/fastapiprac/data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return book
    return {"message": "Книга не найдена"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)