#!/usr/bin/env python3

import re
import sys
import os.path
from typing import Union


def is_symbol(value: str):
    try:
        int(value)
        return False
    except ValueError:
        return True


def parse_line(line: str):
    normalized = re.sub(r"\s+|//.*", "", line)
    if not normalized:
        return None

    if normalized[0] == "(":
        return {"label": True, "value": normalized[1:-1]}
    elif normalized[0] == "@":
        return {"instruction": "a", "value": normalized[1:]}
    else:
        dest = None
        assignment = normalized.split("=")
        if len(assignment) > 1:
            dest = assignment[0]
        right_side = assignment[-1].split(";")
        comp = right_side[0]
        jump = None
        if len(right_side) > 1:
            jump = right_side[1]
        return {"instruction": "c", "dest": dest, "comp": comp, "jump": jump}


def parse_file(filename: str):
    parsed_lines = []
    with open(filename) as file:
        for line in file:
            parsed = parse_line(line)
            if parsed:
                parsed_lines.append(parsed)
    return parsed_lines


def get_binary_string(num: str):
    return format(int(num), "015b")


comp_map = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101",
}


def get_comp_output(comp: str):
    a = "0"
    if "M" in comp:
        a = "1"
        comp = comp.replace("M", "A")
    return a + comp_map[comp]


dest_map = {
    None: "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}


def get_dest_output(dest: Union[str, None]):
    return dest_map[dest]


jump_map = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def get_jump_output(jump: Union[str, None]):
    return jump_map[jump]


def get_output(parsed_line: dict):
    if parsed_line["instruction"] == "a":
        return "0" + get_binary_string(parsed_line["value"])
    else:
        return "".join(
            [
                "111",
                get_comp_output(parsed_line["comp"]),
                get_dest_output(parsed_line["dest"]),
                get_jump_output(parsed_line["jump"]),
            ]
        )


predefined_symbols = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}


def replace_symbols(parsed_lines: list):
    symbols = {**predefined_symbols}
    no_labels = []
    for parsed in parsed_lines:
        if parsed:
            if "label" in parsed:
                symbols[parsed["value"]] = len(no_labels)
                # print("label: ", parsed["value"], len(no_labels))
            else:
                no_labels.append(parsed)

    variable_index = 16
    for parsed in no_labels:
        if parsed["instruction"] == "a" and is_symbol(parsed["value"]):
            symbol = parsed["value"]

            if symbol not in symbols:
                symbols[symbol] = variable_index
                variable_index += 1

            parsed["value"] = symbols[symbol]

    return no_labels


def assemble(input_filename: str, output_filename: str):
    parsed_lines = parse_file(input_filename)
    preprocessed_lines = replace_symbols(parsed_lines)

    with open(output_filename, "w") as output_file:
        for parsed in preprocessed_lines:
            if parsed:
                output_line = get_output(parsed)
                output_file.write(output_line + "\n")


if __name__ == "__main__":
    import argparse

    cli_parser = argparse.ArgumentParser(description="Assemble .asm files into .hack")
    cli_parser.add_argument(
        "input_filepath", help="The input file path - e.g. ./add/Add.asm"
    )

    args = cli_parser.parse_args()
    input_filepath = args.input_filepath
    filepath, file_extension = os.path.splitext(input_filepath)
    if file_extension != ".asm":
        raise Exception(
            f'Only files with .asm extension are excepted. Instead received a "{file_extension}" extension"'
        )
    output_filepath = filepath + ".hack"

    if not os.path.isfile(input_filepath):
        raise Exception(
            f"Input file does not exist at {os.path.abspath(input_filepath)}"
        )

    assemble(input_filepath, output_filepath)
