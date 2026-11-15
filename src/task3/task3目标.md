### Task 3 · 目标诊断与阶段准入（截止时间1021周三中午12：00）

### 1. 主要问题

已有同提示的优选与非优选回答时，怎样固定参考策略、形成偏好边际并完成离线 DPO 更新？

### 2. 推荐学习顺序

同提示偏好对 → 固定参考策略 → 偏好边际 → 离线更新与独立复测 → 候选清单

### 3. 学习内容

**3.1 最小学习**  
[05 DPO 与离线偏好优化](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/05_dpo_and_preference_optimization.md)  
[Part 02 · 50 偏好数据与评测](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/50_Preference_Data_and_Evaluation.ipynb)  
[Part 02 · 17 DPO](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/17_DPO_Loss_Tutorial.ipynb)；

**3.2 扩展学习**

[Part 02 · 84 离线 DPO](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/84_DPO_Preference_Project.ipynb)

### 4. 打卡任务 (优先保住最小打卡）

**4.1 最小打卡(对应05 DPO 与离线偏好优化,Part 02 · 50 偏好数据与评测,Part 02 · 17 DPO）**  
（1）**DPO 的基本原理与数据要求。** 什么是偏好数据？为什么优选回答和非优选回答必须对应同一个问题？DPO 如何利用这类数据更新模型？请结合 DPO 损失函数，说明参考模型、偏好差值和 `beta` 分别起什么作用，并解释为什么训练 Loss 下降不代表模型实际表现一定提升。  
（2）**如何判断偏好优化是否有效？** 假设模型经过 DPO 训练后，训练 Loss 明显下降，但实际使用时并没有变好，甚至部分回答质量下降。你会从哪些方面排查问题？请结合偏好数据质量、训练集与评测集隔离、偏好准确率、评审一致性和安全性，说明如何判断模型是否值得保留。

**4.2 学有余力增项1（对应Part 02 · 84 离线 DPO）**  
（1）**如何设计一套完整、可复现的离线 DPO 实验？** 请从 SFT 基线、偏好数据、固定参考模型、训练配置和独立评测等方面说明实验流程，并解释如何比较训练前后的模型效果。当模型整体指标提升、部分样本却明显退化时，应如何决定接受、继续调整或拒绝该候选模型？

**4.3 学有余力增项2（对应 Part 02 · 17 DPO、Part 02 · 84 离线 DPO）**  
（1）**如何选择 DPO 的 `beta` 参数？** 假设不同 `beta` 设置下，模型的训练 Loss 持续下降，但偏好准确率、平均偏好边际和最差偏好边际的变化并不一致。请分析这些指标分别反映什么，说明为什么不能只依据 Loss 或平均指标选择模型，并讨论如何在偏好改善、模型稳定性和原有能力保持之间做出权衡。

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
