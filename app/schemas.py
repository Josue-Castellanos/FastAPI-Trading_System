from models import PostBase


# class Post(PostBase, table=True):
#     id: int = Field(nullable=False, primary_key=True, unique=True)
#     published: Optional[bool] = Field(nullable=False, default=True,
#         sa_column_kwargs={
#             "server_default": text("1")
#         }
#     )
#     created: datetime = Field(
#         sa_column_kwargs={
#             "server_default": text("CURRENT_TIMESTAMP"),
#             "nullable": False
#         }
#     )
#     last_modified: Optional[datetime] = Field(
#         sa_column_kwargs={
#             "server_default": text("NULL ON UPDATE CURRENT_TIMESTAMP"),
#             "nullable": True
#         }
#     )