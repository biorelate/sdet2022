from datetime import datetime
from sqlite3 import IntegrityError
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, create_engine  # noqa
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///../data/sql_app.db"

app = FastAPI()


# Database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Middleware
@app.middleware("http")
def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = call_next(request)
    finally:
        request.state.db.close()
    return response


# CORS
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization, X-Requested-With, X-HTTP-Method-Override"
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


# Schemas
class DocumentSchema(BaseModel):
    doc_id: int
    title: str
    date: datetime
    url: str
    # In the spirit of keeping things simple for the test, let's not bother
    # with the many-to-manies here and just hard-code 2 concepts and one author
    author: str  # Nasty hack
    concept1: str  # Nasty hack
    concept2: str  # Nasty hack

    class Config:
        orm_mode = True


# Models
class DocumentModel(Base):
    __tablename__ = "document"

    doc_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(DateTime)
    snippet = Column(String)
    url = Column(String)
    # In the spirit of keeping things simple for the test, let's not bother
    # with the many-to-manies here and just hard-code 2 concepts and one author
    author = Column(String)  # Nasty hack
    concept1 = Column(String)  # Nasty hack
    concept2 = Column(String)  # Nasty hack


Base.metadata.create_all(bind=engine)

# CRUD
def delete_document(db: Session, document: DocumentSchema) -> None:
    try:
        db.delete(document)
        db.commit()
    except (IntegrityError, SQLAIntegrityError):
        raise HTTPException(status_code=400)


def create_document(db: Session, document: DocumentSchema) -> DocumentModel:
    db_item = DocumentModel(**document.dict())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except (IntegrityError, SQLAIntegrityError):
        db.rollback()
        raise HTTPException(status_code=400)


def get_documents(db: Session, skip: int = 0, limit: int = 100) -> List:
    return db.query(DocumentModel).offset(skip).limit(limit).all()


# Routers
@app.get(
    "/document",
    response_model=List[DocumentSchema],
)
def list_documents(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> List[DocumentSchema]:
    return get_documents(db=db, skip=skip, limit=limit)


@app.post(
    "/document",
    response_model=DocumentSchema,
    include_in_schema=False,
)
def create_documents(
    document: DocumentSchema,
    db: Session = Depends(get_db),
) -> DocumentSchema:
    return create_document(db=db, document=document)
