from pydantic import BaseModel, ConfigDict


class Form(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    name: str
