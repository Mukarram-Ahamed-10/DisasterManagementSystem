from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class DisasterReport:
    report_id: Optional[int] = None
    location: str = ""
    disaster_type: str = ""
    severity: int = 0
    report_date: Optional[datetime] = None
    description: str = ""
    status: str = "Active"

@dataclass
class ReliefResource:
    resource_id: Optional[int] = None
    resource_name: str = ""
    quantity: int = 0
    unit: str = ""
    cost_per_unit: float = 0.0

@dataclass
class ResourceAllocation:
    allocation_id: Optional[int] = None
    report_id: int = 0
    resource_id: int = 0
    allocated_quantity: int = 0
    allocation_date: Optional[datetime] = None

@dataclass
class Donation:
    donation_id: Optional[int] = None
    donor_name: str = ""
    donor_email: str = ""
    amount: float = 0.0
    donation_date: Optional[datetime] = None
    disaster_id: Optional[int] = None
    message: str = ""

@dataclass
class SafetyPolicy:
    policy_id: Optional[int] = None
    disaster_type: str = ""
    title: str = ""
    content: str = ""
    priority: int = 1
    last_updated: Optional[datetime] = None

@dataclass
class DisasterNews:
    news_id: Optional[int] = None
    title: str = ""
    content: str = ""
    news_type: str = ""  # 'warning', 'prediction', 'update'
    severity: int = 1
    location: str = ""
    publish_date: Optional[datetime] = None
    is_active: bool = True
