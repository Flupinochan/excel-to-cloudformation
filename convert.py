"""ExcelファイルをCloudFormationテンプレートに変換する"""

from __future__ import annotations

import warnings
from pathlib import Path

import openpyxl
from jinja2 import Environment, FileSystemLoader

from utils import get_horizontal_key_value_dict, get_horizontal_key_value_pairs, get_vertical_key_value_pairs

# ファイル読み込み時の警告を無視
warnings.filterwarnings("ignore")

# Jinja2のテンプレート読み込み設定
jinja_env = Environment(loader=FileSystemLoader("."), autoescape=True)
jinja_template_name = "jinja_cloudformatin_template.j2"
jinja2_template = jinja_env.get_template(jinja_template_name)

# Excelファイル読み込み設定
excel_file_name = "【EC2】パラメータシート.xlsx"
wb = openpyxl.load_workbook(excel_file_name)

# EC2インスタンス設定
ec2_tags = get_horizontal_key_value_pairs(wb, "タグ")
ec2_ami_id = get_horizontal_key_value_dict(wb, "AMI")
ec2_instance_type = get_horizontal_key_value_dict(wb, "インスタンスタイプ")
ec2_network = get_horizontal_key_value_dict(wb, "ネットワーク")
ec2_security_group_id = get_horizontal_key_value_dict(wb, "セキュリティグループ")
ec2_storage = get_horizontal_key_value_dict(wb, "ストレージ")
ec2_other_settings = get_horizontal_key_value_dict(wb, "高度な詳細")

# Windows Server OS設定
os_users = get_vertical_key_value_pairs(wb, "OSユーザ")

# Jinja2テンプレートに適用するデータ(キーと値)
jinja2_data = {
    "ec2_tags": ec2_tags,
    **ec2_ami_id,
    **ec2_instance_type,
    **ec2_network,
    **ec2_security_group_id,
    **ec2_storage,
    **ec2_other_settings,
    "os_users": os_users,
}

# Jinja2テンプレートに適用し、CloudFormationテンプレートを生成
cloudformation_template = jinja2_template.render(**jinja2_data)
print(cloudformation_template)
with Path("cloudformation_template.yaml").open("w", encoding="utf-8") as f:
    f.write(cloudformation_template)
