#!/usr/bin/env python3

import re
import sys
import os.path
from typing import Union


def parse_line(line: str):
    normalized = re.sub(r"\s+|//.*", "", line)
    if not normalized:
        return None

    output = {}
    if normalized[0] == "@":
        output = {"instruction": "a", "value": normalized[1:]}
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
        output = {"instruction": "c", "dest": dest, "comp": comp, "jump": jump}

    return output


def parse_file(filename: str):
    parsed_lines = []
    with open(filename) as file:
        for line in file:
            parsed_lines.append(parse_line(line))
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


def assemble(input_filename: str, output_filename: str):
    with open(output_filename, "w") as output_file:
        parsed_lines = parse_file(input_filename)
        for parsed in parsed_lines:
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
    output_filepath = filepath + ".hack"

    if not os.path.isfile(input_filepath):
        raise Exception(
            f"Input file does not exist at {os.path.abspath(input_filepath)}"
        )

    assemble(input_filepath, output_filepath)
