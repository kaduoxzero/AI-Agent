from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4


class AuthorizationError(RuntimeError):
    pass


@dataclass(frozen=True)
class UserIdentity:
    user_id: str
    tenant_id: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class AgentIdentity:
    agent_id: str
    tenant_id: str


@dataclass(frozen=True)
class Delegation:
    user_id: str
    agent_id: str
    tenant_id: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class Credential:
    token_id: str
    subject_agent_id: str
    on_behalf_of_user_id: str
    tenant_id: str
    scopes: frozenset[str]
    expires_at: datetime

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at


class CredentialBroker:
    def __init__(self) -> None:
        self.audit: list[dict[str, object]] = []

    def issue(
        self,
        user: UserIdentity,
        agent: AgentIdentity,
        delegation: Delegation,
        requested_scopes: set[str],
        ttl_seconds: int = 300,
    ) -> Credential:
        if user.tenant_id != agent.tenant_id or user.tenant_id != delegation.tenant_id:
            raise AuthorizationError("tenant mismatch")

        if delegation.user_id != user.user_id or delegation.agent_id != agent.agent_id:
            raise AuthorizationError("delegation subject mismatch")

        if not delegation.scopes.issubset(user.scopes):
            raise AuthorizationError("delegation exceeds user scopes")

        requested = frozenset(requested_scopes)
        if not requested.issubset(delegation.scopes):
            raise AuthorizationError("agent requested scopes outside delegated boundary")

        credential = Credential(
            token_id=str(uuid4()),
            subject_agent_id=agent.agent_id,
            on_behalf_of_user_id=user.user_id,
            tenant_id=user.tenant_id,
            scopes=requested,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds),
        )

        self.audit.append(
            {
                "event": "CredentialIssued",
                "token_id": credential.token_id,
                "user_id": user.user_id,
                "agent_id": agent.agent_id,
                "tenant_id": user.tenant_id,
                "scopes": sorted(credential.scopes),
                "expires_at": credential.expires_at.isoformat(),
            }
        )
        return credential

    def authorize(self, credential: Credential, required_scope: str, tenant_id: str) -> None:
        if credential.is_expired():
            raise AuthorizationError("credential expired")
        if credential.tenant_id != tenant_id:
            raise AuthorizationError("tenant mismatch")
        if required_scope not in credential.scopes:
            raise AuthorizationError(f"missing scope: {required_scope}")

        self.audit.append(
            {
                "event": "CredentialAuthorized",
                "token_id": credential.token_id,
                "scope": required_scope,
                "tenant_id": tenant_id,
            }
        )


def main() -> None:
    user = UserIdentity(
        user_id="user-001",
        tenant_id="tenant-a",
        scopes=frozenset({"supplier:read", "supplier:write"}),
    )
    agent = AgentIdentity(agent_id="agent-risk", tenant_id="tenant-a")

    # 用户只委派 read，即使用户本人有 write，Agent 也不能自动继承。
    delegation = Delegation(
        user_id=user.user_id,
        agent_id=agent.agent_id,
        tenant_id="tenant-a",
        scopes=frozenset({"supplier:read"}),
    )

    broker = CredentialBroker()

    print("=== issue read-only credential ===")
    credential = broker.issue(
        user,
        agent,
        delegation,
        requested_scopes={"supplier:read"},
        ttl_seconds=300,
    )
    print(credential)

    print("\n=== authorize read ===")
    broker.authorize(credential, "supplier:read", "tenant-a")
    print("READ ALLOWED")

    print("\n=== attempt privilege escalation ===")
    try:
        broker.issue(
            user,
            agent,
            delegation,
            requested_scopes={"supplier:write"},
        )
    except AuthorizationError as exc:
        print("REJECTED:", exc)

    print("\n=== attempt cross-tenant use ===")
    try:
        broker.authorize(credential, "supplier:read", "tenant-b")
    except AuthorizationError as exc:
        print("REJECTED:", exc)

    print("\n=== audit ===")
    for event in broker.audit:
        print(event)


if __name__ == "__main__":
    main()
