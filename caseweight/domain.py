"""独立业务规则，仅依赖冻结资料。"""
def quote(data, request):
    count = request['count']
    crate = request['crate']
    available = float(request['available_kg'])
    if isinstance(count, bool) or not isinstance(count, int) or count not in (8, 10, 12, 16):
        raise ValueError('株数不在包装许可范围')
    if crate not in data['crates'] or available < 0:
        raise ValueError('箱规或可用量非法')
    rule = data['crates'][crate]
    if count > rule['max_count']:
        raise ValueError('箱型容积不支持该株数')
    return {'count': count, 'crate': crate, 'tare_g': rule['tare_g'],
            'tare_sd_g': rule['tare_sd_g'], 'minimum_net_g': rule['minimum_net_g'],
            'packing_yuan': round(rule['fixed_yuan'] + count * 0.04, 2),
            'usable_kg': available * (1 - rule['handling_loss']), 'scale_step_g': 5,
            'rule_version': data['rule_version']}

def gross_to_net(data, request):
    crate = request['crate']
    if crate not in data['crates']:
        raise ValueError('箱型不存在')
    gross = float(request['gross_g'])
    tare = data['crates'][crate]['tare_g']
    if gross < tare:
        raise ValueError('毛重小于皮重')
    return {'net_g': gross - tare, 'tare_g': tare, 'unit': 'g'}

detail = gross_to_net
