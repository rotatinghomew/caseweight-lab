"""已有资料的描述性概览。"""
def summarize(data):
    rows = data["rows"]
    return {'individual_measurements': sum(row['kind'] == 'individual' for row in rows), 'aggregate_measurements': sum(row['kind'] == 'aggregate' for row in rows), 'harvest_batches': len({row['batch'] for row in rows}), 'weight_unit': 'g'}
