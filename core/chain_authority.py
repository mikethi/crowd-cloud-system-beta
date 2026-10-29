"""Provider-neutral chain authority contracts.

IMPORTANT:
This module does not implement blockchain consensus, finality, persistence,
cryptographic authentication, or network access.

A real provider adapter must derive authoritative status from the actual
chain provider's documented rules. The included in-memory test double is
simulation-only and must never be treated as a production chain.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable


class AuthorityStatus(str, Enum):
    FINALIZED = "finalized"
    PENDING = "pending"
    UNAVAILABLE = "unavailable"
    CONFLICTING = "conflicting"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ChainDecision:
    """A decision returned by a chain provider.

    decision_id must be stable according to the provider's contract.
    code_hash and policy_ref are references, not proof of authorization.
    """

    decision_id: str
    status: AuthorityStatus
    sequence: int | None = None
    code_hash: str | None = None
    policy_ref: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.decision_id, str) or not self.decision_id.strip():
            raise ValueError("decision_id must be a non-empty string")

        if not isinstance(self.status, AuthorityStatus):
            raise ValueError("status must be an AuthorityStatus")

        if self.sequence is not None:
            if type(self.sequence) is not int or self.sequence < 0:
                raise ValueError("sequence must be a non-negative integer")

        for field_name in ("code_hash", "policy_ref"):
            value = getattr(self, field_name)
            if value is not None:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"{field_name} must be None or non-empty")


@dataclass(frozen=True)
class AuthoritySnapshot:
    """One adapter response; this is not itself proof of consensus."""

    status: AuthorityStatus
    decisions: tuple[ChainDecision, ...] = ()
    detail: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, AuthorityStatus):
            raise ValueError("status must be an AuthorityStatus")

        if not isinstance(self.decisions, tuple):
            raise ValueError("decisions must be a tuple")

        if any(not isinstance(d, ChainDecision) for d in self.decisions):
            raise ValueError("decisions must contain ChainDecision values")

        if self.detail is not None and not isinstance(self.detail, str):
            raise ValueError("detail must be a string or None")

        if self.status is not AuthorityStatus.FINALIZED and self.decisions:
            raise ValueError(
                "non-finalized snapshots must not expose actionable decisions"
            )

        if self.status is AuthorityStatus.FINALIZED:
            ids = [d.decision_id for d in self.decisions]
            if len(ids) != len(set(ids)):
                raise ValueError("duplicate decision IDs in snapshot")

            if any(d.status is not AuthorityStatus.FINALIZED for d in self.decisions):
                raise ValueError(
                    "finalized snapshot may contain only finalized decisions"
                )

            sequences = [
                d.sequence for d in self.decisions if d.sequence is not None
            ]
            if sequences != sorted(sequences):
                raise ValueError("decisions must be ordered by sequence")


@runtime_checkable
class ChainAuthority(Protocol):
    """Required interface for a future real chain-provider adapter."""

    def read_authority(self) -> AuthoritySnapshot:
        """Return a provider-derived status and ordered finalized decisions."""
        ...


class AuthorityUnavailable(RuntimeError):
    """No usable authority result is available."""


class AuthorityConflict(RuntimeError):
    """The provider reports conflicting or ambiguous authority."""


class DecisionNotFinalized(RuntimeError):
    """The requested decision is not confirmed finalized."""


def require_finalized(snapshot: AuthoritySnapshot) -> tuple[ChainDecision, ...]:
    """Return decisions only for an explicitly finalized snapshot.

    This is a gate, not a consensus algorithm. Trust in FINALIZED must come
    from a real provider adapter and its documented verification rules.
    """

    if snapshot.status is AuthorityStatus.UNAVAILABLE:
        raise AuthorityUnavailable(snapshot.detail or "chain authority unavailable")

    if snapshot.status is AuthorityStatus.CONFLICTING:
        raise AuthorityConflict(snapshot.detail or "conflicting chain authority")

    if snapshot.status is not AuthorityStatus.FINALIZED:
        raise DecisionNotFinalized(
            f"chain authority is {snapshot.status.value}, not finalized"
        )

    return snapshot.decisions


class InMemoryAuthorityDouble:
    """SIMULATION ONLY. Never use this as a production chain adapter.

    This object accepts decisions supplied directly by a test. It does not
    authenticate the submitter, validate a chain, or establish consensus.
    """

    def __init__(self, snapshot: AuthoritySnapshot | None = None) -> None:
        self._snapshot = snapshot or AuthoritySnapshot(
            status=AuthorityStatus.UNKNOWN,
            detail="simulation has no configured authority result",
        )

    def set_snapshot(self, snapshot: AuthoritySnapshot) -> None:
        if not isinstance(snapshot, AuthoritySnapshot):
            raise TypeError("snapshot must be an AuthoritySnapshot")
        self._snapshot = snapshot

    def read_authority(self) -> AuthoritySnapshot:
        return self._snapshot


class FinalizedDecisionConsumer:
    """In-memory idempotency example for tests only.

    It records which decision IDs were consumed. It does not persist state,
    execute code, perform placement, or authorize a decision independently.
    """

    def __init__(self) -> None:
        self._consumed: set[str] = set()

    @property
    def consumed_ids(self) -> frozenset[str]:
        return frozenset(self._consumed)

    def consume(self, snapshot: AuthoritySnapshot) -> tuple[str, ...]:
        decisions = require_finalized(snapshot)
        newly_consumed = []

        for decision in decisions:
            if decision.decision_id not in self._consumed:
                self._consumed.add(decision.decision_id)
                newly_consumed.append(decision.decision_id)

        return tuple(newly_consumed)
