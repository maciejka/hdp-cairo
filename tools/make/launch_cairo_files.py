#!venv/bin/python3
import os
import readline
import argparse
import inquirer
from tools.py.utils import create_directory, get_files_from_folders

# Constants
CAIRO_PROGRAMS_FOLDERS = ["tests/cairo_programs/", "src/", "src/decoders/starknet/"]

BUILD_DIR = "build"
PROFILING_DIR = os.path.join(BUILD_DIR, "profiling")
COMPILED_FILES_DIR = os.path.join(BUILD_DIR, "compiled_cairo_files")


class CairoRunner:
    def __init__(self):
        self.cairo_programs = get_files_from_folders(CAIRO_PROGRAMS_FOLDERS, ".cairo")
        self.filename_dot_cairo_path = ""
        self.filename_dot_cairo = ""
        self.json_input_path = ""
        self.filename = ""
        self.args = self.parse_arguments()
        create_directory(BUILD_DIR)
        create_directory(COMPILED_FILES_DIR)
        create_directory(PROFILING_DIR)

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(
            description="A tool for running cairo programs."
        )
        parser.add_argument(
            "-profile", action="store_true", help="Enable pprof profile"
        )
        parser.add_argument("-pie", action="store_true", help="Create PIE object")
        parser.add_argument("-test", action="store_true", help="Run all tests")
        parser.add_argument("-test_hdp", action="store_true", help="Run hdp tests")
        parser.add_argument("-run_hdp", action="store_true", help="Run HDP")
        parser.add_argument(
            "-contract_dry_run", action="store_true", help="Run contract dry run"
        )
        return parser.parse_args()

    def setup_autocomplete(self):
        """Set up readline autocomplete with available Cairo program names."""
        # Splitting paths and basenames for easier searching.
        base_names = [os.path.basename(x) for x in self.cairo_programs]

        def completer(text, state):
            suggestions = [name for name in base_names if name.startswith(text)]
            try:
                suggestion = suggestions[state]
                return suggestion
            except IndexError:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    def prompt_for_cairo_file(self):
        """Prompt the user to select a Cairo file to run."""
        self.setup_autocomplete()

        while True:
            self.filename_dot_cairo = input(
                "\n>>> Enter .cairo file name or press <TAB> for suggestions:\n\n"
            )

            if self._is_cairo_file_valid():
                self._handle_special_file_cases()
                self.filename = self.filename_dot_cairo.removesuffix(".cairo")
                return
            else:
                print(
                    f"### File '{self.filename_dot_cairo}' not found in the Cairo programs folders."
                )

    def _is_cairo_file_valid(self):
        """Check if the provided Cairo file name is valid."""
        for cairo_path in self.cairo_programs:
            if cairo_path.endswith(self.filename_dot_cairo):
                self.filename_dot_cairo_path = cairo_path
                return True
        return False

    def _handle_special_file_cases(self):
        """Set specific JSON input paths for special Cairo file cases."""

        if self.filename_dot_cairo == "chunk_processor.cairo":
            self._select_input_file("src/single_chunk_processor/data")
        else:
            self._set_default_json_input_path()

        print(f"Selected JSON file: {self.json_input_path}")

    def _select_input_file(self, json_files_dir):
        """Allow the user to select an input JSON file for the chunk processor."""
        json_files = [
            f for f in os.listdir(json_files_dir) if f.endswith("_input.json")
        ]

        if not json_files:
            print("### No JSON files found.")
            return

        questions = [inquirer.List("file", message="Choose a file", choices=json_files)]
        selected_file = inquirer.prompt(questions)["file"]
        self.json_input_path = os.path.join(json_files_dir, selected_file)

    def _set_default_json_input_path(self):
        """Set the default JSON input path based on the Cairo file name."""
        self.json_input_path = self.filename_dot_cairo_path.replace(
            ".cairo", "_input.json"
        )

    def compile_cairo_file(self):
        while True:
            print(f"Compiling {self.filename_dot_cairo} ... ")
            compiled_path = os.path.join(COMPILED_FILES_DIR, f"{self.filename}.json")
            return_code = os.system(
                f"cairo-compile --cairo_path='packages/eth_essentials' {self.filename_dot_cairo_path} --output {compiled_path} --proof_mode"
            )

            if return_code == 0:
                return compiled_path
            print(f"### Compilation failed. Please fix the errors and try again.")
            self.prompt_for_cairo_file()

    def construct_run_command(self, compiled_path):
        cmd_base = f"cairo-run --program={compiled_path} --layout=starknet_with_keccak"
        input_flag = (
            f" --program_input={self.json_input_path} --print_output"
            if os.path.exists(self.json_input_path)
            else ""
        )
        profile_flag = (
            f" --profile_output {PROFILING_DIR}/{self.filename}/profile.pb.gz"
            if self.args.profile
            else " --print_info"
        )
        pie_flag = (
            f" --cairo_pie_output {PROFILING_DIR}/{self.filename}/{self.filename}_pie.zip"
            if self.args.pie
            else ""
        )
        return f"{cmd_base}{input_flag}{profile_flag}{pie_flag}"

    def run_hdp(self):
        self.filename_dot_cairo_path = "src/hdp.cairo"
        compiled_path = self.compile_cairo_file()
        cmd_base = f"cairo-run --program={compiled_path} --layout=starknet_with_keccak  --program_input=src/hdp_input.json --print_output --print_info --proof_mode"
        os.system(cmd_base)

    def contract_dry_run(self):
        self.filename_dot_cairo_path = "src/contract_dry_run.cairo"
        compiled_path = self.compile_cairo_file()
        cmd_base = f"cairo-run --program={compiled_path} --layout=starknet_with_keccak  --program_input=src/dry_run_input.json --print_output"
        os.system(cmd_base)

    def run(self):
        self.prompt_for_cairo_file()
        print(f"Selected Cairo file: {self.filename_dot_cairo_path}")
        create_directory(f"{PROFILING_DIR}/{self.filename}")

        compiled_path = self.compile_cairo_file()
        run_command = self.construct_run_command(compiled_path)
        os.system(run_command)

        if self.args.profile:
            self.run_profiling_tool()

    def test(self):
        """Run all tests."""
        tests_files = get_files_from_folders(["tests/cairo_programs"], ".cairo")
        for test_file in tests_files:
            if test_file != "tests/cairo_programs/tx_decoder.cairo":
                continue

            self.filename_dot_cairo_path = test_file
            self.filename_dot_cairo = os.path.basename(test_file)
            self.filename = self.filename_dot_cairo.removesuffix(".cairo")
            self.compile_cairo_file()
            run_command = self.construct_run_command(
                os.path.join(COMPILED_FILES_DIR, f"{self.filename}.json")
            )
            return_code = os.system(run_command)
            if return_code != 0:
                print(f"### Test {self.filename_dot_cairo} failed.")
                print(f"### Aborting tests.")
                return
            else:
                print(f"Test {self.filename_dot_cairo} passed.")
        print(f"All tests passed.")

    def run_profiling_tool(self):
        """Run the profiling tool for the selected Cairo file."""
        print(f"Running profiling tool for {self.filename_dot_cairo} ... ")
        os.system(
            f"cd {PROFILING_DIR}/{self.filename} && go tool pprof -png profile.pb.gz"
        )


if __name__ == "__main__":
    x = CairoRunner()
    if x.args.test:
        x.test()
    elif x.args.run_hdp:
        x.run_hdp()
    elif x.args.contract_dry_run:
        x.contract_dry_run()
    else:
        x.run()
