from fastapi import FastAPI, Path, HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated,Optional
from typing import Literal
from pydantic import computed_field

import json

app = FastAPI()

class Patient(BaseModel):#pydantic model
    id: Annotated[str,Field(...,description='The unique identifier for the patient',example='P001')]
    name:Annotated[str,Field(...,description='The name of the patient',example='Ashish Shetty')]
    city:Annotated[str,Field(...,description='The city where the patient lives',example='New York')]
    age:Annotated[int,Field(...,description='The age of the patient',example=30)]
    gender:Annotated[Literal['male','female','other'],Field(...,description='The gender of the patient')]
    height:Annotated[float,Field(..., gt=0,description='The height of the patient in mtrs',example=175.5)]
    weight:Annotated[float,Field(..., gt=0,description='The weight of the patient in kgs',example=70.0)]

    @ computed_field
    def bmi(self) -> float:
        bmi=round(self.weight / (self.height ** 2),2)
        return bmi
    @computed_field
    def health_status(self) -> str:
        bmi=self.bmi
        if bmi<18.5:
            return 'Underweight'
        elif 18.5<=bmi<25:
            return 'Normal weight'
        elif 25<=bmi<30:
            return 'Overweight'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None, gt=0)]
    weight:Annotated[Optional[float],Field(default=None, gt=0)]



def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def home():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {
        "about": "A fully functional API for managing patient records."
    }

@app.get("/view")
def view():
    return load_data()

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(..., description="The ID of the patient to retrieve",example="12345")):
    #load all the patients
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")
#Query PArameter
@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='sort on the basis of height,weight and bmi'),order:str=Query('asc',description='sort in asc or desc order')):
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,
                            detail='Invalid field select from{valid_fields}')
    if order not in['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data=load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=False)
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):
    #1.load existing data
    data=load_data()
    #2.check if patient with same id already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient with this ID already exists')
    #3.add new patient to database
    data[patient.id]=patient.model_dump(exclude=['id'])
    #save into json file
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"Patient created successfully","patient":data[patient.id]})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient: PatientUpdate):

    data_load=load_data()

    if patient_id not in data_load:#check if patient exists
        raise HTTPException(status_code=404,detail='Patient not found')
    existing_patient_info=data_load[patient_id]#dic of existing patient data
    #patient_data=patient.model_dump(exclude_unset=True)#dic of only the fields that are provided in the request body
    updated_patient_info=patient.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value

    #existing_patient_info ->pydantic object -> updated bmi+verdict
    existing_patient_info['id']=patient_id
    patient_pydantic_obj=Patient(**existing_patient_info)
    #convert back to dict
    existing_patient_info=patient_pydantic_obj.model_dump(exclude=['id'])
    #update the existing patient data with the new data
    data_load[patient_id]=existing_patient_info

    #save updated data into json file
    save_data(data_load)
    return JSONResponse(status_code=200,content={"message":"Patient updated successfully","patient":data_load[patient_id]})
 # Delete end-point
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={"message":"Patient deleted successfully"})
