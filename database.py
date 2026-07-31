from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Update this URL with your PostgreSQL credentials and database name
# root%40123 is the encoded form of root@123

db_url = "postgresql://postgres:root%40123@localhost:5432/ashu"
engine = create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
