from __future__ import annotations

from packages.contracts import ApprovalStatus, TaskRecord


class PolicyEngine:
    HIGH_IMPACT_TERMS = {
        "删除",
        "delete",
        "转账",
        "transfer money",
        "暂停采购",
        "disable account",
        "terminate",
    }

    def requires_approval(self, task: TaskRecord) -> bool:
        query = task.query.lower()
        return any(term in query for term in self.HIGH_IMPACT_TERMS)

    def scopes_for(self, task: TaskRecord) -> set[str]:
        # In production derive scopes from user delegation + agent identity + tool policy.
        return {"data:read", "web:read", "knowledge:read"}

    def can_execute(self, task: TaskRecord) -> bool:
        if not self.requires_approval(task):
            return True
        return task.approval_status == ApprovalStatus.APPROVED
