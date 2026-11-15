### Task 2 · 更新范围与参数高效适配（截止时间1018周日中午12：00）

### 1. 主要问题

监督目标与输入工作负载固定后，哪些参数需要更新，怎样在全参数、LoRA、QLoRA 和 LoRA 变体之间选择？

### 2. 推荐学习顺序

全参数 / 适配器选择 → 目标模块、秩与缩放 → 固定秩或固定参数预算比较 → 基座显存不足时进入 QLoRA → 可恢复适配器产物

### 3. 学习内容

**3.1 最小学习**  
[02 LoRA / PEFT](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/topic_discussion/post_training_optimization/02_lora_peft_design.md)  
[Part 02 · 14 LoRA](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/14_LoRA_Tutorial.ipynb)

**3.2 扩展学习**  
[Part 02 · 31 LoRA 变体](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/31_LoRA_Variants_Theory.ipynb)；  
[Part 02 · 26 QLoRA](https://github.com/datawhalechina/llm-algo-leetcode/blob/main/02_PyTorch_Algorithms/26_QLoRA_and_4bit_Quantization.ipynb)

### 4. 打卡任务 (优先保住最小打卡）

**4.1 最小打卡(对应02 LoRA / PEFT,Part 02 · 14 LoRA）**

1. 全参微调、LoRA、QLoRA 的主要收益与代价分别是什么？要对它们做公平比较，至少应固定哪些条件？候选通过验证后，交付形态又该依据哪些因素决定？
2. 设计适配器的推荐顺序是什么？QLoRA 和 LoRA 变体分别改变什么？为什么它们不是必须依次经过的两个阶段？需要低比特训练时，应记录哪些配置，避免把哪些影响混为一谈？
3. 选择 LoRA 挂载范围的实质是什么？在低秩旁路中，矩阵 A、矩阵 B、秩 r、缩放系数 α、随机失活分别起什么作用？为什么训练开始时让 B 为零可以保持基座初始行为？

**4.2 学有余力增项1（对应Part 02 · 31 LoRA 变体）**  
LoRA、rsLoRA、DoRA的区别主要是什么 ？为什么比较这些变体时，既要固定 rank，也要在同一参数上限内反推 rank？

**4.3 学有余力增项2(对应Part 02 · 26 QLoRA)**  
QLoRA 一次前向中主要涉及哪些对象？底座权重W、NF4 码点与缩放因子、LoRA 旁路 A/B、LoRA 优化器状态分别以什么方式存储或计算？哪些对象会更新？

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
