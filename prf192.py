import subprocess
from termcolor import colored
import json
import os
from glob import glob
import pandas as pd
import re
import argparse


def preprocess(s):
    s = s.replace(" \n", "\n")
    if len(s) == 0:
        return s
    if s[-1] in " \n":
        s = s[:-1]

    return s


def compute_grade(gold_out, out):
    gold_out = preprocess(gold_out)
    out = preprocess(out)

    return out == gold_out


def run_c_program(c_file_path, testcases, timeout=10):
    """
    args:
        c_file_path: full path of c source file
        testcases: {"tc1": {"inp": "xx", "out": "yy"}, "tc2": {"inp": "xx", "out": "yy"}, ..}
    returns:
        res: {cp_err: bool, cp_err_text, tc_res: {tc1: {ex_err: bool, ex_err_text, out}, ..}}
    """

    cp_result = subprocess.run(["gcc",
                                c_file_path,
                                "-o",
                                c_file_path[:-2] + ".out",
                                "-Wno-implicit-function-declaration",
                                "-Wimplicit-function-declaration",
                                "-Wno-format",
                                "-Wformat-extra-args",
                                "-Wno-format-insufficient-args",
                                "-lm"],
                               capture_output=True,
                               text=False)
    if cp_result.returncode != 0:
        cp_err_text = cp_result.stderr.decode("utf-8", errors="ignore")
        print(colored(f"cp_err: {cp_err_text}", "red"))
        return {
            "cp_err": True,
            "cp_err_text": cp_err_text,
            "tc_res": {},
            "avg_grade": 0}

    res = {"cp_err": False, "cp_err_text": "", "tc_res": {}}
    for testcase_name, testcase in testcases.items():
        try:
            execution_result = subprocess.run([c_file_path[:-2] + ".out"],
                                              input=testcase["inp"].encode(
                                                  "utf-8"),
                                              capture_output=True,
                                              text=False,
                                              timeout=timeout)
            if execution_result.returncode != 0:
                ex_err_text = execution_result.stderr.decode("utf-8", errors="ignore")
                print(colored(f"Execution error on {testcase_name}. {ex_err_text}", "magenta"))
                res["tc_res"][testcase_name] = {
                    "ex_err": True,
                    "ex_err_text": ex_err_text,
                    "out": "",
                    "grade": 0}
            else:
                output = execution_result.stdout.decode(
                    "utf-8", errors="ignore")
                grade = compute_grade(testcase["out"], output)
                res["tc_res"][testcase_name] = {
                    "ex_err": False,
                    "ex_err_text": "",
                    "out": output,
                    "grade": grade}
        except subprocess.TimeoutExpired:
            print(colored(f"Timeout on testcase {testcase_name}", "red"))
            res["tc_res"][testcase_name] = {
                "ex_err": True,
                "ex_err_text": "Execution timed out",
                "out": "",
                "grade": 0
            }

    res["avg_grade"] = round(sum([res["tc_res"][tc_name]["grade"]
                             for tc_name in testcases.keys()]) / len(testcases), 1)

    return res


def process_c_files(source_files, testcases,
                    show_output=True, timeout=10):
    """
    args:
        source_files: list of c source files with the full paths, ["./SE1911workshop1/source/prob1/ce123456prob1.c", ..]
        testcases: dict of testcases, {"tc1": {"inp": "xx", "out": "yy"}, "tc2": {"inp": "xx", "out": "yy"}, ..}
    returns:
        res_dict: result dictionary
    """

    res_dict = {}

    for c_file in source_files:
        c_filename = os.path.basename(c_file)
        print("Process", c_file)
        res_dict[c_filename] = run_c_program(
            c_file, testcases, timeout=timeout)
        if res_dict[c_filename]["cp_err"]:
            print(colored(json.dumps(res_dict[c_filename], indent=4), "red"))
        elif show_output:
            print(colored(json.dumps(res_dict[c_filename], indent=4), "cyan"))
    try:
        subprocess.run(
            f'rm "{os.path.dirname(source_files[0])}/"*.out',
            shell=True,
            check=True)
    except subprocess.CalledProcessError as e:
        print(colored(f"Run process_c_files: {e}", "red"))

    return res_dict


def is_valid(filename):
    filename = os.path.basename(filename)
    pattern = r'^[a-z]{2}\d{6}prob\d\.c$'
    return re.match(pattern, filename) is not None


def read_source_files(source_folder):
    """
    read all c files in the source_folder
    args:
        source_folder: [prob1, prob2, prob3, ..]
        prob1: [ce123456prob1.c, ce123457prob1.c, ...]
    returns:
        folders: dict {"../prob1": ["../ce123456prob1.c", "../ce123457prob1.c", ..], ..}
    """

    folders = {}
    for folder in glob(f"{source_folder}/*/"):
        folder = folder.rstrip('/')
        valid_files = []
        for file in glob(f"{folder}/*"):
            if is_valid(file):
                valid_files.append(file)
            else:
                print(colored(f"{file}: invalid file name", "magenta"))

        if len(valid_files) > 0:
            folders[folder] = valid_files
        else:
            print(
                colored(f"{folder}: folder empty or no valid files", "magenta"))

    return folders


def clean_illegal_chars(value):
    if isinstance(value, str):
        # Remove control characters (ascii code in range [0, 31])
        value = re.sub(r"[\x00-\x1F]+", "", value)

    return value


def dict2excel(dict, excel_file, grades):
    ex_dict = {}
    for folder in dict.keys():
        for file in dict[folder]:
            file_name = file[8:].split('.')[0].lower()
            student_id, prob = file[:8].lower(), file_name
            if student_id not in ex_dict:
                ex_dict[student_id] = {
                    f"{prob}_avg_grade": dict[folder][file]["avg_grade"],
                    f"{prob}_path": folder,
                    f"{prob}_file": file,
                    f"{prob}_cp_err_text": dict[folder][file]["cp_err_text"]}
            else:
                ex_dict[student_id].update(
                    {
                        f"{prob}_avg_grade": dict[folder][file]["avg_grade"],
                        f"{prob}_path": folder,
                        f"{prob}_file": file,
                        f"{prob}_cp_err_text": dict[folder][file]["cp_err_text"]})

            tc_names = dict[folder][file]["tc_res"].keys()
            col_names = [
                f"{prob}_{tc_name}_{subfix}" for tc_name in tc_names for subfix in [
                    "grade", "out", "ex_err_text"]]

            if dict[folder][file]["cp_err"]:
                for col_name in col_names:
                    ex_dict[student_id][col_name] = ""
            else:
                for tc_name in tc_names:
                    ex_dict[student_id][f"{prob}_{tc_name}_grade"] = dict[folder][file]["tc_res"][tc_name]["grade"]
                    ex_dict[student_id][f"{prob}_{tc_name}_out"] = dict[folder][file]["tc_res"][tc_name]["out"]
                    ex_dict[student_id][f"{prob}_{tc_name}_ex_err_text"] = dict[folder][file]["tc_res"][tc_name]["ex_err_text"]

    df = pd.DataFrame.from_dict(ex_dict, orient="index")
    left_cols = sorted([col for col in df.columns if "grade" in col])
    right_cols = sorted([col for col in df.columns if "grade" not in col])
    df = df.reindex(columns=left_cols + right_cols)
    df.insert(loc=0, column="student id", value=df.index)

    avg_columns = [prob + "_avg_grade" for prob in grades]
    weight_list = grades.values()
    weighted_sum = (df[avg_columns] * weight_list).sum(axis=1)
    df.insert(1, 'total_grade', weighted_sum)

    df = df.map(clean_illegal_chars)
    df.sort_values(by='student id', inplace=True)
    df.to_excel(excel_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PRF192 Grader")
    parser.add_argument("source_folder", help="Folder containing source files")
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout for running C programs (default: 10 seconds)")
    parser.add_argument("--show_output",
                        action="store_true",
                        help="Show output when running c file")
    args = parser.parse_args()
    source_folder = args.source_folder
    timeout = args.timeout
    show_output = args.show_output

    testcase_json_file = f"{source_folder}/testcases.json"
    json_out_file = f"{source_folder}/result.json"
    excel_grade_file = f"{source_folder}/result.xlsx"

    testcases = json.load(open(testcase_json_file))
    grades = testcases["grades"]
    testcases = testcases["testcases"]
    source_files = read_source_files(source_folder)

    res_dict = {}
    for folder in source_files.keys():
        folder_name = os.path.basename(folder)
        res_dict[folder] = process_c_files(source_files[folder],
                                           testcases[folder_name],
                                           show_output=show_output,
                                           timeout=timeout)

    json.dump(res_dict, open(json_out_file, "w"), indent=4)
    dict2excel(res_dict, excel_grade_file, grades)
    print("Output was successfully written to result.json, result.xlsx files.")
