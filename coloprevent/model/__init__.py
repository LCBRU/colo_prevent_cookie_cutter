from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from lbrc_flask.database import db


class Ordered(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    equipment: Mapped[str] 
    date_ordered: Mapped[date]
    total_requested: Mapped[str]

