from math import isfinite
INTERVENTION_SPECS = (
    {
        "name": "prompt", "failure_signals": {"format", "instruction"},
        "requirements": ["prompt_tested"],
        "invasiveness": 1, "cost": 1, "reversible": True,
    },
    {
        "name": "rag", "failure_signals": {"fresh_knowledge", "private_knowledge"},
        "requirements": ["corpus_ready", "retrieval_eval_ready"],
        "invasiveness": 2, "cost": 2, "reversible": True,
    },
    {
        "name": "sft", "failure_signals": {"behavior", "style", "task_pattern"},
        "requirements": ["sft_data_ready", "training_budget_ready"],
        "invasiveness": 3, "cost": 3, "reversible": False,
    },
)


def assess_problem_evidence(evidence: dict[str, object]) -> dict[str, object]:
    """确认可测目标、稳定失败、独立评测和失败切片级基线齐备。"""
    missing = [
        name for name in ("goal_metric", "target_threshold")
        if evidence.get(name) in (None, "")
    ]
    missing += [
        name for name in ("repeatable_failure", "independent_evaluation")
        if evidence.get(name) is not True
    ]
    if "target_threshold" not in missing:
        threshold = evidence["target_threshold"]
        if type(threshold) not in (int, float) or not isfinite(threshold):
            raise ValueError("target_threshold 必须是有限数值")
    failure_slices = set(evidence.get("failure_slices", []))
    if not failure_slices:
        missing.append("failure_slices")
    uncovered = sorted(failure_slices - set(evidence.get("baseline_slices", [])))
    return {
        "ready": not missing and not uncovered,
        "missing_foundations": missing,
        "uncovered_failure_slices": uncovered,
    }


def build_intervention_candidates(
    context: dict[str, object], specifications: tuple | list,
) -> list[dict[str, object]]:
    """按外部规格检查完整机制覆盖和执行条件；requirements 使用布尔状态。"""
    failure_signals = set(context.get("failure_signals", []))
    if not failure_signals:
        raise ValueError("failure_signals 不能为空")
    candidates = []
    for spec in specifications:
        for field in ("invasiveness", "cost"):
            value = spec[field]
            if type(value) not in (int, float) or not isfinite(value) or value < 0:
                raise ValueError(f"{field} 必须是非负有限数值")
        if type(spec["reversible"]) is not bool:
            raise ValueError("reversible 必须是布尔值")
        supported = set(spec["failure_signals"])
        uncovered = sorted(failure_signals - supported)
        missing = [name for name in spec["requirements"] if context.get(name) is not True]
        candidates.append({
            "name": spec["name"],
            "matched_signals": sorted(failure_signals & supported),
            "uncovered_signals": uncovered,
            "mechanism_match": not uncovered,
            "requirements_ready": not missing,
            "missing_requirements": missing,
            "invasiveness": spec["invasiveness"],
            "cost": spec["cost"],
            "reversible": spec["reversible"],
        })
    return candidates


def recommend_minimal_intervention(
    evidence_report: dict[str, object], candidates: list[dict[str, object]],
) -> dict[str, object]:
    """优先低侵入、低成本、可逆；所有候选均不合格时返回阻塞原因。"""
    if not evidence_report["ready"]:
        return {
            "decision": "blocked", "reason": "missing_problem_evidence",
            "missing": evidence_report["missing_foundations"] + evidence_report["uncovered_failure_slices"],
        }
    matching = [candidate for candidate in candidates if candidate["mechanism_match"]]
    selected = min(
        (candidate for candidate in matching if candidate["requirements_ready"]),
        key=lambda candidate: (candidate["invasiveness"], candidate["cost"], not candidate["reversible"]),
        default=None,
    )
    if selected is not None:
        return {"decision": selected["name"], "reason": "minimal_ready_intervention", "missing": []}
    if matching:
        missing = sorted({name for candidate in matching for name in candidate["missing_requirements"]})
        return {"decision": "blocked", "reason": "candidate_requirements_not_ready", "missing": missing}
    uncovered = sorted({signal for candidate in candidates for signal in candidate["uncovered_signals"]})
    return {"decision": "blocked", "reason": "no_full_coverage_candidate", "missing": uncovered}


def self_test():
    """验证证据门、三类方案、完整覆盖、排序和输入边界。"""
    from unittest import TestCase

    check = TestCase()
    evidence = {
        "goal_metric": "accuracy", "target_threshold": 0,
        "repeatable_failure": True, "independent_evaluation": True,
        "failure_slices": ["target_task"], "baseline_slices": ["target_task"],
    }
    ready = assess_problem_evidence(evidence)
    assert ready["ready"]
    missing = assess_problem_evidence({**evidence, "independent_evaluation": False, "baseline_slices": []})
    assert missing["missing_foundations"] == ["independent_evaluation"]
    assert missing["uncovered_failure_slices"] == ["target_task"]
    assert recommend_minimal_intervention(missing, [])["reason"] == "missing_problem_evidence"
    assert assess_problem_evidence({**evidence, "failure_slices": []})["missing_foundations"] == ["failure_slices"]

    for signal, assets, expected in (
        ("format", {"prompt_tested": True}, "prompt"),
        ("fresh_knowledge", {"corpus_ready": True, "retrieval_eval_ready": True}, "rag"),
        ("behavior", {"sft_data_ready": True, "training_budget_ready": True}, "sft"),
        ("behavior", {"sft_data_ready": True}, "blocked"),
    ):
        candidates = build_intervention_candidates({"failure_signals": [signal], **assets}, INTERVENTION_SPECS)
        decision = recommend_minimal_intervention(ready, candidates)
        assert decision["decision"] == expected
        if expected == "blocked":
            assert decision["missing"] == ["training_budget_ready"]

    mixed = build_intervention_candidates({"failure_signals": ["format", "behavior"], "prompt_tested": True}, INTERVENTION_SPECS)
    assert recommend_minimal_intervention(ready, mixed)["reason"] == "no_full_coverage_candidate"
    base = {"failure_signals": {"format"}, "requirements": [], "invasiveness": 1, "cost": 2, "reversible": True}
    alternatives = [
        {**base, "name": "intrusive", "invasiveness": 2, "cost": 0},
        {**base, "name": "expensive", "cost": 3},
        {**base, "name": "irreversible", "reversible": False},
        {**base, "name": "minimal"},
    ]
    candidates = build_intervention_candidates({"failure_signals": ["format"]}, alternatives)
    assert recommend_minimal_intervention(ready, candidates)["decision"] == "minimal"
    with check.assertRaises(ValueError):
        build_intervention_candidates({}, INTERVENTION_SPECS)
    for value in (float("nan"), float("inf"), -1):
        with check.assertRaises(ValueError):
            build_intervention_candidates({"failure_signals": ["format"]}, [{**base, "name": "invalid", "cost": value}])
    with check.assertRaises(ValueError):
        assess_problem_evidence({**evidence, "target_threshold": float("nan")})


def run_demo():
    """使用合成输入展示 Prompt、RAG、SFT 和阻塞四种结果。"""
    from json import dumps

    evidence = assess_problem_evidence({
        "goal_metric": "accuracy", "target_threshold": 0.9,
        "repeatable_failure": True, "independent_evaluation": True,
        "failure_slices": ["target_task"], "baseline_slices": ["target_task"],
    })
    scenarios = (
        ("格式问题：选择 Prompt", "format", {"prompt_tested": True}),
        ("新知识问题：选择 RAG", "fresh_knowledge", {"corpus_ready": True, "retrieval_eval_ready": True}),
        ("行为问题：SFT 准入通过", "behavior", {"sft_data_ready": True, "training_budget_ready": True}),
        ("行为问题：预算未就绪", "behavior", {"sft_data_ready": True, "training_budget_ready": False}),
    )
    for label, signal, assets in scenarios:
        candidates = build_intervention_candidates({"failure_signals": [signal], **assets}, INTERVENTION_SPECS)
        print(f"\n{label}")
        print(dumps(recommend_minimal_intervention(evidence, candidates), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    self_test()
    print("微调准入与最小干预自检全部通过。")
    run_demo()
