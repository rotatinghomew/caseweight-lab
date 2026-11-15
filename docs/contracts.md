# 资料与接口约定

## 领域记录
individual 是独立取走的单株净重，aggregate 是另取整筐的毛重和株数；paired_with_individuals=false 表示不含逐株记录中的实物。同 harvest_day、plot 和 batch 共享来源，measured_day 可能迟于采收。全部重量字段为克，可用量请求为 kg。POST /quote 接受 count、crate、available_kg，返回许可箱规、净重下限、皮重误差、处理损耗及费用，超容积不核价；POST /detail 接受 crate、gross_g，返回去皮后的净重。损耗不是称量误差。



## 冻结来源
GET /manifest 返回 release、digest、row_count、metadata。digest 对完整领域资料按 JSON 键排序、紧凑分隔和 UTF-8 计算 SHA-256。
GET /records 及后续 cursor 请求、POST /quote、POST /detail 都要求 If-Match 等于清单 release，否则返回 412。
游标仅用于所属版本，客户端不能自行猜测页数。source 进程在启动时固定加载 data/release.json。
业务请求成功返回 release、request、result；业务值非法返回 422，游标不合法返回 400，未知地址返回 404。
仅有资料概览与领域核价，不含方案选型、统计推断或预测能力。

## 已有消费接口
GET /health 返回 status=ok；GET /overview 返回 release、digest 与描述性 overview。
POST /quotes 的 JSON 为 release 和 request，结果转发来源方回执。
POST /reports 接受 release、source_digest、kind、result、receipts，返回内容寻址 id；相同内容重复保存得到同一 id。
GET /reports/{id} 返回 id 与原 payload，重启后仍可读，不重算来源资料；不存在时 404。
这些接口的字段和返回类型保持兼容，新增业务可以扩展而不改变旧档案内容。
数据数值保留原始精度；只有领域服务中已标注的金额按对应货币规则处理。
