# 交付与检查

## 分阶段结果

| 阶段 | 必须产出 | 继续工作的依据 |
|---|---|---|
| 确定任务 | project.json、文件索引、研究问题 | 日期、范围、读者和交付清楚 |
| 获取与核对 | 原件、来源/事实/冲突台账 | 关键字段可定位，时间与口径适用 |
| 研究判断 | claims、assumptions、gaps | 机制、模型处理和改变判断条件清楚 |
| 模型 | 可执行代码/公式、输入、结果、manifest | 主结果可重算，三表/现金/权利一致 |
| 主报告 | 正文、精选表图、数字绑定 | 首次读者能理解结论和理由 |
| 最终交付 | 指定格式、复算和页面审阅、索引 | 数字/版本一致，实质限制表述充分 |

用户只要求其中一段时执行该段及其必要依赖；完整报告任务则不能停在“资料收集完成”或“提示词已给出”。目录建立和脚本通过不等于研究完成。

工作目录由初始化脚本建立：`sources/`原件；`evidence/`台账；`model/`模型；`report/`报告；`qa/`检查。历史成果留在原目录，以索引关联。不可为了整洁删除失败、冲突或旧交付。

## 启动命令

以下使用可用的Python3运行时；路径均可替换为目标工作区。

```text
python scripts/init_workspace.py research_run --company "Example Company" --ticker EXAMPLE --valuation-date 2026-09-30 --cutoff 2026-09-30T15:30:00+08:00 --language zh
python scripts/capture_source.py ORIGINAL_PUBLIC_URL --out research_run/sources --expect pdf
python scripts/check_bundle.py research_run --stage data
python scripts/check_bundle.py research_run --stage model
python scripts/check_bundle.py research_run --stage delivery --out research_run/qa/machine_check_01.json
```

初始化拒绝已有目录；采集每次留存新文件，失败会留失败元数据；检查输出拒绝覆盖已有文件。采集成功只标记`captured_not_admitted`，公开时间需研究者从原件/公告索引补核。JSON检查器不运行模型，不下载资料，也不进行语言质量评分。

## 台账格式

除`project.json`和manifest/审阅记录外，台账文件都是JSON数组。使用稳定ID；信息存在底稿一次，报告用引用或输出绑定。

`project.json`：初始化后补齐`audience`、`purpose`、`business_perimeter`、`forecast_horizon`、`materiality_policy`及`methods`。币种/单位/格式按实际任务修改，不能沿用初始化默认值作为未经决定的事实。重要性标准按是否影响结论、变量或预测路径说明，不强制固定百分比。

`evidence/sources.json`中一条已采用来源：

```json
{
  "id": "S01", "title": "Annual report", "publisher": "Issuer",
  "url": "https://issuer.example/annual.pdf",
  "local_path": "sources/annual.pdf", "sha256": "ACTUAL_SHA256",
  "retrieved_at": "2026-10-12T10:00:00+08:00",
  "published_at": null, "published_date": "2026-04-30", "published_date_utc_offset": "+08:00",
  "publication_evidence": "Issuer announcement index dated 2026-04-30",
  "version": "Original disclosed annual report", "admission": "accepted"
}
```

`admission`取`accepted/excluded/unresolved`。`published_at`用带时区ISO时间；只有日期时填`published_date`及原发布当地该日期的`published_date_utc_offset`。检查器用当地日末判断整个可能公开区间是否早于截止；不能直接比较来自不同时区的日期。无法证明区间在截止前时不可自动采用。`publication_evidence`必须有真实依据，哈希位置必须是工作区内相对路径。

`facts.json`记录数值与定义：

```json
{
  "id": "F01", "kind": "fact", "label": "Revenue",
  "value": 100, "unit": "RMB hundred million", "period": "2025",
  "scope": "Consolidated", "locator": "S01 PDF file page 10, row Revenue",
  "source_ids": ["S01"], "raw_value": 10000000000, "raw_unit": "CNY",
  "normalization_rule": "raw_value / 100000000"
}
```

`kind`取`fact/derived/unknown`。推导项另填`calculation`及`depends_on`事实ID；未知项`value:null`且填`gap_id`。关键币种、税与范围信息按字段加到记录中。检查器只检查结构和引用，换算及会计定义仍需复核。

`assumptions.json`：`id,value,unit,rationale,basis_ids,model_fields,alternatives,effect`；`basis_ids`指事实或已采用来源。`alternatives`说明有根据的区间/情景或为何无法确定，不硬填数字。

`claims.json`：`id,judgment,evidence_ids,mechanism,model_treatment,counterevidence,change_condition`。`evidence_ids`可引用事实、假设和来源；`counterevidence`记录反例或最强替代解释。未采用模型时，`model_treatment`说明该论点仅为描述及原因。

`gaps.json`：`id,issue,impact,treatment,affected_claims`；可补充优先级和下一资料渠道。没有缺项时为空数组；不为满足格式编造缺项。

## 模型和报告绑定

`model/manifest.json`：

```json
{
  "command": "python model/run.py", "runtime": "Python version recorded",
  "inputs": [{"path":"project.json","sha256":"ACTUAL_SHA256"}],
  "code": [{"path":"model/run.py","sha256":"ACTUAL_SHA256"}],
  "outputs": [{"path":"model/results.json","sha256":"ACTUAL_SHA256"}]
}
```

此简例需补入所有实际输入，其中至少包括`project.json`、`evidence/facts.json`和`evidence/assumptions.json`；也包括模型配置、调用代码及其他输入。先实际运行模型，再计算对应哈希。检查器校验当前文件与该次记录，不证明运行本身正确。

`report/number_bindings.json`中一条展示数：

```json
{
  "label": "Baseline conditional value", "model_path": "model/results.json",
  "pointer": "/baseline/per_share", "value": 33.39,
  "decimals": 2, "scale": 1, "report_location": "Table 17 baseline row"
}
```

数值只是格式示例。`pointer`为JSON Pointer，数组用数字索引，`scale`负责实际单位转换。按十进制ROUND_HALF_UP核对。全部重要表格和正文数字应登记或采用同等可检查的生成绑定；检查器验证登记数与输出一致，不自动识别DOCX中全部数字。实质审阅要确认登记数确实对应最终报告。

`report/manifest.json`的`deliverables`为`path,sha256`数组；格式满足`project.requested_formats`。

## 审阅记录与交付边界

`qa/review.json`：

```json
{
  "reviews": {
    "sources": {"status":"passed","reviewer":"Reviewer name","reviewer_kind":"ai","scope":"Actual checked source scope","evidence_path":"qa/sources.md"}
  },
  "reviewed_files": [{"path":"report/final.docx","sha256":"ACTUAL_SHA256"}],
  "pages": {"pdf_path":"report/final.pdf","count":28,"reviewed":[1,2],"renderer":"Actual renderer and version"}
}
```

简例并未完成验收。`reviews`必须覆盖`sources,independent_math,model_economics,narrative,layout`。每项留真实范围、审阅者、AI/人类身份和证据文件。`reviewed_files`覆盖最终报告、数字绑定、模型manifest和模型输出；输入/代码修改导致哈希不一致，应重算并重审受影响部分。页数从实际PDF获得，`reviewed`须列全部实际审阅页。

独立计算使用不同实现或直接原始算式，说明范围；审阅不必自动使用多agent，当前任务有授权且有实际价值时才考虑分工。经济审阅检查增长/投资、现金/融资、资本结构和权利边界；读者审阅检查判断、连贯性和条件；布局审阅检查实际图像。

Word或其他排版器导出后，检查标题层级、目录页码、表序、字体、数字对齐、重复表头、行高、公式、引用和跨页。公式复杂时用可编辑数学或验证过的渲染公式；不能把纯文本近似假称原生公式。默认参考样式可用A4、清楚的黑色标题、统一深色表头和淡色隔行，但用户模板优先。源样本的具体字号不是强制规范。

若首选渲染器不可用，诊断后使用环境可用替代方式，例如Word原生导出加PDF页面栅格化，并记录方法。没有真正渲染/阅读就明确排版未验证；不要凭“存在文件”通过布局审阅。

最终交付索引说明报告入口、模型命令、输入/结果位置、重要条件、检查覆盖和未完成事项。把核验通过、可复现、经济结论、人工认可和正式提交分别说明。公开发布和持续监控按用户授权执行，不是本流程自动附带动作。
