import logging
from sqlmodel import Session
from app.middleware.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine)as session:
        init_db(session)
        
def main()-> None:
    logger.info("creating initial data")
    init()
    logger.info("First data created into the database")
    
if __name__ == "__main__":
    main()