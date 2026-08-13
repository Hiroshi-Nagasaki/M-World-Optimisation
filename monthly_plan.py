import os
from typing import List, Optional 
from AIclient import client
from pydantic import BaseModel, Field
import json
from _system_instructions.sys_monthly_plan import monthly_plan_instructions


class KPI(BaseModel):
    name: str
    target: str
    rationale: str


class SprintBudgetDistribution(BaseModel):
    sprint_number_in_month: int = Field(..., ge=1)
    percentage_of_total_credits: float = Field(..., ge=0, le=100)
    rationale: str = Field(..., description="Why this sprint gets this share")



class MonthlyPlanOutput(BaseModel):

    year: int = Field(..., ge=1)

    month_index: int = Field(..., ge=1, le=12)
    month_name: str

    title: str
    monthly_goal: str
    why_this_month: str


    sprint_credit_distribution: List[SprintBudgetDistribution]

    priorities: List[str]
    kpis_targeted: List[KPI]
    dependencies: List[str]
    risks: List[str]
    execution_notes: List[str]

#I:20000, O:10000
def generate_monthly_plan(prompt:str):
    try:
        response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config={
                    "system_instruction": monthly_plan_instructions,
                    "response_mime_type": "application/json",
                    "response_schema": MonthlyPlanOutput,
                },
                contents=prompt
            )
        r = json.loads(response.text)
        return {"success": True, "data": r}
    except Exception as e:
        print(f"Error generating monthly plan: {e}")
        return {"success": False, "error": str(e)}