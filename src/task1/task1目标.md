### Task 1 · 监督目标与最小 SFT 基线（截止时间1015周四中午12：00）

### 1. 主要问题

样本怎样经过切分、模板和标签掩码变成有效监督 Token，并完成一次可复查的 SFT 基线？

### 2. 推荐学习顺序

来源、切分与去污染 → 模板、分词与标签边界 → 有效监督词元与损失 → 有效更新 → 冻结验证 → 可复查基线

### 3. 学习内容

**3.1 最小学习**

[Part 02 · 32 SFT 数据准入与长度审计](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/32_Data_Engineering_for_SFT.ipynb)  
[Part 02 · 13 SFT 训练循环](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/13_SFT_Training_Loop.ipynb)  
[Part 02 · 15 端到端微调](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/15_End_to_End_Fine_Tuning_Experiment.ipynb)  
**3.2 扩展学习**  
[Part 02 · 30 长上下文微调](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/30_Long_Context_Fine_Tuning.ipynb)  
[01 SFT 数据与监督契约](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/01_sft_data_and_loss.md)  
[04 SFT 基线与交付](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/04_end_to_end_experiment.md)  
[Part 02 · 11–12 训练控制](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/2_3.md)

### 4. 打卡任务 (优先保住最小打卡）

**4.1 最小打卡(对应Part 02 · 32 SFT 数据准入与长度审计,Part 02 · 13 SFT 训练循环）**  
1.为什么在检查训练—评测泄漏（Split Leakage）时，只比较“任务输入指纹”而不把目标回答（response）纳入比较范围？如果把回答也包含进去，会产生什么漏洞？  
2.为什么数据审计要求“汇总独立拒绝原因”而不是“发现第一项风险就立即停止”？多重风险同时存在时，对后续的模板、标签及序列拼接处理有什么影响？  
3.语言模型预训练（Pre-training）与监督微调（SFT）都使用 Next-Token Prediction 和交叉熵损失，但两者的监督范围和优化侧重点有着本质不同。说明为什么在 SFT 中不能让模型对整个序列（包括 prompt）都计算损失？如果不加限制会带来什么隐患？  
4.在计算一个 Batch 的 SFT 损失时，为什么正确的做法是“先累加全部有效监督位置的损失，再除以整个 Batch 的有效监督 Token 总数”？如果直接对 Batch 内各个样本的平均损失求均值（即“按样本数等权平均”），会带来什么问题？

**4.2 学有余力增项1（对应Part 02 · 15 端到端微调, 01 SFT 数据与监督契约， 04 SFT 基线与交付）**  
1.当样本长度超出目标窗口时，系统不会盲目截断，而是通过执行受控截断。请问“最少监督量”和“最大监督损失比例”这两项门槛是如何共同把关的？如果样本的残留监督严重不足却依然强行通过，会对模型的指令遵循能力产生什么负面影响？  
2.为什么在长上下文微调中通常不直接一步到位使用最大窗口，而是采用分阶段扩大长样本比例的“长度课程”？候选模型要进入下一个更长窗口的训练阶段，必须同时满足哪些关键条件（请列举至少三项核心门槛并说明其目的）？  
3.在 SFT 的监督契约中，为什么在构造 labels 时必须将提示词（prompt）、系统消息、填充位置（padding）以及模板 Token 屏蔽（如设为 -100），而只让目标回答（response）和结束标记（EOS）计入损失？如果让整个输入序列都参与损失计算，会给模型带来什么严重的负面影响？

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

相关图片：

![](C:/Users/sshix/AppData/Roaming/marktext/images/13282ec9485f13b192c83099c0b2a055a2e1cf83.png)

![](C:/Users/sshix/AppData/Roaming/marktext/images/fd62c32065f4daad264c39513bbfa88ef84d9518.png)
