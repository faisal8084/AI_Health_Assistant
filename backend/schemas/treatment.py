from pydantic import BaseModel,Field
from typing import Literal

class treatmentInput(BaseModel):

    Age : float = Field(...,ge=0,le=120)

    Gender : Literal["Female", "Male", "Other"]

    self_employed : Literal["No", "Yes"]

    family_history : Literal["No", "Yes"]

    work_interfere : Literal['Often', 'Rarely', 'Never', 'Sometimes', 'Unknown']

    no_employees : Literal['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']

    remote_work : Literal["No", "Yes"]

    tech_company : Literal["Yes", "No"]

    benefits : Literal['Yes', "Don't know", 'No']

    care_options : Literal['Not sure', 'No', 'Yes']

    wellness_program : Literal['No', "Don't know", 'Yes']

    seek_help : Literal['Yes', "Don't know", 'No']

    anonymity : Literal['Yes', "Don't know", 'No']

    leave : Literal['Somewhat easy', "Don't know", 'Somewhat difficult', 'Very difficult', 'Very easy']

    mental_health_consequence: Literal['No', 'Maybe', 'Yes']

    phys_health_consequence: Literal['No', 'Yes', 'Maybe']

    coworkers: Literal['Some of them', 'No', 'Yes']

    supervisor: Literal['Yes', 'No', 'Some of them']

    mental_health_interview: Literal['No', 'Yes', 'Maybe']

    phys_health_interview: Literal['Maybe', 'No', 'Yes']

    mental_vs_physical: Literal['Yes', "Don't know", 'No']

    obs_consequence: Literal['No', 'Yes']

    Country: str

