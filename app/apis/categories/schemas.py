from pydantic import BaseModel, constr

NameStr = constr(strip_whitespace=True, min_length=1, max_length=50)

class CategoryBase(BaseModel):
    name: NameStr

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    user_id: int 

    class Config:
        from_attributes = True