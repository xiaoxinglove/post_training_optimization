微信群昵称:阿星  
环境：GPU  
系统：Windows  
AI 占比 vs 人工占比：70：30
任务项编号4.1  
当前卡点：无

### Task 3 · 目标诊断与阶段准入

## 4.1 最小打卡(**对应05 DPO 与离线偏好优化,Part 02 · 50 偏好数据与评测,Part 02 · 17 DPO**）

(1)DPO 的基本原理与数据要求。 什么是偏好数据？为什么优选回答和非优选回答必须对应同一个问题？DPO 如何利用这类数据更新模型？请结合 DPO 损失函数，说明参考模型、偏好差值和 `beta` 分别起什么作用，并解释为什么训练 Loss 下降不代表模型实际表现一定提升。 
偏好数据，就是把同一道题的两个回答放在一起，并标出哪个更好。

两个回答必须对应同一个完整输入，这样模型才能学到在同样条件下应该偏向哪种回答，否则很难直接判断谁更好，因为它们面对的要求不同。需要共享相同的问题、系统指令、对话历史和其他约束。

参考模型提供固定基准，偏好差值反映相对基准的变化，贝塔参数调节训练中的尺度和约束。参考模型通常是一份冻结的监督微调模型，可以理解为保留训练前的水平作为对照。偏好差值关注的是，当前模型相比这个基准，是否更偏向优选回答。贝塔参数会影响损失和梯度；在理论目标中，奖励尺度相同时，它越大，偏离参考模型的代价越高。因此，不能简单认为贝塔参数越大，模型更新就越激进。

训练损失下降，模型可能记住训练样本，也可能学到错误标签，或者形成回答越长越容易获选的偏差。还有一种容易忽略的情况：两个回答的生成概率都下降了，只要非优选回答下降得更快，损失仍然可能降低。所以，验收时需要让模型回答没见过的问题，检查回答是否正确、是否遵循要求，以及在控制长度和评审偏差后，是否确实更受认可。

(2)**如何判断偏好优化是否有效？** 假设模型经过 DPO 训练后，训练 Loss 明显下降，但实际使用时并没有变好，甚至部分回答质量下降。你会从哪些方面排查问题？请结合偏好数据质量、训练集与评测集隔离、偏好准确率、评审一致性和安全性，说明如何判断模型是否值得保留。
判断偏好优化是否有效，看模型在独立评测中是否真正变好，而不是训练 Loss 是否下降。训练 Loss 下降只说明训练目标得到改善；实际回答在正确性、任务完成度和指令遵循等方面获得稳定提升，才是优化有效的证据。

排查问题时，应结合部分回答质量下降样本比较不同训练阶段，定位问题从何时、在哪类任务上出现。首先检查实现与配置是否正确，包括优选和非优选回答是否接反、损失计算与截断是否正确、参考模型是否固定，以及推理时是否加载了正确的权重和聊天模板。其次检查学习率、训练轮数和 beta 是否合适，是否出现过度优化、能力遗忘或模型偏移过大。还要分析目标与生成质量为何脱节：DPO 优化的是相对偏好差距，即使优选回答的生成概率下降，只要非优选下降更多，Loss 仍可能降低。

实际收益可信、关键能力与安全达标时，可以接受；收益不明确或存在可修复的局部回答质量下降时，继续调整；出现不可接受的关键能力或错误回答时，拒绝替换或回滚。偏好数据质量决定训练方向是否可靠；训练集与评测集隔离保证结果能够反映泛化；独立集上的偏好准确率用于检查排序能力，并与实际生成质量交叉验证；评审一致性用于检查评价是否稳定，同时排除共同偏差；安全性用于确认有害输出和过度拒答是否恶化。

**4.2 学有余力增项1（对应Part 02 · 84 离线 DPO）**  
（1）**如何设计一套完整、可复现的离线 DPO 实验？** 请从 SFT 基线、偏好数据、固定参考模型、训练配置和独立评测等方面说明实验流程，并解释如何比较训练前后的模型效果。当模型整体指标提升、部分样本却明显退化时，应如何决定接受、继续调整或拒绝该候选模型？
完整的离线 DPO 实验：先评测并冻结 SFT 模型，用它初始化策略模型，同时作为固定参考模型；偏好数据应来自同一问题下的优劣回答，经过质量审核、去重，并隔离训练集、验证集和测试集。训练时保存数据、模型、代码环境和完整配置，记录随机种子、学习率、beta、批量及训练步数，用验证集调参和选择检查点。

比较训练前后效果时，让基线和候选模型在独立测试集上使用相同推理设置生成回答，综合考察客观正确率、盲评胜率、评审一致性、安全性和各类任务表现，并通过重复实验检查收益是否稳定。训练 Loss 下降、偏好准确率提高只能作为辅助证据，实际生成质量才是最终依据。

整体提升但局部退化时，应根据退化的严重程度、发生频率和场景重要性判断：收益稳定、关键能力和安全指标达标，局部退化在预设容忍范围内，可以接受；重要场景退化或收益证据不足，应继续调整；出现严重安全问题或关键能力明显受损，应拒绝。若利用测试失败样本继续优化，下一轮验收必须使用新的独立测试数据。

参考链接：

- 打卡 Issue：[llm-algo-leetcode 后训练优化 | 202610 Task 3 · 偏好数据与离线策略优化 · Issue #220 · datawhalechina/llm-algo-leetcode](https://github.com/datawhalechina/llm-algo-leetcode/issues/220)
- DataWhale 社区：[https://www.datawhale.cn/](https://www.datawhale.cn/)





微信群昵称：郭才高  
环境：本地  
系统：windows  
AI 占比 vs 人工占比：50:50

**4.1 最小打卡(对应05 DPO 与离线偏好优化,Part 02 · 50 偏好数据与评测,Part 02 · 17 DPO）**  
**（1）DPO 的基本原理与数据要求。 什么是偏好数据？为什么优选回答和非优选回答必须对应同一个问题？DPO 如何利用这类数据更新模型？请结合 DPO 损失函数，说明参考模型、偏好差值和 beta 分别起什么作用，并解释为什么训练 Loss 下降不代表模型实际表现一定提升。**  
**什么是偏好数据？**  
偏好数据不是普通的“问题—标准答案”监督数据，而是一组比较信号：对同一个问题或同一个任务输入，给出两个候选回答，并标注哪一个更好。通常记为：  
x：同一个提示/问题/任务输入；  
yw：优选回答，即被标注为更好的回答；  
yℓ：非优选回答，即被标注为较差的回答。  
所以一条偏好对的核心不是“A 是绝对正确的”，而是“在同一个问题下，A 比 B 更好”。

**为什么优选回答和非优选回答必须对应同一个问题？**  
因为偏好比较要成立，必须满足“比较对象契约”：两个回答要来自同一任务、同一输入和同一约束。否则，你比较的可能是“题目差异”而不是“回答质量差异”。比如两个回答面对的问题措辞不同、约束不同、长度要求不同，那么标注者选 A 可能只是因为 A 对应的题目更容易，而不是 A 的回答更好。这样训练出来的信号就是噪声，模型会学到错误偏好。文档中把这一点列为偏好数据有效性的第一层契约：比较对象必须一致。

**DPO 如何利用这类数据更新模型？**  
DPO 不显式训练奖励模型，也不在线跑强化学习，而是直接用偏好对优化策略。它以一个冻结的参考模型πref为锚点，通常是 SFT 后的模型。DPO 损失函数可写为：

[![Image](https://private-user-images.githubusercontent.com/4394216/681220946-656842a8-d3be-463d-b75f-919d9b8510bd.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI4MDc0NTIsIm5iZiI6MTc5MjgwNzE1MiwicGF0aCI6Ii80Mzk0MjE2LzY4MTIyMDk0Ni02NTY4NDJhOC1kM2JlLTQ2M2QtYjc1Zi05MTlkOWI4NTEwYmQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MTAyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjEwMjRUMDE1OTEyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MjVlNjJjOTcyNTBmZjIwM2RlZjUyOWFhNDQ0YWVlMmQwYjMxNDdmODY4ZDA1ODMyODY3NjdmNTRlNmQ0Yzc4MyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.Wki4SBja_JKp7hAiR682_7gGxfSMnIgD0Yo3FygaV_A)](https://private-user-images.githubusercontent.com/4394216/681220946-656842a8-d3be-463d-b75f-919d9b8510bd.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI4MDc0NTIsIm5iZiI6MTc5MjgwNzE1MiwicGF0aCI6Ii80Mzk0MjE2LzY4MTIyMDk0Ni02NTY4NDJhOC1kM2JlLTQ2M2QtYjc1Zi05MTlkOWI4NTEwYmQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MTAyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjEwMjRUMDE1OTEyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MjVlNjJjOTcyNTBmZjIwM2RlZjUyOWFhNDQ0YWVlMmQwYjMxNDdmODY4ZDA1ODMyODY3NjdmNTRlNmQ0Yzc4MyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.Wki4SBja_JKp7hAiR682_7gGxfSMnIgD0Yo3FygaV_A) 其中： πθ：当前正在训练的策略模型； πref：冻结的参考模型，通常是 SFT 基线； yw：优选回答； yℓ：非优选回答； β：控制“拉开偏好差距”的力度，也控制模型偏离参考模型的程度。

DPO 的直观目标是：让优选回答相对于参考模型的概率提升，比非优选回答相对于参考模型的概率提升更多。换句话说，它不是简单要求“好回答绝对概率高”，而是要求“好回答相对于原来的 SFT 人格，要比坏回答相对涨得更多”。

**参考模型、偏好差值和 beta 分别起什么作用？**  
参考模型 πref ：冻结的 SFT 基线，起“锚点”和“正则”作用。它防止模型为了讨好偏好数据而彻底抛弃原有可用行为。DPO 比较的是当前策略相对于参考策略的对数概率变化，而不是绝对概率。

偏好差值：核心是  
[![Image](https://private-user-images.githubusercontent.com/4394216/681225285-fcbdfbe1-ff90-4486-9e81-00d997868a5d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI4MDc0NTIsIm5iZiI6MTc5MjgwNzE1MiwicGF0aCI6Ii80Mzk0MjE2LzY4MTIyNTI4NS1mY2JkZmJlMS1mZjkwLTQ0ODYtOWU4MS0wMGQ5OTc4NjhhNWQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MTAyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjEwMjRUMDE1OTEyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MjBmZWZiZjViZWZiYmI0MGIwOTBkNzJlNTM4MTgzMTdkYzVlNzYwMGNjZmZmNDQwMDg5ODkyMjEyN2E1NmMxNyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.fSTQXgZjcdL_jB3BfV-hMDNz1Ogpqd4IdIZW9jmWa98)](https://private-user-images.githubusercontent.com/4394216/681225285-fcbdfbe1-ff90-4486-9e81-00d997868a5d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI4MDc0NTIsIm5iZiI6MTc5MjgwNzE1MiwicGF0aCI6Ii80Mzk0MjE2LzY4MTIyNTI4NS1mY2JkZmJlMS1mZjkwLTQ0ODYtOWU4MS0wMGQ5OTc4NjhhNWQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MTAyNCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjEwMjRUMDE1OTEyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MjBmZWZiZjViZWZiYmI0MGIwOTBkNzJlNTM4MTgzMTdkYzVlNzYwMGNjZmZmNDQwMDg5ODkyMjEyN2E1NmMxNyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.fSTQXgZjcdL_jB3BfV-hMDNz1Ogpqd4IdIZW9jmWa98)  
它表示“优选回答相对参考模型的提升”减去“非优选回答相对参考模型的提升”。这个差值越大，说明模型越偏向优选回答。DPO 希望这个差值经过 β 缩放后，被 sigmoid 判为更接近“优选胜出”。

beta β：像“油门”或“拉力强度”。β 太小，模型不太敢偏离参考模型，偏好学习弱；β 太大，模型可能为了拉大偏好差距而用力过猛，输出变得不自然，甚至偏离原有可用行为。文档特别强调：不能只看训练 loss 来选β，必须在固定数据和预算下做独立评测对照。

**为什么训练 Loss 下降不代表模型实际表现一定提升？**  
因为 DPO 的训练 loss 只衡量模型在训练偏好对上拟合得怎么样，不衡量模型在真实使用中的帮助性、安全性、稳定性。Loss 下降可能来自：  
模型记住了训练偏好对，而不是学会了可泛化的偏好；  
偏好数据本身有噪声，模型在拟合错误信号；  
训练集和评测集没有隔离，评测被记忆效应污染；  
β 或步数过大，模型偏离 SFT 基线，输出变得不自然；  
评审器本身有偏差，训练信号和真实目标不一致。  
所以文档反复强调：训练 loss 下降、奖励上升，都不能直接说明模型更有帮助、更安全或更可靠。必须回到独立、隔离的评测集上比较。

**（2）如何判断偏好优化是否有效？ 假设模型经过 DPO 训练后，训练 Loss 明显下降，但实际使用时并没有变好，甚至部分回答质量下降。你会从哪些方面排查问题？请结合偏好数据质量、训练集与评测集隔离、偏好准确率、评审一致性和安全性，说明如何判断模型是否值得保留。**  
**如何判断偏好优化是否有效？**  
假设 DPO 训练后训练 Loss 明显下降，但实际使用没有变好，甚至部分回答质量下降，应从以下方面排查。  
第一，查偏好数据质量。  
文档给出四个契约层次：  
比较对象：两个回答是否来自同一任务、同一输入、同一约束。如果问题不同、约束不同，比较结果反映的是题目差异，不是回答质量。  
偏好语义：标注者选择 A 的理由，是否和目标能力一致。比如你想要“更准确”，但标注者因为“更长”选了 A，这就是偏好语义错位。  
来源身份：生成来源、标注规范、判分依据是否可追溯。争议样本能否复核。  
切分隔离：训练集和评测集在规范化后是否无重复。如果有重复，模型可能只是背答案，而不是能力提升。  
如果数据本身配对错误、标注噪声大、理由和目标不一致，优化器不能掩盖信号问题，应先回到数据工程。

第二，查训练集与评测集隔离。  
如果评测集和训练集有重复或近似重复，Loss 下降可能只是记忆效应。必须使用未参与更新的偏好对做独立评测，并且固定评测工作负载：相同模型起点、分词器、评测对、最大长度和评分方法。训练阶段只允许策略参数变化。

第三，看偏好准确率和非平局胜率。  
不能只看训练 loss。要在独立评测对上比较更新前后的偏好表现，看优选回答是否更常胜出。还要看有效样本量、评测覆盖率、明确判决数和非平局胜率。如果大量样本是平局或评审器无法明确判决，偏好准确率本身不可靠。

第四，查评审一致性。  
自动评审器不是永远公正的裁判。要检查：  
同一评审器重复判断是否一致；  
交换两个回答的顺序后，判断是否翻转；  
是否偏爱更长、更格式漂亮的回答。  
如果评审器不稳定，训练信号和评测结果都可能失真。

第五，看安全硬指标和原有能力保持。  
偏好准确率提升不等于安全。必须同时看安全硬指标是否退化。如果模型输出明显偏离原有可用行为，说明更新幅度过大，需要检查  
β、步数、数据覆盖和参考模型。

如何判断模型是否值得保留？  
文档的标准不是“训练 loss 最低”，而是：在隔离的、经过质检的评测集上，非平局胜率有真实提升；安全硬指标不退化；有效样本量、覆盖率和明确判决数足够；评审器重复判断和顺序交换稳定；最差偏好边际没有明显恶化；人工抽查没有发现明显退化。如果训练 loss 下降但独立评测无提升，或安全/关键能力退化，就不应仅凭 loss 保留该模型。

**4.2 学有余力增项1（对应Part 02 · 84 离线 DPO）**  
**（1）如何设计一套完整、可复现的离线 DPO 实验？ 请从 SFT 基线、偏好数据、固定参考模型、训练配置和独立评测等方面说明实验流程，并解释如何比较训练前后的模型效果。当模型整体指标提升、部分样本却明显退化时，应如何决定接受、继续调整或拒绝该候选模型？**  
一个可交付、可审计的离线 DPO 实验应按以下流程设计：  
第一步：准备并冻结 SFT 基线。  
项目起点是一个已交付的 SFT 基线。训练分支复制基线得到可更新策略；同时冻结一份参考模型 πref。参考模型不参与更新，作为 DPO 的锚点。评测分支保留未参与更新的偏好对。

第二步：输入准入与偏好数据检查。  
对偏好数据做准入检查：比较对象是否同一任务/输入/约束；偏好语义是否与目标能力一致；来源身份是否可追溯；训练集与评测集规范化后是否无重复。数据不合格，不进入训练。

第三步：候选训练并完整记录配置。  
训练阶段只允许策略参数变化。参考模型、数据版本、β、步数、随机种子等全部写入运行记录。这样结果才能归因于候选模型本身，而不是评测条件变化。

第四步：固定评测工作负载，做独立复测。  
更新前后的策略必须使用相同的模型起点、分词器、评测对、最大长度和评分方法。评测对不参与训练，且与训练集隔离。用配对比较更新前后的偏好表现，而不是直接采用训练损失最低的检查点。

第五步：产物交付。  
最终交付适配器、模型血缘和评测结果，包括偏好准确率、边际变化、安全硬指标、有效样本量、覆盖率和明确判决数等。

如何比较训练前后的模型效果？  
不是看训练 loss 曲线，而是用同一套独立评测对做配对比较：同一模型起点、同一分词器、同一评测对、同一最大长度和评分方法。看更新前后在偏好准确率、非平局胜率、平均偏好边际、最差偏好边际和安全硬指标上的变化。训练阶段只允许策略参数变化，参考模型、数据版本、β、步数和种子都要记录，保证可复现。

当模型整体指标提升、部分样本却明显退化时，如何决定接受、继续调整或拒绝？  
应同时看整体收益和尾部退化：  
如果安全硬指标退化，或关键能力明显下降，应拒绝该候选模型；  
如果整体偏好准确率提升，但最差偏好边际显著恶化，说明提升可能以尾部样本为代价，不能只看平均指标，应继续调整；  
如果退化局限在少量可解释样本，且整体收益显著、安全不退化，可以继续调整数据覆盖、β、步数或早停策略，再复测；  
如果调整后仍以牺牲安全或原有能力为代价，应拒绝并回滚到 SFT 基线。

核心原则是：不能只依据平均指标或训练 loss 接受模型，必须看安全硬指标、最差边际和独立评测。

4.3 学有余力增项2（对应 Part 02 · 17 DPO、Part 02 · 84 离线 DPO）  
（1）如何选择 DPO 的 beta 参数？ 假设不同 beta 设置下，模型的训练 Loss 持续下降，但偏好准确率、平均偏好边际和最差偏好边际的变化并不一致。请分析这些指标分别反映什么，说明为什么不能只依据 Loss 或平均指标选择模型，并讨论如何在偏好改善、模型稳定性和原有能力保持之间做出权衡。  
如何选择 DPO 的 beta 参数？  
假设不同β下训练 Loss 持续下降，但偏好准确率、平均偏好边际和最差偏好边际变化不一致，需要先理解这些指标分别反映什么。  
训练 Loss：只反映模型在训练偏好对上的拟合程度。Loss 下降可能是记住了训练对，不一定代表独立评测提升。  
偏好准确率：在独立评测对中，优选回答胜出的比例。它反映模型在隔离评测上的偏好判断是否变好，比训练 loss 更接近实际效果。  
平均偏好边际：所有评测对上的平均偏好差距或平均置信度。它反映“平均而言模型有多偏向优选回答”，但平均指标会掩盖尾部问题。  
最差偏好边际：尾部最差样本上的偏好边际。它反映模型稳定性和局部退化风险。平均边际提升但最差边际恶化，说明模型可能牺牲了部分难样本或边缘样本来换取平均收益。

为什么不能只依据 Loss 或平均指标选择模型？  
训练 Loss 只衡量训练目标拟合，不衡量独立泛化、安全性和原有能力。平均偏好边际会把少数严重退化样本“平均掉”。偏好优化是否成功，要看隔离评测上的非平局胜率、安全硬指标、有效样本量、覆盖率和明确判决数，而不是只看 loss 或平均值。

如何在偏好改善、模型稳定性和原有能力保持之间权衡？  
β 太小，模型不太敢偏离参考模型，偏好改善弱但稳定；  
β 太大，模型可能为了拉大偏好差距而偏离 SFT 基线，输出不自然，尾部样本更容易退化。选择时应：  
1.固定数据、预算、随机种子，做β 网格对照；  
2.用独立、隔离的评测对比较偏好准确率和非平局胜率；  
3.同时看安全硬指标和最差偏好边际，不能只看平均；  
4.检查有效样本量、覆盖率和明确判决数，避免评测本身不可靠；  
5.结合人工抽查原有能力是否保持；  
6.如果平均指标提升但最差边际或安全指标恶化，应降低 β、调整数据覆盖或步数，必要时早停或回滚参考。

最终选择的标准不是“训练 Loss 最低”或“平均偏好边际最高”，而是在偏好准确率有真实提升、安全硬指标不退化、最差偏好边际可接受、原有能力保持之间取得平衡的 β。
