from dataclasses import dataclass


@dataclass
class RuleResult:
    passed: bool
    score: float
    findings: dict


class StrategyEngine:
    """Evaluates modular JSON strategy definitions against structure context."""

    def evaluate(self, strategy: dict, context: dict) -> RuleResult:
        required = strategy.get("required_confluences", [])
        findings = context.get("findings", {})

        passed = True
        score = 0.0
        for rule in required:
            hit = bool(findings.get(rule))
            weight = float(strategy.get("weights", {}).get(rule, 1.0))
            if hit:
                score += weight
            else:
                passed = False

        max_score = sum(float(strategy.get("weights", {}).get(r, 1.0)) for r in required) or 1.0
        normalized = round((score / max_score) * 100, 2)
        return RuleResult(passed=passed, score=normalized, findings=findings)
