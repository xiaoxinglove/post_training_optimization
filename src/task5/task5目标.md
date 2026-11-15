### Task 5 · 轨迹治理与在线训练交付（截止时间1027周二中午12：00）

### 1. 主要问题

在线轨迹怎样绑定策略、奖励和环境版本，经过新鲜度与消费状态检查进入更新；采样、奖励和训练组件又怎样同步权重、保存检查点并从失败中恢复？

### 2. 推荐学习顺序

策略版本 → 轨迹身份与环境状态 → 奖励版本 → 新鲜度与消费准入 → 采样 / 奖励 / 训练拓扑 → 权重同步、检查点、恢复与候选交接

### 3. 学习内容

**3.1 最小学习**  
[Part 02 · PT-ROLLOUT-LIFECYCLE 轨迹与策略新鲜度](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/PT-ROLLOUT-LIFECYCLE_Rollout_and_Policy_Freshness.ipynb)  
[Part 02 · PT-RL-SYSTEM 采样、训练与奖励系统](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/PT-RL-SYSTEM_Rollout_Training_and_Reward_System.ipynb)；  
[08 轨迹生命周期与环境交互](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/08_trajectory_lifecycle_and_environment_interaction.md)  
**3.2 扩展学习**  
[Part 02 · 51 在线 DPO](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/51_Online_DPO.ipynb)；

[09 在线训练交付与执行系统](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/09_rl_execution_system_and_efficiency.md)  
[Part 02 · 85 在线奖励候选](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/85_GRPO_Groupwise_Alignment_Project.ipynb)  
[Part 02 · 86 生命周期与恢复](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/86_DPO_Online_Benchmark.ipynb)

### 4. 打卡任务 (优先保住最小打卡）

**4.1 最小打卡(对应Part 02 · PT-ROLLOUT-LIFECYCLE 轨迹与策略新鲜度,Part 02 · PT-RL-SYSTEM 采样、训练与奖励系统,08 轨迹生命周期与环境交互）**  
（1）一条轨迹需要同时记录哪五类信息？正常生命周期如何迁移，更新中止时应回到哪个状态？为什么“检查可用与写入预留”必须构成一次不可分割的状态迁移？  
（2）为什么不同阶段的原始处理率不能直接比较？如何用阶段倍率把原始处理率换算为等价处理率？流水线容量、队列余量分别如何定义，队列余量为负说明什么？

**4.2 学有余力增项1（对应Part 02 · 51 在线 DPO，09 在线训练交付与执行系统）**  
（1）为什么在线 DPO 不能只看 “反馈有没有进来”，还必须跟踪 policy freshness？policy freshness 应该在哪一个环节被记录或检查？请结合闭环步骤说明。  
（2）为什么在线 DPO 中 “参考模型永远冻结” 可能成为一个问题？如果选择更新参考模型， stability boundary（稳定性边界） 意味着在更新 ref 时必须同时控制什么？

**4.3 学有余力增项2(对应 Part 02 · 85 在线奖励候选，Part 02 · 86 生命周期与恢复）**  
（1）在 GRPO 训练中，对某个 prompt 采样了 4 条回答，验证器返回的奖励分别为 [0, 0, 1, 0]。请回答：  
1.这组轨迹是否构成“有效组”？为什么？  
2.如果项目中把 minimum_valid_group_ratio 设为 0.25，而一批 rollout 中包含 8 个 prompt、每个 prompt 采样 4 条回答，其中只有 1 个 prompt 的奖励组存在组内差异，这批 rollout 是否满足有效组比例门槛？请写出判断依据。  
3.结合 GRPO 的优势估计逻辑，解释“有效组比例”这一门槛为什么在工程上有必要，而不仅仅是一个锦上添花的指标

**打卡选择多选一： (1)4.1 ； (2) 4.1+4.2 ； (3) 4.1+4.2+4.3 **

### 打卡模板

> 微信群昵称:  
> 环境：本地 NVIDIA / 云 GPU / 无 GPU / 国产卡 / Mac / 其他  
> 系统：Linux / WSL2 / Windows / 其他  
> AI 占比 vs 人工占比： 比如70：30、90：10  
> 任务项编号4.x 任务名 + 内容  
> 当前卡点：如有

### === 打卡截图要求 请仔细阅读===

微信群截图具体要求："两步走” 与“三要素”

第一步： github 指定issue链接中，上传测试通过截图，作为打卡；

第二步：然后把自己打卡截图发到群里。 微信群截图包括（1）issue 标题 （2） GitHub ID 和（3） 微信群昵称清晰可见

（如果打卡内容更长，可以在外部写笔记，这里挂链接， 注意 （1）不要直接抄教程内容 ，（2）要带上DataWhale社区和教程地址）

> 相关图片

![](C:\Users\sshix\AppData\Roaming\marktext\images\36c3a00750da0e291225ad58ff57625b97b7c14c.png)
