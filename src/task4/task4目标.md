### Task 4 · 奖励构造与在线策略候选（截止时间1024周六中午12：00）

### 1. 主要问题

当前策略生成的回答由人类偏好、奖励模型还是规则验证器评分；评分怎样经过校准、基线和优势估计形成受约束的 PPO 或 GRPO 更新，并产出可独立复测的候选策略？

### 2. 推荐学习顺序

人类偏好或规则反馈 → 奖励训练与留出校准 → 在线采样 → 回报、价值或组内基线 → 优势 → 受约束更新 → 候选策略与新轨迹

### 3. 学习内容

**3.1 最小学习**  
[Part 02 · 16 PPO](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/16_RLHF_PPO_Memory.ipynb)  
[Part 02 · PT-REWARD-MODEL 奖励模型训练、校准与过度优化](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/PT-REWARD-MODEL_Reward_Model_Training_and_Calibration.ipynb)  
[06 奖励信号、PPO 与 RLHF](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/06_rlhf_and_ppo_system_cost.md)

**3.2 扩展学习**  
[Part 02 · PT-REWARD-SIGNAL 奖励、价值与优势](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/PT-REWARD-SIGNAL_Reward_Model_Value_and_Advantage.ipynb)  
[07 GRPO、RLVR 与组内奖励](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/07_grpo_and_groupwise_alignment.md)  
[Part 02 · 18 GRPO](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/18_GRPO_Loss_Tutorial.ipynb)  
[Part 02 · 85 GRPO / RLVR 候选](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/85_GRPO_Groupwise_Alignment_Project.ipynb)

### 4. 打卡任务 (优先保住最小打卡）

**4.1 最小打卡(对应06 奖励信号、PPO 与 RLHF, ,Part 02 · 16 PPO, Part 02 · PT-REWARD-MODEL 奖励模型训练、校准与过度优化,）**  
（1）某团队在强化学习中持续奖励更长的思考过程，结果模型的思维链变长了，数学题正确率却下降了。为什么奖励更长的思维链，反而可能让模型推理效果变差？请分析原因，并提出改进方案。  
（2）PPO 为什么要在一轮更新期间固定旧策略？如果同一批回答被反复用于更新，当前策略逐渐偏离旧策略，会发生什么？PPO 的裁剪机制又有哪些局限？

**4.2 学有余力增项1（对应Part 02 · PT-REWARD-SIGNAL 奖励、价值与优势, 07 GRPO、RLVR 与组内奖励）**  
（1）A 的奖励分数为 0.8，预期回报为 0.7；B 的奖励分数为 0.6，预期回报为 0.3，哪个优势更高，为什么？  
（2）数学问答中，奖励模型认为回答很好，但规则验证器判定答案错误。你会怎样设计奖励机制，避免模型只迎合其中一种评分？

**4.3 学有余力增项2(对应Part 02 · 18 GRPO，Part 02 · 85 GRPO / RLVR 候选)**  
（1）GRPO 使用规则验证器给数学答案打分：正确得 1 分，错误得 0 分。同一道题生成的四个答案全部正确、全部错误或对错各半，哪种情况能提供更有效的组内优势信号？为什么？

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

![](C:/Users/sshix/AppData/Roaming/marktext/images/36c3a00750da0e291225ad58ff57625b97b7c14c.png)
