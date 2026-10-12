from math import isfinite
def assess_problem_evidence(evidence: dict[str, object]) -> dict[str, object]:
    """检查复测次数、失败率、评测隔离与基线覆盖。"""
    required_fields = ["goal_metric", "target_threshold", "minimum_repeats", "minimum_failure_rate", "failure_runs"]
    baseline_slices = set(evidence.get("baseline_slices", []))
    missing_fields = [name for name in required_fields if evidence.get(name) in (None, "")]
    failed_checks = [] if evidence.get("evaluation_ids_isolated") is True else ["evaluation_ids_isolated"]
    minimum_repeats = 1 if "minimum_repeats" in missing_fields else evidence["minimum_repeats"]
    minimum_failure_rate = 0.0 if "minimum_failure_rate" in missing_fields else float(evidence["minimum_failure_rate"])
    if type(minimum_repeats) is not int or minimum_repeats <= 0:
        raise ValueError("minimum_repeats 必须是正整数")
    if not 0 <= minimum_failure_rate <= 1:
        raise ValueError("minimum_failure_rate 必须在 [0, 1] 内")
    if "target_threshold" not in missing_fields and not isfinite(float(evidence["target_threshold"])):
        raise ValueError("target_threshold 必须是有限数值")

    repeatable_failure_slices = []
    failure_runs = {} if "failure_runs" in missing_fields else evidence["failure_runs"]
    for name, run in failure_runs.items():
        attempts, failures = run["attempts"], run["failures"]
        if type(attempts) is not int or type(failures) is not int or not 0 <= failures <= attempts:
            raise ValueError(f"切片 {name} 必须满足整数计数 0 <= failures <= attempts")
        if attempts >= minimum_repeats and failures > 0 and failures / attempts >= minimum_failure_rate:
            repeatable_failure_slices.append(name)
    repeatable_failure_slices.sort()
    if not repeatable_failure_slices:
        failed_checks.append("repeatable_failure_slices")
    uncovered_failure_slices = sorted(set(repeatable_failure_slices) - baseline_slices)
    return {
        "ready": not missing_fields and not failed_checks and not uncovered_failure_slices,
        "repeatable_failure_slices": repeatable_failure_slices,
        "missing_fields": missing_fields,
        "failed_checks": failed_checks,
        "uncovered_failure_slices": uncovered_failure_slices,
    }


def assess_parameter_update_need(
    failure_slices: list[str],
    candidate_results: list[dict[str, object]],
    target_threshold: float,
    *,
    higher_is_better: bool = True,
) -> dict[str, object]:
    """每个失败切片都须有候选评测；错误率或损失使用 higher_is_better=False。"""
    target_threshold = float(target_threshold)
    if not isfinite(target_threshold):
        raise ValueError("target_threshold 必须是有限数值")
    if type(higher_is_better) is not bool:
        raise ValueError("higher_is_better 必须是布尔值")
    repeatable_failures = set(failure_slices)
    evaluated_slices = {item["failure_slice"] for item in candidate_results}
    unknown_slices = sorted(evaluated_slices - repeatable_failures)
    if unknown_slices:
        raise ValueError(f"候选结果包含未登记切片：{unknown_slices}")
    unevaluated_slices = sorted(repeatable_failures - evaluated_slices)
    if unevaluated_slices:
        raise ValueError(f"失败切片缺少非参数候选评测：{unevaluated_slices}")
    resolved_slices = set()
    for item in candidate_results:
        value = float(item["metric_value"])
        if not isfinite(value):
            raise ValueError("metric_value 必须是有限数值")
        introduced_failures = item.get("introduced_failures", [])
        if not isinstance(introduced_failures, list):
            raise ValueError("introduced_failures 必须是列表")
        meets_target = value >= target_threshold if higher_is_better else value <= target_threshold
        if meets_target and not introduced_failures:
            resolved_slices.add(item["failure_slice"])
    residual_parameter_slices = sorted(repeatable_failures - resolved_slices)
    return {
        "parameter_update_required": bool(residual_parameter_slices),
        "resolved_slices": sorted(resolved_slices),
        "residual_parameter_slices": residual_parameter_slices,
    }


def select_next_training_stage(
    evidence_report: dict[str, object],
    parameter_report: dict[str, object],
    context: dict[str, object],
) -> dict[str, object]:
    if not evidence_report["ready"]:
        missing = evidence_report["missing_fields"] + evidence_report["failed_checks"] + evidence_report["uncovered_failure_slices"]
        return {"decision": "blocked", "reason": "missing_problem_evidence", "missing": missing}
    if not parameter_report["parameter_update_required"]:
        return {"decision": "no_parameter_update", "reason": "non_parameter_baseline_resolved_failures", "missing": []}
    parameter_gap = context.get("parameter_gap", "behavior")
    feedback_mode = context.get("feedback_mode", "demonstrations")
    if parameter_gap not in ("representation", "behavior"):
        raise ValueError(f"未知 parameter_gap：{parameter_gap}")
    requirements = {
        "continued_pretraining": ["domain_corpus_version", "evaluation_manifest", "training_budget_gpu_hours"],
        "sft": ["demonstration_dataset_version", "evaluation_manifest", "training_budget_gpu_hours"],
        "offline_preference": ["sft_baseline_manifest", "preference_dataset_version", "evaluation_manifest"],
        "online_rl": ["sft_baseline_manifest", "reward_model_version", "exploration_required", "rollout_budget", "rollback_checkpoint"],
        "rlvr": ["sft_baseline_manifest", "verifier_version", "exploration_required", "rollout_budget", "rollback_checkpoint"],
    }
    if parameter_gap == "representation":
        next_stage = "continued_pretraining"
    elif context.get("sft_baseline_ready") is not True:
        next_stage = "sft"
    elif feedback_mode == "demonstrations":
        return {"decision": "stop_at_sft", "reason": "no_new_feedback_signal", "missing": []}
    else:
        next_stage = {
            "preference_pairs": "offline_preference",
            "learned_reward": "online_rl",
            "verifier": "rlvr",
        }.get(feedback_mode)
        if next_stage is None:
            raise ValueError(f"未知 feedback_mode：{feedback_mode}")
    missing = []
    for name in requirements[next_stage]:
        value = context.get(name)
        if name in ("training_budget_gpu_hours", "rollout_budget"):
            valid = type(value) in (int, float) and isfinite(value) and value > 0
        elif name == "exploration_required":
            valid = value is True
        else:
            valid = bool(value)
        if not valid:
            missing.append(name)
    if missing:
        return {"decision": "blocked", "reason": "stage_requirements_not_ready", "missing": missing}
    return {"decision": next_stage, "reason": "stage_requirements_ready", "missing": []}


def test_problem_evidence_gate():
    """分别报告字段缺失、检查未通过和切片未覆盖。"""
    missing = assess_problem_evidence({"goal_metric": "accuracy", "minimum_repeats": 3, "minimum_failure_rate": 0.6, "failure_runs": {"json_format": {"attempts": 3, "failures": 2}}, "evaluation_ids_isolated": True, "baseline_slices": ["json_format"]})
    assert missing == {"ready": False, "repeatable_failure_slices": ["json_format"], "missing_fields": ["target_threshold"], "failed_checks": [], "uncovered_failure_slices": []}
    report = assess_problem_evidence({"goal_metric": "accuracy", "target_threshold": 0.9, "minimum_repeats": 3, "minimum_failure_rate": 0.6, "failure_runs": {"json_format": {"attempts": 3, "failures": 2}, "long_input": {"attempts": 4, "failures": 3}, "rare": {"attempts": 2, "failures": 2}}, "evaluation_ids_isolated": False, "baseline_slices": ["json_format"]})
    assert report == {"ready": False, "repeatable_failure_slices": ["json_format", "long_input"], "missing_fields": [], "failed_checks": ["evaluation_ids_isolated"], "uncovered_failure_slices": ["long_input"]}


def test_parameter_update_gate():
    """只有不修改参数的方案复测后仍存在的失败才能进入参数更新。"""
    results = [{"failure_slice": "format", "metric_value": 0.94, "introduced_failures": []}, {"failure_slice": "fresh_knowledge", "metric_value": 0.91, "introduced_failures": []}]
    resolved = assess_parameter_update_need(["format", "fresh_knowledge"], results, 0.9)
    assert resolved == {"parameter_update_required": False, "resolved_slices": ["format", "fresh_knowledge"], "residual_parameter_slices": []}
    residual = assess_parameter_update_need(["format", "behavior"], [{"failure_slice": "format", "metric_value": 0.95, "introduced_failures": []}, {"failure_slice": "behavior", "metric_value": 0.92, "introduced_failures": ["safety"]}], 0.9)
    assert residual == {"parameter_update_required": True, "resolved_slices": ["format"], "residual_parameter_slices": ["behavior"]}
    try:
        assess_parameter_update_need(["format"], [{"failure_slice": "unknown", "metric_value": 0.99, "introduced_failures": []}], 0.9)
    except ValueError:
        pass
    else:
        raise AssertionError("未登记切片不应进入候选结果")


def test_training_stage_branches():
    """参数缺口、SFT 基线与反馈形态共同决定下一训练阶段。"""
    evidence = {"ready": True, "repeatable_failure_slices": ["behavior"], "missing_fields": [], "failed_checks": [], "uncovered_failure_slices": []}
    parameter = {"parameter_update_required": True, "residual_parameter_slices": ["behavior"]}
    pretraining = select_next_training_stage(evidence, parameter, {"parameter_gap": "representation", "domain_corpus_version": "corpus-v1", "evaluation_manifest": "eval-v1.json", "training_budget_gpu_hours": 8})
    assert pretraining["decision"] == "continued_pretraining"
    sft = select_next_training_stage(evidence, parameter, {"demonstration_dataset_version": "sft-v1", "evaluation_manifest": "eval-v1.json", "training_budget_gpu_hours": 4})
    assert sft["decision"] == "sft"
    preference = select_next_training_stage(evidence, parameter, {"sft_baseline_ready": True, "sft_baseline_manifest": "sft.json", "feedback_mode": "preference_pairs", "preference_dataset_version": "prefs-v1", "evaluation_manifest": "eval-v1.json"})
    assert preference["decision"] == "offline_preference"
    rlvr = select_next_training_stage(evidence, parameter, {"sft_baseline_ready": True, "sft_baseline_manifest": "sft.json", "feedback_mode": "verifier", "verifier_version": "math-v1", "exploration_required": True, "rollout_budget": 128, "rollback_checkpoint": "checkpoint-100"})
    assert rlvr["decision"] == "rlvr"


def test_training_stage_blockers():
    """阶段前置条件不足时返回具体缺口。"""
    evidence = {"ready": True, "repeatable_failure_slices": ["behavior"], "missing_fields": [], "failed_checks": [], "uncovered_failure_slices": []}
    parameter = {"parameter_update_required": True, "residual_parameter_slices": ["behavior"]}
    result = select_next_training_stage(evidence, parameter, {"demonstration_dataset_version": "sft-v1"})
    assert result == {"decision": "blocked", "reason": "stage_requirements_not_ready", "missing": ["evaluation_manifest", "training_budget_gpu_hours"]}
    pretraining = select_next_training_stage(evidence, parameter, {"parameter_gap": "representation", "evaluation_manifest": "eval-v1.json", "training_budget_gpu_hours": 8})
    assert pretraining == {"decision": "blocked", "reason": "stage_requirements_not_ready", "missing": ["domain_corpus_version"]}


def test_readiness_boundaries():
    """回归：遗漏评测、非法计数、指标方向、非有限值与无效预算。"""
    from unittest import TestCase

    check = TestCase()
    evidence = {
        "goal_metric": "accuracy", "target_threshold": 0.9,
        "minimum_repeats": 3, "minimum_failure_rate": 0.6,
        "failure_runs": {"behavior": {"attempts": 3, "failures": 2}},
        "evaluation_ids_isolated": True, "baseline_slices": ["behavior"],
    }
    for field in evidence:
        if field in ("evaluation_ids_isolated", "baseline_slices"):
            continue
        report = assess_problem_evidence({**evidence, field: None})
        assert not report["ready"] and field in report["missing_fields"]
    zero_runs = assess_problem_evidence({**evidence, "failure_runs": {"behavior": {"attempts": 0, "failures": 0}}})
    assert not zero_runs["ready"] and "repeatable_failure_slices" in zero_runs["failed_checks"]
    for changes in (
        {"minimum_repeats": 0}, {"minimum_repeats": 1.5},
        {"minimum_failure_rate": float("nan")}, {"minimum_failure_rate": 1.1},
        {"target_threshold": float("inf")},
        {"failure_runs": {"behavior": {"attempts": 3, "failures": 4}}},
    ):
        with check.assertRaises(ValueError):
            assess_problem_evidence({**evidence, **changes})

    row = {"failure_slice": "format", "metric_value": 0.95, "introduced_failures": []}
    assert not assess_parameter_update_need(["format"], [{"failure_slice": "format", "metric_value": 0.95}], 0.9)["parameter_update_required"]
    for results in ([], [row]):
        with check.assertRaisesRegex(ValueError, "behavior"):
            assess_parameter_update_need(["format", "behavior"], results, 0.9)
    for value in (float("nan"), float("inf")):
        with check.assertRaises(ValueError):
            assess_parameter_update_need(["format"], [{**row, "metric_value": value}], 0.9)
    with check.assertRaises(ValueError):
        assess_parameter_update_need(["format"], [{**row, "introduced_failures": None}], 0.9)
    for value, required in ((0.05, False), (0.1, False), (0.5, True)):
        report = assess_parameter_update_need(["format"], [{**row, "metric_value": value}], 0.1, higher_is_better=False)
        assert report["parameter_update_required"] is required

    evidence_report = assess_problem_evidence(evidence)
    parameter = {"parameter_update_required": True}
    context = {"demonstration_dataset_version": "sft-v1", "evaluation_manifest": "eval-v1.json"}
    for budget in (0, -1, float("nan"), float("inf"), True, "4"):
        result = select_next_training_stage(evidence_report, parameter, {**context, "training_budget_gpu_hours": budget})
        assert result["decision"] == "blocked" and result["missing"] == ["training_budget_gpu_hours"]
    rl_context = {
        "sft_baseline_ready": True, "sft_baseline_manifest": "sft.json",
        "feedback_mode": "learned_reward", "reward_model_version": "reward-v1",
        "exploration_required": True, "rollout_budget": 128, "rollback_checkpoint": "checkpoint-100",
    }
    assert select_next_training_stage(evidence_report, parameter, rl_context)["decision"] == "online_rl"
    for changes, missing in (({"rollout_budget": -1}, "rollout_budget"), ({"exploration_required": "yes"}, "exploration_required")):
        result = select_next_training_stage(evidence_report, parameter, {**rl_context, **changes})
        assert result["decision"] == "blocked" and result["missing"] == [missing]
    assert select_next_training_stage(evidence_report, parameter, {"sft_baseline_ready": True})["decision"] == "stop_at_sft"
    with check.assertRaises(ValueError):
        select_next_training_stage(evidence_report, parameter, {**rl_context, "feedback_mode": "typo"})


def run_demo():
    """用同一组复测证据，展示无需训练、进入 SFT 和缺少预算三种结果。"""
    from json import dumps

    evidence = {
        "goal_metric": "accuracy",
        "target_threshold": 0.9,
        "minimum_repeats": 3,
        "minimum_failure_rate": 0.6,
        "failure_runs": {
            "format": {"attempts": 3, "failures": 2},
            "behavior": {"attempts": 4, "failures": 3},
        },
        "evaluation_ids_isolated": True,
        "baseline_slices": ["format", "behavior"],
    }
    evidence_report = assess_problem_evidence(evidence)
    context = {
        "parameter_gap": "behavior",
        "demonstration_dataset_version": "demo-sft-v1",
        "evaluation_manifest": "demo-eval-v1.json",
        "training_budget_gpu_hours": 4,
    }
    scenarios = [
        ("非参数方案达标，无需更新参数", 0.93, 4),
        ("行为缺口仍在，SFT 条件齐备", 0.82, 4),
        ("行为缺口仍在，训练预算为零", 0.82, 0),
    ]
    print("\n测试跑通：")
    for label, behavior_score, budget in scenarios:
        candidate_results = [
            {"failure_slice": "format", "metric_value": 0.95, "introduced_failures": []},
            {"failure_slice": "behavior", "metric_value": behavior_score, "introduced_failures": []},
        ]
        parameter_report = assess_parameter_update_need(
            evidence_report["repeatable_failure_slices"],
            candidate_results,
            evidence["target_threshold"],
        )
        decision = select_next_training_stage(evidence_report, parameter_report, {**context, "training_budget_gpu_hours": budget})
        print(f"\n{label}")
        print(dumps({"parameter_report": parameter_report, "decision": decision}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    test_problem_evidence_gate()
    test_parameter_update_gate()
    test_training_stage_branches()
    test_training_stage_blockers()
    test_readiness_boundaries()
    print("微调准入与最小干预自检全部通过。")
    run_demo()
