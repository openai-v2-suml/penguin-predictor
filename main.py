import os
from pathlib import Path

from fastapi import FastAPI
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

app = FastAPI()

bootstrap_project(Path().cwd())
session_tmp = KedroSession.create("penguins")
catalog = session_tmp.load_context().catalog


@app.post("/run-pipeline/")
def run_pipeline(island: str = "Dream", bill_length_mm: float = 1, bill_depth_mm: float = 1,
                 flipper_length_mm: float = 1, body_mass_g: float = 1, sex: str = "MALE"):
    try:
        with KedroSession.create() as session:
            req = f"island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex\n{island},{bill_length_mm},{bill_depth_mm},{flipper_length_mm},{body_mass_g},{sex}"

            catalog.save("api_data_catalog", req)

            session.run("serving")

            result = catalog.load("api_result")

            print(result)

            return {"result": result}
    except Exception as e:
        print(e)
        return {"error": str(e)}

