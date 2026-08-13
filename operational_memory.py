import os
from typing import List, Optional 
from AIclient import client
from pydantic import BaseModel, Field
import json
from datetime import datetime
from _system_instructions.sys_operational_memory import operational_memory_instructions


""" 
Operational Memory:
{
  "meta": {
    "last_updated": "2026-04-07T09:00:00Z", # Time of last update in ISO format
    "lifecycle_phase": "IDEA", 
    // Options: IDEA, MVP, VALIDATION, GROWTH, SCALE
    "business_day": 12,
    "system_status": "STABLE"
  },
  "credit_ledger": {
    "total_balance": 2450,
    "min_safety_threshold": 1000,
    "status": "HEALTHY", 
    // Options: HEALTHY, WARNING (<1000), CRITICAL (<200)
    ```"burn_rate_avg_7d": 45.5,```
    "credit_valuation_usd": 0.05
  },
  "strategic_anchor": {
    "active_sprint_goal": "Validate core problem statement with 5 target users.",
    "current_bottleneck": "Lack of high-fidelity prototypes.",
    "north_star_metric": "User Interview Completion Rate"
  },
  ```"departmental_deltas": {
    "product": {
      "focus": "Wireframing the landing page.",
      "completion": "40%",
      "blockers": []
    },
    "market_outreach": {
      "active_channels": ["LinkedIn", "Direct Email"],
      "feedback_loops_open": 3,
      "sentiment_summary": "Neutral"
    },
    "operations": {
      "legal_compliance_status": "PENDING",
      "infrastructure_health": "100%"
    }```
  },
  "intelligence_layer": {
	  ```"efficiency_score": 0.85,```
    "market_signals": "No major competitor shifts detected today.",
    "unexpected_learnings": "Users expressed more interest in the 'X' feature than 'Y'.",
    "risk_registry": [
      {"id": "R1", "impact": "High", "description": "High dependence on single API provider."}
    ]
  }
}
 """

# I: 15000, O: 10000
class Meta(BaseModel):
    last_updated: str = Field(..., description="Time of last update in ISO format.")
    lifecycle_phase: str = Field(..., description="Current phase in the product lifecycle. Options: IDEA, MVP, VALIDATION, GROWTH, SCALE")
    business_day: int = Field(..., description="Current business day count since inception.")
    system_status: str = Field(..., description="Overall health status of the system. Options: Stable, Warning, Critical.")

class CreditLedger(BaseModel):
    total_balance: float = Field(..., description="Total balance of credits.")
    min_safety_threshold: float = Field(..., description="Minimum balance before triggering warnings.")
    status: str = Field(..., description="Health status of the credit ledger. Options: Stable, Warning (<1000), Critical (<200).")
    burn_rate: float = Field(..., description="Average burn rate of credits")
    credit_valuation_usd: float = Field(..., description="Current USD valuation per credit unit.")

class StrategicAnchor(BaseModel):
    active_sprint_goal: str = Field(..., description="Current sprint goal guiding the team's efforts.")
    current_bottleneck: str = Field(..., description="Primary bottleneck hindering progress.")
    north_star_metric: str = Field(..., description="Key metric that reflects overall success.")

class IntelligenceLayer(BaseModel):
    efficiency_score: float = Field(..., description="ROI of credits spent vs goals achieved, on a scale of 0 to 1.")
    market_signals: str = Field(..., description="Summary of current market signals.")
    unexpected_learnings: str = Field(..., description="Notable unexpected learnings from recent activities.")
    risk_registry: List[dict] = Field(..., description="List of identified risks with details.")


class OperationalMemory(BaseModel):
    meta: Meta = Field(..., description="Metadata about the operational memory.")
    credit_ledger: CreditLedger = Field(..., description="Financial health and credit information.")
    strategic_anchor: StrategicAnchor = Field(..., description="Current strategic focus and bottlenecks.")
    departmental_deltas: dict = Field(..., description="Current focus and progress of different departments.")
    intelligence_layer: IntelligenceLayer = Field(..., description="Insights and risks from recent activities.")
    evolution_history: Optional[List[str]] = Field(None, description="Historical snapshots of operational memory for tracking changes over time.")






def generate_operational_memory(prompt:str):
    try:
        response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config={
                    "system_instruction": operational_memory_instructions,
                    "response_mime_type": "application/json",
                    "response_json_schema": OperationalMemory.model_json_schema()
                },
                contents=prompt
            )
        r = json.loads(response.text)
        return {"success": True, "data": r}
    except Exception as e:
        print(f"Error generating operational memory: {e}")
        return {"success": False, "error": str(e)}