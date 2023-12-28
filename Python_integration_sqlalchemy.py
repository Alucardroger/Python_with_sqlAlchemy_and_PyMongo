from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey




Base = declarative_base()


class User(Base):

    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname}) "


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"),nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address},)"

print(User.__tablename__)
print(Address.__tablename__)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspector_engine = inspect(engine)
print(inspector_engine.has_table("user_account"))
print(inspector_engine.get_table_names())
print(inspector_engine.default_schema_name)

with Session(engine) as session:

    roger = User(
        name = 'Roger',
        fullname = 'Roger Bonito',
        address = [Address(email_address='RogerBonito@email.com')]
    )

    thais = User(
        name = 'Thais',
        fullname= 'Thais Cientista',
        address=[Address(email_address='Thais@ciencia.com'),
                 Address(email_address='ThaisdoRoger@mail.com')]
    )

    bob = User(name= 'bob', fullname='bob exponjha')

    session.add_all([roger, thais, bob])

    session.commit()

stmt = select(User).where(User.name.in_(["Roger", 'Thais']))
print('Recuperando usuários filtrados')
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print(f'\nRecuperando os endereços de email de{User.id.in_([2])} ')
for address in session.scalars(stmt_address):
    print(address)

stmt_order = select(User).order_by(User.fullname.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print('\nTotal de instâncias em User')
for result in session.scalars(stmt_count):
    print(result)


session.close()