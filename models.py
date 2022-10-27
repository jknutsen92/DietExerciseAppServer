from pydantic   import BaseModel, validator, constr, confloat, conint
from typing     import Optional, List
from datetime   import datetime, date
from validators import url, email
from enum       import Enum
from re         import match


class Macros(BaseModel):
    total_fat:          confloat(ge=0.0)
    saturated_fat:      confloat(ge=0.0)
    cholesterol:        confloat(ge=0.0)
    sodium:             confloat(ge=0.0)
    carbohydrates:      confloat(ge=0.0)
    dietary_fiber:      confloat(ge=0.0)
    sugars:             confloat(ge=0.0)
    protein:            confloat(ge=0.0)
    potassium:          confloat(ge=0.0)


class FoodEntry(BaseModel):
    name:               constr(max_length=75)
    calories:           confloat(ge=0.0)
    num_servings:       confloat(gt=0.0)
    serving_qty:        conint(gt=0)
    serving_unit:       constr(max_length=50)
    serving_weight:     confloat(gt=0.0)
    macros:             Macros
    image_url:          Optional[constr(max_length=2048)]
    timeEaten:          datetime

    @validator("image_url")
    def url_must_be_valid(cls, image_url):
        if not url(image_url):
            raise ValueError(f"{image_url} is not a valid URL")
        return image_url

    
class FoodItemEaten(BaseModel):
    user_id:            int
    food_id:            constr(min_length=40, max_length=40, regex=r"^[\dA-Fa-f]{40}$")
    time_consumed:      datetime
    servings:           confloat(gt=0.0)


class FoodItem(BaseModel):
    id:                 constr(min_length=40, max_length=40, regex=r"^[\dA-Fa-f]{40}$")
    name:               constr(max_length=75)
    calories:           confloat(ge=0.0)
    total_fat:          confloat(ge=0.0)
    saturated_fat:      confloat(ge=0.0)
    cholesterol:        confloat(ge=0.0)
    sodium:             confloat(ge=0.0)
    carbohydrates:      confloat(ge=0.0)
    dietary_fiber:      confloat(ge=0.0)
    sugars:             confloat(ge=0.0)
    protein:            confloat(ge=0.0)
    serving_qty:        conint(gt=0)
    serving_unit:       constr(max_length=50)
    serving_weight:     confloat(ge=0.0)
    image_url:          Optional[constr(max_length=2048)]

    @validator("image_url")
    def url_must_be_valid(cls, image_url):
        if not url(image_url):
            raise ValueError(f"{image_url} is not a valid URL")
        return image_url


class ExerciseEntry(BaseModel):
    name:               constr(max_length=50)
    calories_per_hour:  confloat(gt=0.0)
    time_completed:     datetime
    duration:           confloat(gt=0.0)


class ExerciseDone(BaseModel):
    user_id:            int
    exercise_id:        constr(min_length=40, max_length=40, regex=r"^[\dA-Fa-f]{40}$")
    time_completed:     datetime
    duration:           confloat(ge=0.0)


class ExerciseItem(BaseModel):
    id:                 constr(min_length=40, max_length=40, regex=r"^[\dA-Fa-f]{40}$")
    name:               constr(max_length=50)
    calories_per_hour:  confloat(gt=0.0)


class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class NewUserInfo(BaseModel):
    first_name:         constr(max_length=50)
    last_name:          constr(max_length=50)
    email:              constr(max_length=100)
    password:           constr(regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
    goal_id:            Optional[int]
    birthdate:          date
    weight:             confloat(gt=0.0)
    height:             confloat(gt=0.0)
    gender:             GenderEnum

    @validator("email")
    def email_must_be_valid(cls, userEmail):
        if not email(userEmail):
            raise ValueError(f"{userEmail} is not a valid email address")
        return userEmail


class UserMeasures(BaseModel):
    weight:             confloat(gt=0.0)
    height:             Optional[confloat(gt=0.0)]


class UserInfo(BaseModel):
    first_name:         constr(max_length=50)
    last_name:          constr(max_length=50)
    email:              constr(max_length=100)
    goal_id:            Optional[int]
    birthdate:          date
    weight:             confloat(gt=0.0)
    height:             confloat(gt=0.0)
    gender:             GenderEnum

    @validator("email")
    def email_must_be_valid(cls, userEmail):
        if not email(userEmail):
            raise ValueError(f"{userEmail} is not a valid email address")
        return userEmail