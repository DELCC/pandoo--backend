from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "utilisateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password : Mapped[str] = mapped_column(String,nullable=False)
    children: Mapped[list["Child"]] = relationship(
        back_populates="parent"
    )


class Child(Base):
    __tablename__ = "enfants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    id_parent: Mapped[int] = mapped_column(
        ForeignKey("utilisateurs.id")
    )

    parent: Mapped["User"] = relationship(
        back_populates="children"
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="child"
    )


class Product(Base):
    __tablename__ = "produits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bare_code: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)

    calories: Mapped[float] = mapped_column(Float)
    calcium: Mapped[float] = mapped_column(Float)
    proteins: Mapped[float] = mapped_column(Float)
    lipids: Mapped[float] = mapped_column(Float)
    salt: Mapped[float] = mapped_column(Float)

    id_child: Mapped[int] = mapped_column(
        ForeignKey("enfants.id")
    )

    child: Mapped["Child"] = relationship(
        back_populates="products"
    )