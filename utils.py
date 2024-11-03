"""セルの値を取得するための関数一覧"""
# 関数の利用には、「ExcelのBook」と「名前の定義名」を指定する

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openpyxl.workbook import Workbook


def get_horizontal_key_value_pairs(wb: Workbook, range_name: str) -> list[list[any]]:
    """名前付き範囲において、横(キー、値)の組み合わせのリストを取得する"""
    values = []
    named_range = wb.defined_names[range_name]
    for area in named_range.destinations:
        sheet_name, cell_range = area
        sheet = wb[sheet_name]
        for row in sheet[cell_range]:
            key_value = []
            for cell in row:
                if cell.value is None:
                    continue
                key_value.append(cell.value)
            values.append(key_value)
    return values


def get_vertical_key_value_pairs(wb: Workbook, range_name: str) -> list[list[any]]:
    """名前付き範囲において、縦(キー、値)の組み合わせのリストを取得する"""
    values = []
    named_range = wb.defined_names[range_name]
    for area in named_range.destinations:
        sheet_name, cell_range = area
        sheet = wb[sheet_name]
        rows = list(sheet[cell_range])
        columns = zip(*rows)
        for col in columns:
            key_value = []
            for cell in col:
                if cell.value is None:
                    continue
                key_value.append(cell.value)
            if key_value:
                values.append(key_value)
    return values


def get_horizontal_key_value_dict(wb: Workbook, range_name: str) -> dict[any, any]:
    """名前付き範囲において、横(キー、値)の組み合わせの辞書を取得する"""
    values = {}
    named_range = wb.defined_names[range_name]
    for area in named_range.destinations:
        sheet_name, cell_range = area
        sheet = wb[sheet_name]
        for row in sheet[cell_range]:
            key_value = []
            for cell in row:
                if cell.value is None:
                    continue
                key_value.append(cell.value)
            values[key_value[0]] = key_value[1]
    return values
