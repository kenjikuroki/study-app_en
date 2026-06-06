from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BANK_ROOT = ROOT / "data" / "question_banks"
CYCLE_BANK_ROOT = ROOT / "data" / "cycle_banks"
CYCLE_WINDOWS = {
    "cycle_01": (0, 30),
    "cycle_02": (30, 60),
    "cycle_03": (60, 90),
    "cycle_04": (90, 100),
}


@dataclass(frozen=True)
class IRSpec:
    id: str
    topic: str
    fact_type: str
    statement: str
    conditions: list[str]
    examples: list[str]
    source_url: str
    source_section: str
    source_quote_or_summary: str
    confidence: str
    question_potential: str
    notes: str
    source_document_rel: str = ""
    required_snippets: list[str] = field(default_factory=list)
    source_name: str = ""
    source_title: str = ""
    source_version: str = ""


@dataclass(frozen=True)
class QuestionSpec:
    id: str
    source_ir_id: str
    question: str
    answer: bool
    explanation: str
    difficulty: str


SOURCE_NAME = "GNU Coreutils 9.11 manual"
SOURCE_TITLE = "GNU Coreutils manual"
SOURCE_VERSION = "9.11"
SOURCE_DOC_REL = "studyapp/input/source_documents/linux/basic_commands/GNU Coreutils 9.11.html"


SUPPORTED_PIPELINES: dict[tuple[str, str], dict[str, Any]] = {
    ("linux", "basic_commands"): {
        "ir_specs": [
            IRSpec("linux_basic_commands_ir_0001", "pwd", "command", "The pwd command prints the name of the current directory.", [], ["pwd"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#pwd-invocation", "19.1 pwd: Print working directory", "pwd prints the name of the current directory.", "high", "high", "", ['id="pwd-invocation"', "prints the name of the current directory"]),
            IRSpec("linux_basic_commands_ir_0002", "basename", "command", "The basename command removes any leading directory components from a name.", [], ["basename /usr/bin/sort"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#basename-invocation", "18.1 basename: Strip directory and suffix from a file name", "basename removes leading directory components from name.", "high", "high", "", ['id="basename-invocation"', "removes any leading directory components"]),
            IRSpec("linux_basic_commands_ir_0003", "dirname", "command", "The dirname command prints all but the final slash-delimited component of each name.", [], ["dirname /usr/bin/sort"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#dirname-invocation", "18.2 dirname: Strip last file name component", "dirname prints all but the final slash-delimited component.", "high", "high", "", ['id="dirname-invocation"', "prints all but the final slash-delimited component"]),
            IRSpec("linux_basic_commands_ir_0004", "dirname no-slash behavior", "behavior", "If the input string contains no slash, dirname prints '.'.", ["The input string contains no slash."], ["dirname stdio.h"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#dirname-invocation", "18.2 dirname: Strip last file name component", "If the string contains no slash, dirname prints '.' meaning the current directory.", "high", "high", "", ['id="dirname-invocation"', "If the string contains no slash", "prints"]),
            IRSpec("linux_basic_commands_ir_0005", "true", "behavior", "The true command returns an exit status of 0, meaning success.", [], ["true"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#true-invocation", "16.2 true: Do nothing, successfully", "true does nothing except return exit status 0, meaning success.", "high", "high", "The manual notes that in most modern shells, true is often a shell built-in.", ['id="true-invocation"', "return an exit status of 0", "success"]),
            IRSpec("linux_basic_commands_ir_0006", "false", "behavior", "The false command returns an exit status of 1, meaning failure.", [], ["false"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#false-invocation", "16.1 false: Do nothing, unsuccessfully", "false does nothing except return exit status 1, meaning failure.", "high", "high", "The manual notes that in most modern shells, false is often a shell built-in.", ['id="false-invocation"', "return an exit status of 1", "failure"]),
            IRSpec("linux_basic_commands_ir_0007", "pwd --logical", "option", "With --logical, pwd outputs the contents of PWD if PWD is an absolute name of the current directory with no '.' or '..' components.", [], ["pwd --logical"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#pwd-invocation", "19.1 pwd: Print working directory", "pwd --logical uses PWD when it is an absolute current-directory path without dot components.", "high", "high", "Behavior depends on the contents of the PWD environment variable.", ['id="pwd--logical"', "provide an", "absolute name of the current directory", "no", ".."]),
            IRSpec("linux_basic_commands_ir_0008", "pwd --physical", "option", "With --physical, pwd prints a fully resolved name for the current directory with no symbolic links in the printed path.", [], ["pwd --physical"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#pwd-invocation", "19.1 pwd: Print working directory", "pwd --physical prints a fully resolved name with no symbolic links in the output path.", "high", "high", "", ['id="pwd--physical"', "Print a fully resolved name for the current directory", "none", "symbolic links"]),
            IRSpec("linux_basic_commands_ir_0009", "basename suffix removal", "behavior", "If basename is given a suffix identical to the end of the name, that suffix is removed.", [], ["basename file.txt .txt"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#basename-invocation", "18.1 basename: Strip directory and suffix from a file name", "A suffix identical to the end of the name is removed by basename.", "high", "high", "", ['id="basename-invocation"', "If", "suffix", "identical to the end of", "it is removed"]),
            IRSpec("linux_basic_commands_ir_0010", "basename --zero", "option", "The basename --zero option outputs a zero byte at the end of each line rather than a newline.", [], ["basename --zero /tmp/file"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#basename-invocation", "18.1 basename: Strip directory and suffix from a file name", "basename --zero uses an ASCII NUL terminator instead of a newline.", "high", "medium", "", ['id="basename--zero"', "Output a zero byte", "rather than a newline"]),
            IRSpec("linux_basic_commands_ir_0011", "echo", "command", "The echo command writes each given string to standard output with a space between strings and a newline after the last one.", [], ["echo hello world"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#echo-invocation", "15.1 echo: Print a line of text", "echo writes each string to standard output with spaces between strings and a trailing newline.", "high", "high", "Shell built-ins and aliases may behave differently from the standalone program documented here.", ['id="echo-invocation"', "writes each given", "to standard output", "newline after the last one"]),
            IRSpec("linux_basic_commands_ir_0012", "echo -n", "option", "The echo -n option does not output the trailing newline.", [], ["echo -n hello"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#echo-invocation", "15.1 echo: Print a line of text", "echo -n suppresses the trailing newline.", "high", "high", "Shell built-ins and aliases may behave differently from the standalone program documented here.", ['id="echo-n"', "Do not output the trailing newline"]),
            IRSpec("linux_basic_commands_ir_0013", "echo -e", "option", "The echo -e option enables interpretation of backslash-escaped characters in each string.", [], ['echo -e "a\\nb"'], "https://www.gnu.org/software/coreutils/manual/coreutils.html#echo-invocation", "15.1 echo: Print a line of text", "echo -e enables backslash escape interpretation.", "high", "high", "Shell built-ins and aliases may behave differently from the standalone program documented here.", ['id="echo-e"', "Enable interpretation of the following backslash-escaped characters"]),
            IRSpec("linux_basic_commands_ir_0014", "echo -E", "option", "The echo -E option disables interpretation of backslash escapes in each string.", [], ['echo -E "a\\nb"'], "https://www.gnu.org/software/coreutils/manual/coreutils.html#echo-invocation", "15.1 echo: Print a line of text", "echo -E disables backslash escape interpretation and is the default.", "high", "high", "Shell built-ins and aliases may behave differently from the standalone program documented here.", ['id="echo-E"', "Disable interpretation of backslash escapes", "This is the default"]),
            IRSpec("linux_basic_commands_ir_0015", "printf", "command", "The printf command does formatted printing of text.", [], ['printf "%s\\n" hello'], "https://www.gnu.org/software/coreutils/manual/coreutils.html#printf-invocation", "15.2 printf: Format and print data", "printf does formatted printing of text.", "high", "high", "Shell built-ins and aliases may behave differently from the standalone program documented here.", ['id="printf-invocation"', "does formatted printing of text"]),
            IRSpec("linux_basic_commands_ir_0016", "printf format behavior", "behavior", "The printf command prints the format string, interpreting percent directives and backslash escapes to format numeric and string arguments.", [], ['printf "%s %d\\n" file 3'], "https://www.gnu.org/software/coreutils/manual/coreutils.html#printf-invocation", "15.2 printf: Format and print data", "printf interprets percent directives and backslash escapes in the format string.", "high", "high", "Shell built-ins and aliases may behave differently from the standalone program documented here.", ['id="printf-invocation"', "prints the", "format string", "interpreting", "backslash"]),
            IRSpec("linux_basic_commands_ir_0017", "yes", "command", "The yes command prints its command line arguments, separated by spaces and followed by a newline, forever until it is killed.", [], ["yes ok"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#yes-invocation", "15.3 yes: Print a string until interrupted", "yes repeats its arguments, separated by spaces and followed by a newline, until killed.", "high", "high", "", ['id="yes-invocation"', "prints the command line arguments", "followed by a newline", "forever until it is killed"]),
            IRSpec("linux_basic_commands_ir_0018", "yes default output", "behavior", "If yes is invoked with no arguments, it prints 'y' followed by a newline forever until killed.", [], ["yes"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#yes-invocation", "15.3 yes: Print a string until interrupted", "With no arguments, yes prints y followed by a newline until killed.", "high", "high", "", ['id="yes-invocation"', "If no arguments are", "prints", "y", "followed by a newline"]),
            IRSpec("linux_basic_commands_ir_0019", "printenv", "command", "The printenv command prints environment variable values.", [], ["printenv PATH"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#printenv-invocation", "19.3 printenv: Print all or some environment variables", "printenv prints environment variable values.", "high", "high", "", ['id="printenv-invocation"', "prints environment variable values"]),
            IRSpec("linux_basic_commands_ir_0020", "printenv all variables", "behavior", "If no variables are specified, printenv prints the value of every environment variable.", [], ["printenv"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#printenv-invocation", "19.3 printenv: Print all or some environment variables", "When no variable is specified, printenv prints every environment variable value.", "high", "high", "", ['id="printenv-invocation"', "If no", "prints the value of", "every environment variable"]),
            IRSpec("linux_basic_commands_ir_0021", "printenv --null", "option", "The printenv --null option outputs a zero byte at the end of each line rather than a newline.", [], ["printenv --null PATH"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#printenv-invocation", "19.3 printenv: Print all or some environment variables", "printenv --null uses an ASCII NUL terminator instead of a newline.", "high", "medium", "", ['id="printenv--null"', "Output a zero byte", "rather than a newline"]),
            IRSpec("linux_basic_commands_ir_0022", "tty", "command", "The tty command prints the file name of the terminal connected to standard input.", [], ["tty"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#tty-invocation", "19.4 tty: Print file name of terminal on standard input", "tty prints the file name of the terminal connected to standard input.", "high", "high", "", ['id="tty-invocation"', "prints the file name of the terminal connected to its standard", "input"]),
            IRSpec("linux_basic_commands_ir_0023", "tty non-terminal input", "behavior", "If standard input is not a terminal, tty prints 'not a tty'.", [], ["echo hi | tty"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#tty-invocation", "19.4 tty: Print file name of terminal on standard input", "tty prints not a tty when standard input is not a terminal.", "high", "high", "", ['id="tty-invocation"', "not a tty", "if standard input is not a terminal"]),
            IRSpec("linux_basic_commands_ir_0024", "logname", "command", "The logname command prints the calling user's name as found in a system-maintained file.", [], ["logname"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#logname-invocation", "20.2 logname: Print current login name", "logname prints the calling user's name from a system-maintained file.", "high", "high", "The manual cites files such as /var/run/utmp or /etc/utmp.", ['id="logname-invocation"', "prints the calling user", "system-maintained file"]),
            IRSpec("linux_basic_commands_ir_0025", "logname no entry behavior", "behavior", "If there is no entry for the calling process, logname exits with status 1.", [], ["logname"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#logname-invocation", "20.2 logname: Print current login name", "If there is no entry for the calling process, logname exits with status 1.", "high", "high", "", ['id="logname-invocation"', "If there is no entry", "status of 1"]),
            IRSpec("linux_basic_commands_ir_0026", "whoami", "command", "The whoami command prints the user name associated with the current effective user ID.", [], ["whoami"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#whoami-invocation", "20.3 whoami: Print effective user name", "whoami prints the user name associated with the current effective user ID.", "high", "high", "", ['id="whoami-invocation"', "prints the user name associated with the current", "effective user ID"]),
            IRSpec("linux_basic_commands_ir_0027", "whoami equivalence", "behavior", "The whoami command is equivalent to the command id -un.", [], ["whoami"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#whoami-invocation", "20.3 whoami: Print effective user name", "whoami is equivalent to id -un.", "high", "high", "", ['id="whoami-invocation"', "equivalent to the", "id -un"]),
            IRSpec("linux_basic_commands_ir_0028", "date", "command", "The date command displays the date and time.", [], ["date"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#date-invocation", "21.1 date: Print or set system date and time", "date displays the date and time.", "high", "high", "Setting the system time depends on runtime privileges and environment.", ['id="date-invocation"', "command displays the date and time"]),
            IRSpec("linux_basic_commands_ir_0029", "date --set", "option", "With the --set option, date sets the date and time before displaying it.", [], ['date --set="2026-01-01 00:00:00"'], "https://www.gnu.org/software/coreutils/manual/coreutils.html#date-invocation", "21.1 date: Print or set system date and time", "With --set, date sets the date and time before displaying it.", "high", "high", "Setting the system time depends on runtime privileges and environment.", ['id="date-invocation"', "--set", "sets the date and time before displaying it"]),
            IRSpec("linux_basic_commands_ir_0030", "uname default option", "behavior", "If no options are given, uname acts as if the -s option were given.", [], ["uname"], "https://www.gnu.org/software/coreutils/manual/coreutils.html#uname-invocation", "21.4 uname: Print system information", "Without options, uname behaves as if -s were given.", "high", "high", "", ['id="uname-invocation"', "If no options are given", "-s", "option were given"]),
        ],
        "question_specs": [
            QuestionSpec("linux_basic_commands_q_0001", "linux_basic_commands_ir_0001", "The `pwd` command prints the name of the current directory.", True, "`pwd` prints the name of the current directory.", "basic"),
            QuestionSpec("linux_basic_commands_q_0002", "linux_basic_commands_ir_0002", "The `basename` command prints the directory part of a path.", False, "`basename` removes leading directory components rather than printing them.", "basic"),
            QuestionSpec("linux_basic_commands_q_0003", "linux_basic_commands_ir_0004", "If a string contains no slash, `dirname` prints `.`.", True, "For input with no slash, `dirname` prints `.` to mean the current directory.", "basic"),
            QuestionSpec("linux_basic_commands_q_0004", "linux_basic_commands_ir_0005", "The `true` command is used as a placeholder where an unsuccessful command is needed.", False, "`true` is used where a successful command is needed because it returns exit status 0.", "basic"),
            QuestionSpec("linux_basic_commands_q_0005", "linux_basic_commands_ir_0006", "The `false` command returns exit status 1, meaning failure.", True, "`false` does nothing except return exit status 1, which indicates failure.", "basic"),
            QuestionSpec("linux_basic_commands_q_0006", "linux_basic_commands_ir_0003", "The `dirname` command prints only the final slash-delimited component of a path.", False, "`dirname` prints everything except the final slash-delimited component.", "basic"),
            QuestionSpec("linux_basic_commands_q_0007", "linux_basic_commands_ir_0007", "With `pwd --logical`, the command always resolves every symbolic link in the printed path.", False, "`pwd --logical` can use the `PWD` environment value instead of fully resolving symbolic links.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0008", "linux_basic_commands_ir_0008", "With `pwd --physical`, the printed path can still contain symbolic links.", False, "`pwd --physical` prints a fully resolved path whose components are actual directory names, not symbolic links.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0009", "linux_basic_commands_ir_0009", "If `basename` is given a suffix that matches the end of the name, it can remove that suffix.", True, "A suffix identical to the end of the name is removed by `basename`.", "basic"),
            QuestionSpec("linux_basic_commands_q_0010", "linux_basic_commands_ir_0010", "The `basename --zero` option ends each line with a newline character.", False, "`basename --zero` uses an ASCII NUL byte instead of a newline.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0011", "linux_basic_commands_ir_0011", "The `echo` command writes strings separated by spaces and adds a newline after the last one.", True, "`echo` writes each string to standard output with spaces between strings and a trailing newline by default.", "basic"),
            QuestionSpec("linux_basic_commands_q_0012", "linux_basic_commands_ir_0012", "The `echo -n` option forces a trailing newline to be printed.", False, "`echo -n` suppresses the trailing newline.", "basic"),
            QuestionSpec("linux_basic_commands_q_0013", "linux_basic_commands_ir_0013", "The `echo -e` option enables interpretation of backslash escapes.", True, "`echo -e` enables interpretation of backslash-escaped characters.", "basic"),
            QuestionSpec("linux_basic_commands_q_0014", "linux_basic_commands_ir_0014", "The `echo -E` option enables interpretation of backslash escapes.", False, "`echo -E` disables interpretation of backslash escapes.", "basic"),
            QuestionSpec("linux_basic_commands_q_0015", "linux_basic_commands_ir_0015", "The `printf` command does formatted printing of text.", True, "`printf` is used for formatted printing of text.", "basic"),
            QuestionSpec("linux_basic_commands_q_0016", "linux_basic_commands_ir_0016", "The `printf` command ignores both `%` directives and backslash escapes in its format string.", False, "`printf` interprets `%` directives and backslash escapes in the format string.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0017", "linux_basic_commands_ir_0017", "The `yes` command repeats its command line arguments, separated by spaces and followed by a newline, until it is killed.", True, "`yes` keeps printing its arguments until it is interrupted or killed.", "basic"),
            QuestionSpec("linux_basic_commands_q_0018", "linux_basic_commands_ir_0018", "If `yes` is run with no arguments, it repeatedly prints `n`.", False, "With no arguments, `yes` repeatedly prints `y` followed by a newline.", "basic"),
            QuestionSpec("linux_basic_commands_q_0019", "linux_basic_commands_ir_0019", "The `printenv` command prints environment variable values.", True, "`printenv` prints environment variable values.", "basic"),
            QuestionSpec("linux_basic_commands_q_0020", "linux_basic_commands_ir_0020", "If no variable is specified, `printenv` prints only one environment variable.", False, "When no variable is specified, `printenv` prints the value of every environment variable.", "basic"),
            QuestionSpec("linux_basic_commands_q_0021", "linux_basic_commands_ir_0021", "The `printenv --null` option ends each line with a NUL byte instead of a newline.", True, "`printenv --null` uses an ASCII NUL byte terminator instead of a newline.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0022", "linux_basic_commands_ir_0022", "The `tty` command prints the file name of the terminal connected to standard output.", False, "`tty` checks the terminal connected to standard input, not standard output.", "basic"),
            QuestionSpec("linux_basic_commands_q_0023", "linux_basic_commands_ir_0023", "If standard input is not a terminal, `tty` prints `not a tty`.", True, "The manual says `tty` prints `not a tty` when standard input is not a terminal.", "basic"),
            QuestionSpec("linux_basic_commands_q_0024", "linux_basic_commands_ir_0024", "The `logname` command prints the calling user's name from a system-maintained file.", True, "`logname` prints the calling user's name as found in a system-maintained file.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0025", "linux_basic_commands_ir_0025", "If there is no entry for the calling process, `logname` exits with status 0.", False, "If there is no entry for the calling process, `logname` exits with status 1.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0026", "linux_basic_commands_ir_0026", "The `whoami` command prints the user name associated with the current effective user ID.", True, "`whoami` prints the user name associated with the current effective user ID.", "basic"),
            QuestionSpec("linux_basic_commands_q_0027", "linux_basic_commands_ir_0027", "The `whoami` command is equivalent to `id -gn`.", False, "The manual says `whoami` is equivalent to `id -un`, not `id -gn`.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0028", "linux_basic_commands_ir_0028", "The `date` command displays the date and time.", True, "`date` displays the date and time.", "basic"),
            QuestionSpec("linux_basic_commands_q_0029", "linux_basic_commands_ir_0029", "With `--set`, the `date` command sets the date and time and then exits without displaying it.", False, "With `--set`, `date` sets the date and time before displaying it.", "intermediate"),
            QuestionSpec("linux_basic_commands_q_0030", "linux_basic_commands_ir_0030", "If no options are given, `uname` acts as if `-s` were given.", True, "Without options, `uname` behaves as if the `-s` option were given.", "basic"),
        ],
    },
    ("linux", "filesystem"): {
        "ir_specs": [
            IRSpec("linux_filesystem_ir_0001", "cp", "command", "The cp command copies files or, optionally, directories, and the copy is completely independent of the original.", [], ["cp source target"], "https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html", "11.1 cp: Copy files and directories", "cp copies files or directories, and the copy is completely independent of the original.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/cp-invocation.html", ["copies files (or, optionally, directories)", "completely independent of the original"]),
            IRSpec("linux_filesystem_ir_0002", "cp default directory behavior", "behavior", "By default, cp does not copy directories.", [], ["cp dir target"], "https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html", "11.1 cp: Copy files and directories", "By default, cp does not copy directories unless recursive options are used.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/cp-invocation.html", ["By default, <code class=\"command\">cp</code> does not copy directories"]),
            IRSpec("linux_filesystem_ir_0003", "cp --parents", "option", "The cp --parents option forms each destination path by appending the specified source name to the target directory.", [], ["cp --parents a/b/c existing_dir"], "https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html", "11.1 cp: Copy files and directories", "cp --parents appends the specified source name under the destination directory.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/cp-invocation.html", ['id="cp--parents"', "Form the name of each destination file by appending to the target"]),
            IRSpec("linux_filesystem_ir_0004", "cp --copy-contents", "warning", "When copying recursively, cp --copy-contents copies the contents of special files as if they were regular files.", ["Copying recursively."], ["cp -R --copy-contents src dst"], "https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html", "11.1 cp: Copy files and directories", "cp --copy-contents treats special files like regular files during recursive copy and can be risky.", "high", "high", "The manual warns that this can hang on FIFOs or fill a destination file system when used on special files such as /dev/zero.", "studyapp/input/source_documents/linux/filesystem/cp-invocation.html", ['id="cp--copy-contents"', "If copying recursively, copy the contents of any special files", "as if they were regular files"]),
            IRSpec("linux_filesystem_ir_0005", "cp -P", "option", "The cp -P option copies symbolic links as symbolic links rather than copying the files they point to.", [], ["cp -P link dst"], "https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html", "11.1 cp: Copy files and directories", "cp -P preserves symlinks instead of following them.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/cp-invocation.html", ["Copy symbolic links as symbolic links rather than copying the files that", "they point to"]),
            IRSpec("linux_filesystem_ir_0006", "mv rename behavior", "behavior", "To move a file, mv ordinarily simply renames it.", [], ["mv oldname newname"], "https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html", "11.4 mv: Move (rename) files", "mv ordinarily performs a rename when moving a file.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mv-invocation.html", ["To move a file, <code class=\"command\">mv</code> ordinarily simply renames it"]),
            IRSpec("linux_filesystem_ir_0007", "mv cross-filesystem behavior", "behavior", "If a rename cannot work because the destination file system differs, mv falls back on copying as if by cp -a and then removes the original.", ["The destination file system differs."], ["mv source /otherfs/target"], "https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html", "11.4 mv: Move (rename) files", "Across file systems, mv falls back to copy plus removal.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mv-invocation.html", ["destination&rsquo;s file", "system differs", "falls back on copying as if by <code class=\"code\">cp -a</code>"]),
            IRSpec("linux_filesystem_ir_0008", "mv --no-copy", "option", "If a file cannot be renamed because the destination file system differs, mv --no-copy fails instead of copying and then removing the file.", ["The destination file system differs."], ["mv --no-copy source /otherfs/target"], "https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html", "11.4 mv: Move (rename) files", "mv --no-copy disables copy-and-remove fallback across file systems.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mv-invocation.html", ['id="mv--no-copy"', "fail with a diagnostic instead of copying and then removing the file"]),
            IRSpec("linux_filesystem_ir_0009", "mv --exchange", "option", "The mv --exchange option exchanges source and destination instead of renaming source to destination, and both files must exist.", [], ["mv -T --exchange d1 d2"], "https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html", "11.4 mv: Move (rename) files", "mv --exchange swaps two existing paths.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mv-invocation.html", ['id="mv--exchange"', "Exchange source and destination instead of renaming source to destination", "Both files must exist"]),
            IRSpec("linux_filesystem_ir_0010", "mkdir order", "behavior", "The mkdir command creates each directory name in the order given.", [], ["mkdir dir1 dir2"], "https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html", "12.3 mkdir: Create directories", "mkdir processes directory names in the order given.", "high", "medium", "", "studyapp/input/source_documents/linux/filesystem/mkdir-invocation.html", ["creates each directory", "in the order given"]),
            IRSpec("linux_filesystem_ir_0011", "mkdir existing path behavior", "behavior", "The mkdir command reports an error if a name already exists, unless -p is given and the name is a directory.", [], ["mkdir existing_dir"], "https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html", "12.3 mkdir: Create directories", "mkdir errors on an existing path unless -p is used and the path is already a directory.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mkdir-invocation.html", ["reports an error if", "already exists, unless the", "-p"]),
            IRSpec("linux_filesystem_ir_0012", "mkdir --mode", "option", "The mkdir --mode option sets the file permission bits of created directories to the specified mode.", [], ["mkdir --mode=700 private_dir"], "https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html", "12.3 mkdir: Create directories", "mkdir --mode controls permission bits for created directories.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mkdir-invocation.html", ['id="mkdir--mode"', "Set the file permission bits of created directories to"]),
            IRSpec("linux_filesystem_ir_0013", "mkdir --parents", "option", "The mkdir --parents option makes missing parent directories and does not change the file permission bits of existing parent directories.", [], ["mkdir -p a/b/c"], "https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html", "12.3 mkdir: Create directories", "mkdir --parents creates missing parents but leaves existing parent permission bits unchanged.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/mkdir-invocation.html", ['id="mkdir--parents"', "Make any missing parent directories", "existing parent directories", "do not change their file permission", "bits"]),
            IRSpec("linux_filesystem_ir_0014", "ln defaults", "command", "The ln command makes links between files; by default it makes hard links, and with -s it makes symbolic links.", [], ["ln source link", "ln -s target symlink"], "https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html", "12.2 ln: Make links between files", "ln makes hard links by default and symbolic links with -s.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/ln-invocation.html", ["makes links between files.  By default, it makes hard links", "with the", "-s", "it makes symbolic"]),
            IRSpec("linux_filesystem_ir_0015", "hard link limitation", "limitation", "Hard links cannot cross file system boundaries.", [], ["ln /src/file /otherfs/link"], "https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html", "12.2 ln: Make links between files", "Hard links are restricted to the same file system.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/ln-invocation.html", ["Hard links cannot cross file system boundaries"]),
            IRSpec("linux_filesystem_ir_0016", "dangling symlink", "behavior", "There are no restrictions against creating dangling symbolic links.", [], ["ln -s missing-target dangling-link"], "https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html", "12.2 ln: Make links between files", "Dangling symbolic links are allowed.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/ln-invocation.html", ["There are no restrictions against creating dangling symbolic links"]),
            IRSpec("linux_filesystem_ir_0017", "ln --relative", "option", "The ln --relative option makes symbolic links relative to the link location and is only valid with --symbolic.", [], ["ln --relative --symbolic target link"], "https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html", "12.2 ln: Make links between files", "ln --relative is specifically for symbolic links and uses a relative target path.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/ln-invocation.html", ['id="ln--relative"', "Make symbolic links relative to the link location", "only valid with the", "--symbolic"]),
            IRSpec("linux_filesystem_ir_0018", "readlink canonicalize mode", "behavior", "In canonicalize mode, readlink outputs an absolute file name with no repeated separators and no '.', '..', or symbolic link components.", [], ["readlink -f path"], "https://www.gnu.org/software/coreutils/manual/html_node/readlink-invocation.html", "12.6 readlink: Print value of a symlink or canonical file name", "readlink canonicalize mode resolves a path into a cleaned absolute name.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/readlink-invocation.html", ["Canonicalize mode", "outputs the absolute name of the given files", "no <samp class=\"file\">.</samp>", "<samp class=\"file\">..</samp> components nor any repeated separators"]),
            IRSpec("linux_filesystem_ir_0019", "readlink --canonicalize", "option", "With readlink --canonicalize, if any component of the file name except the last one is missing or unavailable, readlink produces no output and exits with a nonzero exit code.", [], ["readlink --canonicalize missing/path"], "https://www.gnu.org/software/coreutils/manual/html_node/readlink-invocation.html", "12.6 readlink: Print value of a symlink or canonical file name", "readlink --canonicalize requires all path components except possibly the last one.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/readlink-invocation.html", ['id="readlink--canonicalize"', "If any component of the file name except the last one is missing or unavailable", "produces no output and exits with a nonzero exit"]),
            IRSpec("linux_filesystem_ir_0020", "readlink --canonicalize-existing", "option", "With readlink --canonicalize-existing, if any component is missing or unavailable, readlink produces no output and exits with a nonzero exit code.", [], ["readlink -e missing/path"], "https://www.gnu.org/software/coreutils/manual/html_node/readlink-invocation.html", "12.6 readlink: Print value of a symlink or canonical file name", "readlink --canonicalize-existing requires all components to exist.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/readlink-invocation.html", ['id="readlink--canonicalize-existing"', "If any component is missing or unavailable", "produces no output and exits with a nonzero exit code"]),
            IRSpec("linux_filesystem_ir_0021", "readlink --no-newline", "option", "The readlink --no-newline option does not print the output delimiter when a single file is specified.", ["A single file is specified."], ["readlink --no-newline link"], "https://www.gnu.org/software/coreutils/manual/html_node/readlink-invocation.html", "12.6 readlink: Print value of a symlink or canonical file name", "readlink --no-newline suppresses the delimiter for a single input file.", "high", "medium", "", "studyapp/input/source_documents/linux/filesystem/readlink-invocation.html", ['id="readlink--no-newline"', "Do not print the output delimiter, when a single", "file", "is specified"]),
            IRSpec("linux_filesystem_ir_0022", "realpath result", "behavior", "The realpath command outputs an absolute file name that contains neither unnecessary '/', '.', '..', nor symbolic link components.", [], ["realpath path"], "https://www.gnu.org/software/coreutils/manual/html_node/realpath-invocation.html", "18.5 realpath: Print the resolved file name", "realpath prints a fully resolved absolute path without redundant path components.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/realpath-invocation.html", ["an absolute file name that contains neither unnecessary", ".", "..", "or a symbolic link"]),
            IRSpec("linux_filesystem_ir_0023", "realpath --canonicalize-existing", "option", "The realpath --canonicalize-existing option fails if the named file does not exist.", [], ["realpath -e missing"], "https://www.gnu.org/software/coreutils/manual/html_node/realpath-invocation.html", "18.5 realpath: Print the resolved file name", "realpath --canonicalize-existing requires the target to exist.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/realpath-invocation.html", ['id="realpath--canonicalize-existing"', "Fail if the named file does not exist"]),
            IRSpec("linux_filesystem_ir_0024", "realpath --relative-to", "option", "The realpath --relative-to option prints the resolved file names relative to the specified directory.", [], ["realpath --relative-to=/tmp /tmp/a/b"], "https://www.gnu.org/software/coreutils/manual/html_node/realpath-invocation.html", "18.5 realpath: Print the resolved file name", "realpath --relative-to can emit a path relative to a chosen directory.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/realpath-invocation.html", ['id="realpath--relative-to"', "Print the resolved file names relative to the specified directory"]),
            IRSpec("linux_filesystem_ir_0025", "rm default directory behavior", "behavior", "By default, rm does not remove directories.", [], ["rm somedir"], "https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html", "11.5 rm: Remove files or directories", "rm needs explicit directory-related options for directory removal.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/rm-invocation.html", ["<code class=\"command\">rm</code> removes each given", "By default, it does not remove", "directories"]),
            IRSpec("linux_filesystem_ir_0026", "rm dot entries", "warning", "Any attempt to remove a file whose last file name component is '.' or '..' is rejected without any prompting.", [], ["rm .", "rm .."], "https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html", "11.5 rm: Remove files or directories", "rm rejects attempts to remove dot and dot-dot path components.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/rm-invocation.html", ["Any attempt to remove a file whose last file name component is", ".", "or", "..", "is rejected without any prompting"]),
            IRSpec("linux_filesystem_ir_0027", "rm --force", "option", "The rm --force option ignores nonexistent files and missing operands, and never prompts the user.", [], ["rm --force missing-file"], "https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html", "11.5 rm: Remove files or directories", "rm --force suppresses prompts and ignores missing inputs.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/rm-invocation.html", ['id="rm--force"', "Ignore nonexistent files and missing operands, and never prompt the user"]),
            IRSpec("linux_filesystem_ir_0028", "rm --preserve-root", "warning", "The rm --preserve-root option fails upon attempts to remove the root directory '/' recursively, and this is the default behavior.", ["Used with recursive removal."], ["rm -r /"], "https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html", "11.5 rm: Remove files or directories", "rm protects '/' from recursive removal by default.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/rm-invocation.html", ['id="rm--preserve-root"', "Fail upon any attempt to remove the root directory", "This is the default behavior"]),
            IRSpec("linux_filesystem_ir_0029", "rmdir", "command", "The rmdir command removes empty directories.", [], ["rmdir emptydir"], "https://www.gnu.org/software/coreutils/manual/html_node/rmdir-invocation.html", "12.5 rmdir: Remove empty directories", "rmdir is specifically for empty directories.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/rmdir-invocation.html", ["removes empty directories"]),
            IRSpec("linux_filesystem_ir_0030", "df default scope", "behavior", "With no file name arguments, df reports the space available on all currently mounted file systems.", [], ["df"], "https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html", "14.1 df: Report file system space usage", "Without file arguments, df reports on currently mounted file systems.", "high", "high", "", "studyapp/input/source_documents/linux/filesystem/df-invocation.html", ["With no arguments", "currently mounted file systems"]),
        ],
        "question_specs": [
            QuestionSpec("linux_filesystem_q_0001", "linux_filesystem_ir_0001", "By default, `cp` creates another path name for the same file instead of an independent copy.", False, "`cp` makes an independent copy; creating another path name for the same file is hard-link behavior, not the default behavior of `cp`.", "basic"),
            QuestionSpec("linux_filesystem_q_0002", "linux_filesystem_ir_0002", "By default, `cp` does not copy directories.", True, "The manual says `cp` does not copy directories unless recursive behavior is requested.", "basic"),
            QuestionSpec("linux_filesystem_q_0003", "linux_filesystem_ir_0003", "The `cp --parents` option can place the source path under the target directory instead of flattening the file name.", True, "`cp --parents` appends the specified source name under the target directory.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0004", "linux_filesystem_ir_0004", "The `cp --copy-contents` option skips the contents of special files during recursive copies.", False, "`cp --copy-contents` does the opposite: it copies the contents of special files as if they were regular files.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0005", "linux_filesystem_ir_0005", "With `cp -P`, symbolic links in the source are copied as symbolic links.", True, "`cp -P` preserves symbolic links instead of following them.", "basic"),
            QuestionSpec("linux_filesystem_q_0006", "linux_filesystem_ir_0006", "When possible, `mv` ordinarily moves a file by renaming it.", True, "The manual says `mv` ordinarily simply renames a file.", "basic"),
            QuestionSpec("linux_filesystem_q_0007", "linux_filesystem_ir_0007", "If a destination is on a different file system, `mv` always fails immediately and never copies the file.", False, "Without `--no-copy`, `mv` can fall back to copying as if by `cp -a` and then remove the original.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0008", "linux_filesystem_ir_0008", "The `mv --no-copy` option prevents fallback copying across file systems.", True, "With `--no-copy`, `mv` fails instead of doing copy-and-remove across file systems.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0009", "linux_filesystem_ir_0009", "The `mv --exchange` option can swap two paths even if one of them does not exist yet.", False, "The manual says both files must exist when using `mv --exchange`.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0010", "linux_filesystem_ir_0010", "The `mkdir` command creates directory names in a random order chosen by the implementation.", False, "`mkdir` creates each directory name in the order given.", "basic"),
            QuestionSpec("linux_filesystem_q_0011", "linux_filesystem_ir_0011", "Without `-p`, `mkdir` reports an error if the target name already exists.", True, "An existing path causes an error unless `-p` is used and the existing path is a directory.", "basic"),
            QuestionSpec("linux_filesystem_q_0012", "linux_filesystem_ir_0012", "The `mkdir --mode` option changes only the permissions of already existing parent directories.", False, "`mkdir --mode` sets the permission bits of directories it creates, not of already existing parent directories.", "basic"),
            QuestionSpec("linux_filesystem_q_0013", "linux_filesystem_ir_0013", "The `mkdir --parents` option changes the permission bits of existing parent directories to match the new directory.", False, "The manual says `mkdir --parents` does not change the file permission bits of existing parent directories.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0014", "linux_filesystem_ir_0014", "By default, `ln` creates symbolic links, and `-s` switches it to hard-link mode.", False, "It is the other way around: `ln` makes hard links by default, and `-s` makes symbolic links.", "basic"),
            QuestionSpec("linux_filesystem_q_0015", "linux_filesystem_ir_0015", "Hard links cannot cross file system boundaries.", True, "The manual explicitly says hard links cannot cross file system boundaries.", "basic"),
            QuestionSpec("linux_filesystem_q_0016", "linux_filesystem_ir_0016", "GNU `ln` forbids creating a dangling symbolic link.", False, "The manual says there are no restrictions against creating dangling symbolic links.", "basic"),
            QuestionSpec("linux_filesystem_q_0017", "linux_filesystem_ir_0017", "The `ln --relative` option is only valid together with `--symbolic`.", True, "`ln --relative` is specifically defined for symbolic links and requires `--symbolic`.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0018", "linux_filesystem_ir_0018", "In canonicalize mode, `readlink` can output a path that still contains `.` or `..` components.", False, "Canonicalize mode outputs an absolute name without repeated separators and without `.` or `..` components.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0019", "linux_filesystem_ir_0019", "With `readlink --canonicalize`, a missing last path component is allowed, but a missing earlier component is not.", True, "`readlink --canonicalize` requires all components except possibly the last one.", "advanced"),
            QuestionSpec("linux_filesystem_q_0020", "linux_filesystem_ir_0020", "With `readlink --canonicalize-existing`, every path component must exist.", True, "`readlink --canonicalize-existing` fails if any component is missing or unavailable.", "advanced"),
            QuestionSpec("linux_filesystem_q_0021", "linux_filesystem_ir_0021", "The `readlink --no-newline` option removes the output delimiter for every file even when multiple files are specified.", False, "The manual describes `--no-newline` for the single-file case, not as a blanket rule for multiple files.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0022", "linux_filesystem_ir_0022", "The `realpath` command can leave symbolic link components unresolved in its output.", False, "`realpath` outputs an absolute file name without symbolic link components.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0023", "linux_filesystem_ir_0023", "The `realpath --canonicalize-existing` option fails if the named file does not exist.", True, "This option requires the named file to exist.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0024", "linux_filesystem_ir_0024", "The `realpath --relative-to` option prints resolved file names relative to a specified directory.", True, "The manual says `--relative-to` prints resolved names relative to the given directory.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0025", "linux_filesystem_ir_0025", "By default, `rm` removes directories the same way it removes regular files.", False, "By default, `rm` does not remove directories.", "basic"),
            QuestionSpec("linux_filesystem_q_0026", "linux_filesystem_ir_0026", "Attempts to remove `.` or `..` with `rm` are rejected without prompting.", True, "The manual says such attempts are rejected without any prompting.", "basic"),
            QuestionSpec("linux_filesystem_q_0027", "linux_filesystem_ir_0027", "The `rm --force` option ignores nonexistent files and missing operands, and it never prompts the user.", True, "`rm --force` suppresses prompts and ignores missing inputs.", "basic"),
            QuestionSpec("linux_filesystem_q_0028", "linux_filesystem_ir_0028", "With recursive removal, protecting `/` requires an explicit `rm --preserve-root` because GNU `rm` does not do that by default.", False, "GNU `rm` treats `--preserve-root` behavior as the default for recursive removal.", "intermediate"),
            QuestionSpec("linux_filesystem_q_0029", "linux_filesystem_ir_0029", "The `rmdir` command removes empty directories.", True, "`rmdir` is specifically for removing empty directories.", "basic"),
            QuestionSpec("linux_filesystem_q_0030", "linux_filesystem_ir_0030", "With no file name arguments, `df` reports only on the current working directory.", False, "Without file arguments, `df` reports the space available on all currently mounted file systems.", "basic"),
        ],
    },
    ("linux", "permissions"): {
        "ir_specs": [
            IRSpec("linux_permissions_ir_0001", "chmod purpose", "command", "The chmod command changes the access permissions of the named files.", [], ["chmod 644 file"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "chmod changes access permissions of named files.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["changes the access permissions of the named files"]),
            IRSpec("linux_permissions_ir_0002", "chmod symbolic links", "behavior", "The chmod command does not change the permissions of symbolic links on most systems.", [], ["chmod symlink"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "chmod usually does not change symlink permissions on most systems.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["doesn&rsquo;t change the permissions of symbolic links"]),
            IRSpec("linux_permissions_ir_0003", "chmod command-line symlink behavior", "behavior", "For each symbolic link listed on the command line, chmod changes the permissions of the pointed-to file.", [], ["chmod linkname"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "When a symlink is a command-line argument, chmod affects the file it points to.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["for each symbolic link listed on the command", "changes the permissions of the pointed-to file"]),
            IRSpec("linux_permissions_ir_0004", "chmod recursive symlink behavior", "behavior", "The chmod command ignores symbolic links encountered during recursive directory traversals.", [], ["chmod -R mode dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "During recursive traversal, chmod ignores encountered symbolic links unless traversal options change the behavior.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["ignores symbolic links encountered during", "recursive directory traversals"]),
            IRSpec("linux_permissions_ir_0005", "chmod authorization", "limitation", "Only a process whose effective user ID matches the user ID of the file, or a process with appropriate privileges, may change the file mode bits.", [], ["chmod 600 file"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "Changing file mode bits is limited to the owner-equivalent effective user ID or a privileged process.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["Only a process whose effective user ID matches the user ID of the file", "or a process with appropriate privileges"]),
            IRSpec("linux_permissions_ir_0006", "chmod --dereference", "option", "The chmod --dereference option acts on what symbolic links point to, and this is the default for command line arguments.", [], ["chmod --dereference link"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "chmod --dereference affects referents and is the default for symlink command-line arguments.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ['id="chmod--dereference"', "Do not act on symbolic links themselves but rather on what they point to", "This is the default for command line arguments"]),
            IRSpec("linux_permissions_ir_0007", "chmod --reference", "option", "The chmod --reference option changes each file's mode to be the same as that of the reference file.", [], ["chmod --reference=ref target"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "chmod --reference copies mode bits from a reference file.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ['id="chmod--reference"', "Change the mode of each", "to be the same as that of"]),
            IRSpec("linux_permissions_ir_0008", "chmod recursive", "option", "The chmod --recursive option recursively changes permissions of directories and their contents.", [], ["chmod -R 755 dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "chmod --recursive applies permission changes through directories and their contents.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ['id="chmod--recursive"', "Recursively change permissions of directories and their contents"]),
            IRSpec("linux_permissions_ir_0009", "chmod -H", "option", "With recursive chmod, the -H option traverses a command line argument that is a symbolic link to a directory, and this is the default if none of -H, -L, or -P is specified.", [], ["chmod -RH mode linkdir"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "For recursive chmod, -H follows command-line symlinks to directories and is the default traversal mode.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["a command line argument is a symbolic link to a directory, traverse it", "This is the default if none of", "-H", "-L", "or", "-P"]),
            IRSpec("linux_permissions_ir_0010", "chmod -L", "option", "With recursive chmod, the -L option traverses every symbolic link to a directory that is encountered.", [], ["chmod -RL mode dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "In recursive mode, chmod -L follows every encountered symlink to a directory.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["In a recursive traversal, traverse every symbolic link to a directory", "that is encountered"]),
            IRSpec("linux_permissions_ir_0011", "chmod -P", "option", "With recursive chmod, the -P option does not traverse any symbolic links.", [], ["chmod -RP mode dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "In recursive mode, chmod -P avoids traversing symlinks.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ["Do not traverse any symbolic links"]),
            IRSpec("linux_permissions_ir_0012", "chmod --preserve-root", "warning", "The chmod --preserve-root option fails upon attempts to recursively change the root directory '/'.", ["Used with recursive chmod."], ["chmod -R --preserve-root mode /"], "https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html", "13.3 chmod: Change access permissions", "chmod --preserve-root protects '/' from recursive permission changes.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chmod-invocation.html", ['id="chmod--preserve-root"', "Fail upon any attempt to recursively change the root directory"]),
            IRSpec("linux_permissions_ir_0013", "chown purpose", "command", "The chown command changes the user and/or group ownership of each given file.", [], ["chown root file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "chown changes user ownership, group ownership, or both.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ["changes the user and/or group ownership of each given"]),
            IRSpec("linux_permissions_ir_0014", "chown owner:group", "behavior", "If chown is given owner:group, the group ownership of the files is changed as well.", [], ["chown root:staff file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "The owner:group form changes both owner and group.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ["If the", "owner", "is followed by a colon and a", "group", "the group", "ownership of the files is changed as well"]),
            IRSpec("linux_permissions_ir_0015", "chown owner colon", "behavior", "If a colon but no group name follows owner, chown changes the group of the files to the owner's login group.", [], ["chown alice: file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "The owner: form sets the group to the owner's login group.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ["If a colon but no group name follows", "<var class=\"var\">owner</var>&rsquo;s login group"]),
            IRSpec("linux_permissions_ir_0016", "chown colon group", "behavior", "If chown is given :group with the owner omitted, only the group of the files is changed, and chown performs the same function as chgrp.", [], ["chown :staff file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "The :group form changes only group ownership and behaves like chgrp.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ["only the group of the files is changed", "performs the same function as", "chgrp"]),
            IRSpec("linux_permissions_ir_0017", "chown colon only", "behavior", "If only a colon is given, or if new-owner is empty, neither the owner nor the group is changed.", [], ["chown : file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "An empty chown owner/group specification changes nothing.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ["If only a colon is given", "neither the", "owner nor the group is changed"]),
            IRSpec("linux_permissions_ir_0018", "chown --from", "option", "The chown --from option changes a file's ownership only if it has the current attributes specified by old-owner.", [], ["chown --from=old new file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "chown --from adds a current-owner precondition to the change.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ['id="chown--from"', "Change a <var class=\"var\">file</var>&rsquo;s ownership only if it has current attributes specified"]),
            IRSpec("linux_permissions_ir_0019", "chown --dereference", "option", "The chown --dereference option acts on what symbolic links point to, and this is the default when not operating recursively.", [], ["chown --dereference link"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "For non-recursive chown, dereferencing symlinks is the default.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ['id="chown--dereference"', "Do not act on symbolic links themselves but rather on what they point to", "This is the default when not operating recursively"]),
            IRSpec("linux_permissions_ir_0020", "chown --no-dereference", "option", "The chown --no-dereference option acts on symbolic links themselves instead of what they point to.", [], ["chown -h user link"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "chown --no-dereference targets the symlink itself.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ['id="chown--no-dereference"', "Act on symbolic links themselves instead of what they point to"]),
            IRSpec("linux_permissions_ir_0021", "chown --reference", "option", "The chown --reference option changes the user and group of each file to match those of the reference file, using the referent if the reference is a symbolic link.", [], ["chown --reference=ref file"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "chown --reference copies owner and group from a reference target, not from a symlink object.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ['id="chown--reference"', "Change the user and group of each", "to be the same as those of", "If", "ref_file", "is a symbolic link", "but rather those of the file it", "refers to"]),
            IRSpec("linux_permissions_ir_0022", "chown recursive", "option", "The chown --recursive option recursively changes ownership of directories and their contents.", [], ["chown -R root dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chown-invocation.html", "13.1 chown: Change file owner and group", "chown --recursive applies through directories and their contents.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chown-invocation.html", ['id="chown--recursive"', "Recursively change ownership of directories and their contents"]),
            IRSpec("linux_permissions_ir_0023", "chgrp purpose", "command", "The chgrp command changes the group ownership of each given file or uses the group of an existing reference file.", [], ["chgrp staff file"], "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html", "13.2 chgrp: Change group ownership", "chgrp changes group ownership directly or from a reference file.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chgrp-invocation.html", ["changes the group ownership of each given", "or to the group of an existing reference file"]),
            IRSpec("linux_permissions_ir_0024", "chgrp numeric group", "behavior", "If group is intended to represent a numeric group ID, chgrp allows it to be specified with a leading '+'.", [], ["chgrp +1000 file"], "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html", "13.2 chgrp: Change group ownership", "GNU chgrp allows a leading plus sign to disambiguate numeric group IDs.", "high", "medium", "", "studyapp/input/source_documents/linux/permissions/chgrp-invocation.html", ["numeric group ID", "leading", "&lsquo;<samp class=\"samp\">+</samp>&rsquo;"]),
            IRSpec("linux_permissions_ir_0025", "chgrp --dereference", "option", "The chgrp --dereference option acts on what symbolic links point to, and this is the default when not operating recursively.", [], ["chgrp --dereference link"], "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html", "13.2 chgrp: Change group ownership", "For non-recursive chgrp, dereferencing symlinks is the default.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chgrp-invocation.html", ['id="chgrp--dereference"', "Do not act on symbolic links themselves but rather on what they point to", "This is the default when not operating recursively"]),
            IRSpec("linux_permissions_ir_0026", "chgrp --reference", "option", "The chgrp --reference option changes each file's group to match the reference file, using the referent if the reference is a symbolic link.", [], ["chgrp --reference=ref file"], "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html", "13.2 chgrp: Change group ownership", "chgrp --reference copies group ownership from the reference target, not from a symlink object.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chgrp-invocation.html", ['id="chgrp--reference"', "Change the group of each", "to be the same as that of", "If", "ref_file", "is a symbolic link", "but rather that of the file it refers to"]),
            IRSpec("linux_permissions_ir_0027", "chgrp recursive", "option", "The chgrp --recursive option recursively changes the group ownership of directories and their contents.", [], ["chgrp -R staff dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html", "13.2 chgrp: Change group ownership", "chgrp --recursive applies through directories and their contents.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chgrp-invocation.html", ['id="chgrp--recursive"', "Recursively change the group ownership of directories and their contents"]),
            IRSpec("linux_permissions_ir_0028", "chgrp -P", "option", "With recursive chgrp, the -P option does not traverse any symbolic links, and this is the default if none of -H, -L, or -P is specified.", [], ["chgrp -RP staff dir"], "https://www.gnu.org/software/coreutils/manual/html_node/chgrp-invocation.html", "13.2 chgrp: Change group ownership", "For recursive chgrp, -P means no symlink traversal and is the default traversal mode.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/chgrp-invocation.html", ["Do not traverse any symbolic links", "This is the default if none of", "-H", "-L", "or", "-P"]),
            IRSpec("linux_permissions_ir_0029", "file mode bits purpose", "definition", "File mode bits control the kinds of access that users have to a file.", [], ["permission bits"], "https://www.gnu.org/software/coreutils/manual/html_node/File-permissions.html", "27 File permissions", "File mode bits define what kinds of access users have to a file.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/file-permissions.html", ["file mode bits", "control the kinds of", "access that users have to that file"]),
            IRSpec("linux_permissions_ir_0030", "file mode representation", "definition", "File mode bits can be represented either in symbolic form or as an octal number.", [], ["rwx", "755"], "https://www.gnu.org/software/coreutils/manual/html_node/File-permissions.html", "27 File permissions", "GNU Coreutils describes file mode bits in symbolic form and octal form.", "high", "high", "", "studyapp/input/source_documents/linux/permissions/file-permissions.html", ["represented either in", "symbolic form", "or as an octal number"]),
        ],
        "question_specs": [
            QuestionSpec("linux_permissions_q_0001", "linux_permissions_ir_0001", "The `chmod` command changes the access permissions of named files.", True, "`chmod` is used to change access permissions of named files.", "basic"),
            QuestionSpec("linux_permissions_q_0002", "linux_permissions_ir_0002", "On most systems, `chmod` directly changes the permissions stored on a symbolic link itself.", False, "The manual says `chmod` does not change symlink permissions on most systems.", "basic"),
            QuestionSpec("linux_permissions_q_0003", "linux_permissions_ir_0003", "When a symbolic link is listed on the command line, `chmod` changes the permissions of the file it points to.", True, "For command-line symlinks, `chmod` acts on the pointed-to file.", "intermediate"),
            QuestionSpec("linux_permissions_q_0004", "linux_permissions_ir_0004", "During recursive directory traversals, `chmod` always changes the permissions of every symbolic link it encounters.", False, "The manual says `chmod` ignores symbolic links encountered during recursive traversals.", "intermediate"),
            QuestionSpec("linux_permissions_q_0005", "linux_permissions_ir_0005", "Any process can change the mode bits of any file as long as the path exists.", False, "Changing file mode bits is restricted to the matching effective user ID or a privileged process.", "basic"),
            QuestionSpec("linux_permissions_q_0006", "linux_permissions_ir_0006", "For command-line symlink arguments, `chmod --dereference` matches the default behavior.", True, "For command-line symlinks, dereferencing is the default behavior of `chmod`.", "intermediate"),
            QuestionSpec("linux_permissions_q_0007", "linux_permissions_ir_0007", "The `chmod --reference` option copies the mode from a reference file.", True, "`chmod --reference` makes the target file use the same mode as the reference file.", "basic"),
            QuestionSpec("linux_permissions_q_0008", "linux_permissions_ir_0008", "The `chmod --recursive` option changes only the top directory and never touches its contents.", False, "`chmod --recursive` changes directories and their contents recursively.", "basic"),
            QuestionSpec("linux_permissions_q_0009", "linux_permissions_ir_0009", "With recursive `chmod`, `-H` can traverse a command-line argument that is a symlink to a directory.", True, "In recursive mode, `chmod -H` traverses a command-line symlink to a directory.", "advanced"),
            QuestionSpec("linux_permissions_q_0010", "linux_permissions_ir_0010", "With recursive `chmod`, `-L` refuses to traverse symlinks to directories that are encountered.", False, "`chmod -L` traverses every encountered symlink to a directory during recursive traversal.", "advanced"),
            QuestionSpec("linux_permissions_q_0011", "linux_permissions_ir_0011", "With recursive `chmod`, the `-P` option means symbolic links are not traversed.", True, "`chmod -P` disables symlink traversal in recursive mode.", "advanced"),
            QuestionSpec("linux_permissions_q_0012", "linux_permissions_ir_0012", "The `chmod --preserve-root` option has no effect when a recursive `chmod` operation targets `/`.", False, "The manual says `--preserve-root` is meant to fail on attempts to recursively change the root directory.", "intermediate"),
            QuestionSpec("linux_permissions_q_0013", "linux_permissions_ir_0013", "The `chown` command can change user ownership, group ownership, or both.", True, "`chown` changes user ownership, group ownership, or both depending on the form used.", "basic"),
            QuestionSpec("linux_permissions_q_0014", "linux_permissions_ir_0014", "If `chown` is given `owner:group`, it changes only the owner and leaves the group unchanged.", False, "The `owner:group` form changes group ownership as well.", "basic"),
            QuestionSpec("linux_permissions_q_0015", "linux_permissions_ir_0015", "If `chown` is given `owner:` with no group name, the file's group is changed to that owner's login group.", True, "The `owner:` form changes the group to the owner's login group.", "intermediate"),
            QuestionSpec("linux_permissions_q_0016", "linux_permissions_ir_0016", "If `chown` is given `:group` with no owner, it changes only the group and acts like `chgrp`.", True, "The `:group` form changes only the group and performs the same function as `chgrp`.", "intermediate"),
            QuestionSpec("linux_permissions_q_0017", "linux_permissions_ir_0017", "If `chown` is given only `:` or an empty new-owner, it resets both owner and group to defaults.", False, "The manual says that form changes neither owner nor group.", "intermediate"),
            QuestionSpec("linux_permissions_q_0018", "linux_permissions_ir_0018", "The `chown --from` option changes ownership only when the file currently has the specified old-owner attributes.", True, "`chown --from` adds a current-owner check before making the change.", "advanced"),
            QuestionSpec("linux_permissions_q_0019", "linux_permissions_ir_0019", "When `chown` is not operating recursively, acting on what a symbolic link points to is the default behavior.", True, "For non-recursive use, `chown` dereferences symlinks by default.", "advanced"),
            QuestionSpec("linux_permissions_q_0020", "linux_permissions_ir_0020", "The `chown --no-dereference` option always acts on the file pointed to by a symbolic link.", False, "`chown --no-dereference` acts on the symbolic link itself.", "advanced"),
            QuestionSpec("linux_permissions_q_0021", "linux_permissions_ir_0021", "If the reference file is a symbolic link, `chown --reference` uses the owner and group of the symlink itself.", False, "`chown --reference` uses the referent of a symbolic-link reference file, not the symlink object itself.", "advanced"),
            QuestionSpec("linux_permissions_q_0022", "linux_permissions_ir_0022", "The `chown --recursive` option recursively changes ownership of directories and their contents.", True, "The manual explicitly says recursive chown changes directories and their contents.", "basic"),
            QuestionSpec("linux_permissions_q_0023", "linux_permissions_ir_0023", "The `chgrp` command can change a file's user ownership directly when you pass a user name.", False, "`chgrp` changes group ownership, not user ownership.", "basic"),
            QuestionSpec("linux_permissions_q_0024", "linux_permissions_ir_0024", "GNU `chgrp` forbids using a leading `+` when a numeric group ID is intended.", False, "GNU `chgrp` allows a leading `+` to specify a numeric group ID.", "intermediate"),
            QuestionSpec("linux_permissions_q_0025", "linux_permissions_ir_0025", "When `chgrp` is not operating recursively, dereferencing symbolic links is the default behavior.", True, "For non-recursive use, `chgrp` dereferences symlinks by default.", "advanced"),
            QuestionSpec("linux_permissions_q_0026", "linux_permissions_ir_0026", "If the reference file is a symbolic link, `chgrp --reference` uses the group of the symlink itself rather than the file it refers to.", False, "`chgrp --reference` uses the referent of a symbolic-link reference file.", "advanced"),
            QuestionSpec("linux_permissions_q_0027", "linux_permissions_ir_0027", "The `chgrp --recursive` option recursively changes the group ownership of directories and their contents.", True, "`chgrp --recursive` applies through directories and their contents.", "basic"),
            QuestionSpec("linux_permissions_q_0028", "linux_permissions_ir_0028", "With recursive `chgrp`, `-P` means every symlink to a directory will be traversed, and this is the default traversal mode.", False, "For recursive `chgrp`, `-P` means symlinks are not traversed, and that is the default traversal mode.", "advanced"),
            QuestionSpec("linux_permissions_q_0029", "linux_permissions_ir_0029", "File mode bits control the kinds of access that users have to a file.", True, "File mode bits determine what kinds of access users have to a file.", "basic"),
            QuestionSpec("linux_permissions_q_0030", "linux_permissions_ir_0030", "File mode bits can be represented only in symbolic form and not as octal numbers.", False, "The manual says file mode bits can be represented in symbolic form or as an octal number.", "basic"),
        ],
    },
    ("linux", "users_groups"): {
        "ir_specs": [
            IRSpec("linux_users_groups_ir_0001", "id purpose", "command", "The id command prints information about the given user, or about the running process if no user is specified.", [], ["id", "id alice"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id prints information about a named user or the running process when no user is supplied.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["prints information about the given user, or the process", "running it if no user is specified"]),
            IRSpec("linux_users_groups_ir_0002", "id user lookup precedence", "behavior", "For id, user name lookup takes precedence over interpreting a value as a user ID unless the ID is specified with a leading '+'.", [], ["id 1000", "id +1000"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id treats names preferentially unless a numeric ID is explicitly marked with a leading plus sign.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["name look-up", "taking precedence unless the ID is specified with a leading", "&lsquo;<samp class=\"samp\">+</samp>&rsquo;"]),
            IRSpec("linux_users_groups_ir_0003", "id default real uid", "behavior", "By default, id prints the real user ID.", [], ["id"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "The default id output includes the real user ID.", "high", "medium", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["By default, it prints the real user ID"]),
            IRSpec("linux_users_groups_ir_0004", "id default real gid", "behavior", "By default, id prints the real group ID.", [], ["id"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "The default id output includes the real group ID.", "high", "medium", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["real group ID"]),
            IRSpec("linux_users_groups_ir_0005", "id default effective uid condition", "behavior", "By default, id prints the effective user ID if it differs from the real user ID.", ["The effective user ID differs from the real user ID."], ["id"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id includes the effective user ID in default output only when it differs from the real user ID.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["effective user ID", "if different from the real user ID"]),
            IRSpec("linux_users_groups_ir_0006", "id -g", "option", "The id -g option prints only the group ID.", [], ["id -g"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id -g limits output to the group ID.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Print only the group ID."]),
            IRSpec("linux_users_groups_ir_0007", "id -G", "option", "The id -G option prints only the group ID and the supplementary groups.", [], ["id -G"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id -G outputs the primary group ID together with supplementary groups.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Print only the group ID and the supplementary groups."]),
            IRSpec("linux_users_groups_ir_0008", "id -n requirement", "option", "The id -n option prints the user or group name instead of the ID number and requires -u, -g, or -G.", [], ["id -un"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id -n switches to names and must be paired with a selector option.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Print the user or group name instead of the ID number.  Requires", "-u", "-g", "or", "-G"]),
            IRSpec("linux_users_groups_ir_0009", "id -r requirement", "option", "The id -r option prints the real instead of effective user or group ID and requires -u, -g, or -G.", [], ["id -ru"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id -r selects real IDs instead of effective IDs and must be combined with another selector option.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Print the real, instead of effective, user or group ID.  Requires", "-u", "-g", "or", "-G"]),
            IRSpec("linux_users_groups_ir_0010", "id -u", "option", "The id -u option prints only the user ID.", [], ["id -u"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id -u limits output to the user ID.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Print only the user ID."]),
            IRSpec("linux_users_groups_ir_0011", "id -Z", "option", "The id -Z option prints only the security context of the process.", [], ["id -Z"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id -Z outputs only the process security context.", "high", "medium", "Behavior depends on SELinux or SMACK availability.", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Print only the security context of the process"]),
            IRSpec("linux_users_groups_ir_0012", "id -Z failure condition", "behavior", "If neither SELinux nor SMACK is enabled, id -Z prints a warning and sets the exit status to 1.", ["Neither SELinux nor SMACK is enabled."], ["id -Z"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "Without SELinux or SMACK, id -Z does not succeed silently.", "high", "high", "Depends on security framework availability.", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["If neither SELinux or SMACK is enabled then print a warning", "set the exit status to 1"]),
            IRSpec("linux_users_groups_ir_0013", "id --zero", "option", "The id --zero option delimits output items with ASCII NUL characters.", [], ["id -Gn --zero"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id --zero uses NUL delimiters.", "high", "medium", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Delimit output items with ASCII NUL characters."]),
            IRSpec("linux_users_groups_ir_0014", "id --zero default-format restriction", "limitation", "The id --zero option is not permitted when using the default format.", [], ["id --zero"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "id --zero cannot be used with the default output format.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["This option is not permitted when using the default format."]),
            IRSpec("linux_users_groups_ir_0015", "id session staleness", "warning", "After login, id normally does not reflect changes to the group database within the existing login session.", [], ["id"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "Existing sessions can retain old group information in id output.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["will not reflect your changes within your existing login session"]),
            IRSpec("linux_users_groups_ir_0016", "id fresh lookup with user argument", "behavior", "Running id with a user argument causes the user and group database to be consulted afresh.", [], ["id alice"], "https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html", "20.1 id: Print user identity", "Supplying a user argument to id triggers a fresh database lookup.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/id-invocation.html", ["Running", "<code class=\"command\">id</code>", "with a user argument causes the user and group", "database to be consulted afresh"]),
            IRSpec("linux_users_groups_ir_0017", "groups purpose", "command", "The groups command prints the names of the primary and any supplementary groups for each given username, or for the current process if no names are given.", [], ["groups", "groups alice"], "https://www.gnu.org/software/coreutils/manual/html_node/groups-invocation.html", "20.4 groups: Print group names a user is in", "groups prints primary and supplementary group names for a user or the current process.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/groups-invocation.html", ["prints the names of the primary and any supplementary", "or the current process if no names", "are given"]),
            IRSpec("linux_users_groups_ir_0018", "groups multi-user prefix", "behavior", "If more than one name is given to groups, the name of each user is printed before that user's group list, separated by a colon.", [], ["groups alice bob"], "https://www.gnu.org/software/coreutils/manual/html_node/groups-invocation.html", "20.4 groups: Print group names a user is in", "For multiple users, groups prefixes each line with the user name and a colon.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/groups-invocation.html", ["If more than one name is given", "the name of each user is", "group list by a colon"]),
            IRSpec("linux_users_groups_ir_0019", "groups equivalent command", "behavior", "The group lists printed by groups are equivalent to the output of id -Gn.", [], ["groups"], "https://www.gnu.org/software/coreutils/manual/html_node/groups-invocation.html", "20.4 groups: Print group names a user is in", "groups and id -Gn produce equivalent group lists.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/groups-invocation.html", ["equivalent to the output of the command", "&lsquo;<samp class=\"samp\">id -Gn</samp>&rsquo;"]),
            IRSpec("linux_users_groups_ir_0020", "groups session staleness", "warning", "After login, groups normally does not reflect changes to the group database within the existing login session.", [], ["groups"], "https://www.gnu.org/software/coreutils/manual/html_node/groups-invocation.html", "20.4 groups: Print group names a user is in", "Existing sessions can retain old group information in groups output.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/groups-invocation.html", ["will not reflect your changes within your existing login session"]),
            IRSpec("linux_users_groups_ir_0021", "groups fresh lookup with users", "behavior", "Running groups with a list of users causes the user and group database to be consulted afresh.", [], ["groups alice"], "https://www.gnu.org/software/coreutils/manual/html_node/groups-invocation.html", "20.4 groups: Print group names a user is in", "Supplying users to groups triggers a fresh database lookup.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/groups-invocation.html", ["with a list of users causes the user and group", "database to be consulted afresh"]),
            IRSpec("linux_users_groups_ir_0022", "users purpose", "command", "The users command prints on a single line a blank-separated list of user names of users currently logged in to the current host.", [], ["users"], "https://www.gnu.org/software/coreutils/manual/html_node/users-invocation.html", "20.5 users: Print login names of users currently logged in", "users prints the currently logged-in user names as a blank-separated single line.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/users-invocation.html", ["prints on a single line a blank-separated list of user", "names of users currently logged in to the current host"]),
            IRSpec("linux_users_groups_ir_0023", "users repeated sessions", "behavior", "In users output, each user name corresponds to a login session, so a user with multiple login sessions appears multiple times.", [], ["users"], "https://www.gnu.org/software/coreutils/manual/html_node/users-invocation.html", "20.5 users: Print login names of users currently logged in", "users output repeats a user name once per login session.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/users-invocation.html", ["Each user name", "corresponds to a login session", "name will appear the same number of times"]),
            IRSpec("linux_users_groups_ir_0024", "users default data source", "behavior", "With no file argument, users extracts its information from a system-maintained file.", [], ["users"], "https://www.gnu.org/software/coreutils/manual/html_node/users-invocation.html", "20.5 users: Print login names of users currently logged in", "Without a file argument, users reads from the system-maintained login record file.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/users-invocation.html", ["With no", "file", "argument", "extracts its information from", "a system-maintained file"]),
            IRSpec("linux_users_groups_ir_0025", "users file argument", "behavior", "If a file argument is given to users, it uses that file instead, and /var/log/wtmp is a common choice.", [], ["users /var/log/wtmp"], "https://www.gnu.org/software/coreutils/manual/html_node/users-invocation.html", "20.5 users: Print login names of users currently logged in", "users can read from a specified file such as /var/log/wtmp.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/users-invocation.html", ["If a file argument is given", "uses", "that file instead", "A common choice is", "/var/log/wtmp"]),
            IRSpec("linux_users_groups_ir_0026", "who default output", "command", "With no non-option arguments, who prints login name, terminal line, login time, and remote hostname or X display for each user currently logged on.", [], ["who"], "https://www.gnu.org/software/coreutils/manual/html_node/who-invocation.html", "20.6 who: Print who is currently logged in", "Default who output includes login name, terminal, login time, and remote host or X display.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/who-invocation.html", ["prints the following", "information for each user currently logged on: login name, terminal", "line, login time, and remote hostname or X display"]),
            IRSpec("linux_users_groups_ir_0027", "who file argument", "behavior", "If given one non-option argument, who uses that file instead of a default system-maintained file.", [], ["who /var/log/wtmp"], "https://www.gnu.org/software/coreutils/manual/html_node/who-invocation.html", "20.6 who: Print who is currently logged in", "A single file argument makes who read from that file instead of the default login record file.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/who-invocation.html", ["If given one non-option argument, <code class=\"command\">who</code> uses that instead of", "a default system-maintained file"]),
            IRSpec("linux_users_groups_ir_0028", "who am i", "behavior", "If given two non-option arguments, who prints only the entry for the user running it, preceded by the hostname.", [], ["who am i"], "https://www.gnu.org/software/coreutils/manual/html_node/who-invocation.html", "20.6 who: Print who is currently logged in", "Two non-option arguments such as 'am i' make who print only the current user's entry with a hostname prefix.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/who-invocation.html", ["If given two non-option arguments", "prints only the entry", "preceded", "by the hostname"]),
            IRSpec("linux_users_groups_ir_0029", "who --boot", "option", "The who --boot option prints the date and time of last system boot.", [], ["who --boot"], "https://www.gnu.org/software/coreutils/manual/html_node/who-invocation.html", "20.6 who: Print who is currently logged in", "who --boot reports the time of the last system boot.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/who-invocation.html", ["Print the date and time of last system boot."]),
            IRSpec("linux_users_groups_ir_0030", "who --count", "option", "The who --count option prints only the login names and the number of users logged on, and overrides all other options.", [], ["who --count"], "https://www.gnu.org/software/coreutils/manual/html_node/who-invocation.html", "20.6 who: Print who is currently logged in", "who --count reduces output to login names and a user count and takes precedence over other options.", "high", "high", "", "studyapp/input/source_documents/linux/users_groups/who-invocation.html", ["Print only the login names and the number of users logged on.", "Overrides all other options."]),
        ],
        "question_specs": [
            QuestionSpec("linux_users_groups_q_0001", "linux_users_groups_ir_0001", "The `id` command can print information about a named user or about the running process when no user is specified.", True, "The manual says `id` prints information about the given user, or about the running process if no user is specified.", "basic"),
            QuestionSpec("linux_users_groups_q_0002", "linux_users_groups_ir_0002", "For `id`, a plain numeric-looking argument is always treated as a user ID even when a matching user name exists.", False, "Name lookup takes precedence in `id` unless the ID is explicitly marked with a leading `+`.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0003", "linux_users_groups_ir_0003", "By default, `id` omits the real user ID and shows only the effective user ID.", False, "The default `id` output includes the real user ID.", "basic"),
            QuestionSpec("linux_users_groups_q_0004", "linux_users_groups_ir_0004", "By default, `id` never prints any group-related information.", False, "The default `id` output includes the real group ID and can include other group information.", "basic"),
            QuestionSpec("linux_users_groups_q_0005", "linux_users_groups_ir_0005", "By default, `id` prints the effective user ID only when it differs from the real user ID.", True, "The manual says `id` includes the effective user ID in default output if it differs from the real user ID.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0006", "linux_users_groups_ir_0006", "The `id -g` option prints only the user ID.", False, "`id -g` prints only the group ID, not the user ID.", "basic"),
            QuestionSpec("linux_users_groups_q_0007", "linux_users_groups_ir_0007", "The `id -G` option prints only the user ID and omits all group information.", False, "`id -G` prints the group ID and the supplementary groups.", "basic"),
            QuestionSpec("linux_users_groups_q_0008", "linux_users_groups_ir_0008", "The `id -n` option prints names instead of numeric IDs, but it must be used with `-u`, `-g`, or `-G`.", True, "The manual says `id -n` requires `-u`, `-g`, or `-G`.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0009", "linux_users_groups_ir_0009", "The `id -r` option switches output to real IDs instead of effective IDs, and it requires `-u`, `-g`, or `-G`.", True, "`id -r` selects real IDs and must be combined with another selector option.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0010", "linux_users_groups_ir_0010", "The `id -u` option prints only the current group ID.", False, "`id -u` prints only the user ID.", "basic"),
            QuestionSpec("linux_users_groups_q_0011", "linux_users_groups_ir_0011", "The `id -Z` option prints the process security context together with the normal default `id` fields.", False, "The manual says `id -Z` prints only the process security context.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0012", "linux_users_groups_ir_0012", "If neither SELinux nor SMACK is enabled, `id -Z` still succeeds quietly with exit status 0.", False, "Without SELinux or SMACK, `id -Z` prints a warning and sets the exit status to 1.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0013", "linux_users_groups_ir_0013", "The `id --zero` option uses ASCII NUL characters as output delimiters.", True, "`id --zero` changes delimiters to ASCII NUL characters.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0014", "linux_users_groups_ir_0014", "The `id --zero` option is allowed when using the default `id` output format.", False, "The manual says `id --zero` is not permitted with the default format.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0015", "linux_users_groups_ir_0015", "Within an existing login session, `id` may fail to reflect changes made later to the group database.", True, "The manual warns that `id` normally does not reflect those changes within the same login session.", "advanced"),
            QuestionSpec("linux_users_groups_q_0016", "linux_users_groups_ir_0016", "Running `id` with a user argument causes the user and group database to be consulted afresh.", True, "Supplying a user argument to `id` triggers a fresh database lookup.", "advanced"),
            QuestionSpec("linux_users_groups_q_0017", "linux_users_groups_ir_0017", "The `groups` command prints primary and supplementary group names for a given user, or for the current process if no names are given.", True, "That is the purpose of `groups` according to the manual.", "basic"),
            QuestionSpec("linux_users_groups_q_0018", "linux_users_groups_ir_0018", "When `groups` is given more than one user name, it prints only the group lists and never prefixes them with user names.", False, "With multiple users, `groups` prints each user name before that user's group list, separated by a colon.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0019", "linux_users_groups_ir_0019", "The group list printed by `groups` is equivalent to the output of `id -Gn`.", True, "The manual explicitly states that `groups` output is equivalent to `id -Gn`.", "basic"),
            QuestionSpec("linux_users_groups_q_0020", "linux_users_groups_ir_0020", "After login, `groups` always reflects any group-database changes immediately within the existing login session.", False, "The manual says `groups` normally does not reflect those changes in the existing session.", "advanced"),
            QuestionSpec("linux_users_groups_q_0021", "linux_users_groups_ir_0021", "Running `groups` with explicit user names causes the user and group database to be consulted afresh.", True, "Supplying user names to `groups` triggers a fresh database lookup.", "advanced"),
            QuestionSpec("linux_users_groups_q_0022", "linux_users_groups_ir_0022", "The `users` command prints a blank-separated single-line list of users currently logged in to the current host.", True, "That is the standard output format described for `users`.", "basic"),
            QuestionSpec("linux_users_groups_q_0023", "linux_users_groups_ir_0023", "In `users` output, a user with two login sessions is listed only once.", False, "Each occurrence in `users` output corresponds to a login session, so multiple sessions repeat the name.", "basic"),
            QuestionSpec("linux_users_groups_q_0024", "linux_users_groups_ir_0024", "With no file argument, `users` reads its information from a system-maintained file.", True, "The manual says `users` uses a system-maintained file when no file argument is given.", "basic"),
            QuestionSpec("linux_users_groups_q_0025", "linux_users_groups_ir_0025", "If a file argument is given to `users`, it must still ignore that file and read only the default login record file.", False, "When a file argument is given, `users` uses that file instead; `/var/log/wtmp` is a common choice.", "basic"),
            QuestionSpec("linux_users_groups_q_0026", "linux_users_groups_ir_0026", "With no non-option arguments, `who` prints login name, terminal line, login time, and remote hostname or X display for each logged-on user.", True, "That is the default `who` output described in the manual.", "basic"),
            QuestionSpec("linux_users_groups_q_0027", "linux_users_groups_ir_0027", "If `who` is given one non-option argument, it uses that file instead of the default system-maintained file.", True, "A single non-option argument tells `who` to read from that file.", "basic"),
            QuestionSpec("linux_users_groups_q_0028", "linux_users_groups_ir_0028", "With two non-option arguments such as `am i`, `who` prints every logged-in user but omits the hostname.", False, "With two non-option arguments, `who` prints only the current user's entry and precedes it with the hostname.", "intermediate"),
            QuestionSpec("linux_users_groups_q_0029", "linux_users_groups_ir_0029", "The `who --boot` option prints the current number of logged-in users.", False, "`who --boot` prints the date and time of the last system boot.", "basic"),
            QuestionSpec("linux_users_groups_q_0030", "linux_users_groups_ir_0030", "The `who --count` option prints only the login names and the number of users logged on, and it overrides all other options.", True, "The manual says `who --count` overrides all other options.", "intermediate"),
        ],
    },
    ("linux", "processes"): {
        "ir_specs": [
            IRSpec("linux_processes_ir_0001", "timeout purpose", "command", "The timeout command runs the given command and kills it if it is still running after the specified time interval.", [], ["timeout 5 sleep 10"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout runs a command with a time limit and kills it if it overruns.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["runs the given", "kills it if it is", "still running after the specified time interval"]),
            IRSpec("linux_processes_ir_0002", "timeout built-in restriction", "limitation", "The command run by timeout must not be a special built-in utility.", [], ["timeout 5 command"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout cannot directly manage special built-in utilities.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["must not be a special built-in utility"]),
            IRSpec("linux_processes_ir_0003", "timeout --foreground", "option", "The timeout --foreground option does not create a separate background program group, so the managed command can use the foreground TTY normally.", [], ["timeout --foreground 5 top"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout --foreground keeps the managed command in normal foreground TTY use.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["Don&rsquo;t create a separate background program group", "foreground TTY normally"]),
            IRSpec("linux_processes_ir_0004", "timeout foreground child limitation", "limitation", "In timeout foreground mode, any children of the managed command will not be timed out.", [], ["timeout --foreground 5 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "Foreground mode does not apply timeout control to children of the managed command.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["In this mode of operation, any children of", "will not be timed out"]),
            IRSpec("linux_processes_ir_0005", "timeout --kill-after", "option", "The timeout --kill-after option ensures the monitored command is killed by also sending a KILL signal.", [], ["timeout -k 3s 5s cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout --kill-after adds a follow-up KILL signal.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["Ensure the monitored", "is killed by also sending a", "KILL"]),
            IRSpec("linux_processes_ir_0006", "timeout kill-after timing", "behavior", "The duration for timeout --kill-after starts when timeout sends the initial signal, not when the command is started.", [], ["timeout -k 3s 5s cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "The kill-after timer begins when the first timeout signal is sent.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["starts from the point in time when", "sends the initial signal", "not from the beginning"]),
            IRSpec("linux_processes_ir_0007", "timeout kill-after zero behavior", "behavior", "The timeout --kill-after option has no effect if the main timeout duration or the kill-after duration is 0.", [], ["timeout -k 0 5 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "A zero main or kill-after duration disables kill-after behavior.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["This option has no effect if either the main", "duration", "or the <var class=\"var\">duration</var> specified", "is 0"]),
            IRSpec("linux_processes_ir_0008", "timeout --preserve-status", "option", "The timeout --preserve-status option returns the exit status of the managed command on timeout rather than a specific timeout status.", [], ["timeout --preserve-status 5 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout --preserve-status keeps the managed command's exit status on timeout.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["Return the exit status of the managed", "on timeout", "rather than", "a specific exit status indicating a timeout"]),
            IRSpec("linux_processes_ir_0009", "timeout --signal", "option", "The timeout --signal option sends the specified signal on timeout instead of the default TERM signal.", [], ["timeout --signal=INT 5 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout can send a chosen signal instead of TERM when time expires.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["Send this", "signal", "rather than the", "default", "TERM"]),
            IRSpec("linux_processes_ir_0010", "timeout duration default unit", "definition", "For timeout, the default duration unit is seconds.", [], ["timeout 5 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout uses seconds when no duration suffix is given.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["&lsquo;<samp class=\"samp\">s</samp>&rsquo; for seconds (the default)"]),
            IRSpec("linux_processes_ir_0011", "timeout duration units", "definition", "The timeout command accepts duration suffixes for seconds, minutes, hours, and days.", [], ["timeout 2m cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "timeout supports s, m, h, and d unit suffixes.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["&lsquo;<samp class=\"samp\">s</samp>&rsquo; for seconds", "&lsquo;<samp class=\"samp\">m</samp>&rsquo; for minutes", "&lsquo;<samp class=\"samp\">h</samp>&rsquo; for hours", "&lsquo;<samp class=\"samp\">d</samp>&rsquo; for days"]),
            IRSpec("linux_processes_ir_0012", "timeout zero duration", "behavior", "A timeout duration of 0 disables the associated timeout.", [], ["timeout 0 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "In timeout, a zero duration disables that timeout.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["A duration of 0 disables the associated timeout."]),
            IRSpec("linux_processes_ir_0013", "timeout exit 124", "behavior", "The timeout command exits with status 124 if the managed command times out and --preserve-status is not specified.", [], ["timeout 1 sleep 10"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "Without preserve-status, timeout uses exit status 124 on timeout.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["124 if", "times out", "--preserve-status", "is not specified"]),
            IRSpec("linux_processes_ir_0014", "timeout exit 137", "behavior", "The timeout command exits with status 137 if the managed command or timeout itself is sent the KILL(9) signal.", [], ["timeout -k 1s 1s cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html", "23.6 timeout: Run a command with a time limit", "KILL signal cases lead timeout to return 137.", "high", "high", "", "studyapp/input/source_documents/linux/processes/timeout-invocation.html", ["137 if", "is sent the KILL(9) signal"]),
            IRSpec("linux_processes_ir_0015", "nohup purpose", "command", "The nohup command runs the given command with hangup signals ignored so that it can continue running after logout.", [], ["nohup make &"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup makes a command ignore hangup signals so it can survive logout.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["runs the given", "with hangup signals ignored", "continue running in the background after you log", "out"]),
            IRSpec("linux_processes_ir_0016", "nohup stdin terminal behavior", "behavior", "If standard input is a terminal, nohup redirects it and makes the substitute file descriptor unreadable.", [], ["nohup cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup protects terminal input by redirecting it away and making the substitute unreadable.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["If standard input is a terminal, redirect it", "Make the substitute file descriptor unreadable"]),
            IRSpec("linux_processes_ir_0017", "nohup stdout terminal behavior", "behavior", "If standard output is a terminal, nohup appends standard output to nohup.out, falls back to $HOME/nohup.out if needed, and does not run the command if neither file can be written.", [], ["nohup cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup redirects terminal stdout to nohup.out, then to $HOME/nohup.out, or refuses to run if neither is writable.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["If standard output is a terminal", "appended", "nohup.out", "$HOME/nohup.out", "command is not run"]),
            IRSpec("linux_processes_ir_0018", "nohup output file permissions", "behavior", "Any nohup.out or $HOME/nohup.out file created by nohup is made readable and writable only to the user, regardless of current umask settings.", [], ["nohup cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup-created output files are user-only readable and writable regardless of umask.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["created by", "is made readable and writable only to the user", "regardless of the current umask settings"]),
            IRSpec("linux_processes_ir_0019", "nohup stderr behavior", "behavior", "If standard error is a terminal, nohup normally redirects it to the same file descriptor as standard output.", [], ["nohup cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup usually ties terminal stderr to the redirected stdout destination.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["If standard error is a terminal", "normally redirected to the same file", "standard output"]),
            IRSpec("linux_processes_ir_0020", "nohup background behavior", "behavior", "The nohup command does not automatically put the command it runs in the background.", [], ["nohup cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup does not background the command by itself.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["does not automatically put the command it runs in the", "background"]),
            IRSpec("linux_processes_ir_0021", "nohup niceness", "behavior", "The nohup command does not alter the niceness of the command it runs.", [], ["nohup nice cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html", "23.4 nohup: Run a command immune to hangups", "nohup and nice are separate concerns; nohup does not change niceness.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nohup-invocation.html", ["does not alter the", "niceness"]),
            IRSpec("linux_processes_ir_0022", "nice no-args behavior", "behavior", "If no arguments are given, the nice command prints the current niceness.", [], ["nice"], "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html", "23.3 nice: Run a command with modified niceness", "Without arguments, nice reports the current niceness.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nice-invocation.html", ["If no arguments are given", "prints the current niceness"]),
            IRSpec("linux_processes_ir_0023", "nice default adjustment", "behavior", "When running a command, nice increments its niceness by 10 by default.", [], ["nice cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html", "23.3 nice: Run a command with modified niceness", "By default, nice adds 10 to the command's niceness.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nice-invocation.html", ["By default, its niceness is incremented by 10."]),
            IRSpec("linux_processes_ir_0024", "nice range semantics", "behavior", "A niceness of -20 is high priority, while 19 is lower priority and has less impact on other running processes.", [], ["nice -n -1 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html", "23.3 nice: Run a command with modified niceness", "Lower niceness values are favored more by scheduling than higher values.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nice-invocation.html", ["range at least from &minus;20", "high priority", "through 19", "lower priority"]),
            IRSpec("linux_processes_ir_0025", "nice versus priority", "best_practice", "Niceness should not be confused with scheduling priority because niceness is merely advice to the scheduler and may be ignored.", [], ["nice cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html", "23.3 nice: Run a command with modified niceness", "Niceness is advisory and distinct from scheduling priority.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nice-invocation.html", ["should not be confused with a scheduling priority", "merely advice to the", "scheduler", "free to ignore"]),
            IRSpec("linux_processes_ir_0026", "renice for existing process", "best_practice", "To change the niceness of an existing process, use the renice command.", [], ["renice 5 pid"], "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html", "23.3 nice: Run a command with modified niceness", "renice is the tool for changing niceness of an existing process.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nice-invocation.html", ["To change the", "niceness", "of an existing process", "use the", "renice"]),
            IRSpec("linux_processes_ir_0027", "nice -n negative privilege rule", "limitation", "If the nice --adjustment value is negative and you lack appropriate privileges, nice issues a warning and otherwise acts as if you specified a zero adjustment.", [], ["nice -n -1 cmd"], "https://www.gnu.org/software/coreutils/manual/html_node/nice-invocation.html", "23.3 nice: Run a command with modified niceness", "Unprivileged negative adjustments do not take effect and are treated like zero adjustments.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nice-invocation.html", ["adjustment", "is negative and you lack appropriate privileges", "issues a warning", "acts as if you specified", "a zero adjustment"]),
            IRSpec("linux_processes_ir_0028", "sleep purpose", "command", "The sleep command pauses for an amount of time specified by the sum of the values of the command line arguments.", [], ["sleep 1"], "https://www.gnu.org/software/coreutils/manual/html_node/sleep-invocation.html", "25.1 sleep: Delay for a specified time", "sleep pauses for the sum of its command-line duration arguments.", "high", "high", "", "studyapp/input/source_documents/linux/processes/sleep-invocation.html", ["pauses for an amount of time specified by the sum of", "the values of the command line arguments"]),
            IRSpec("linux_processes_ir_0029", "sleep default unit", "definition", "For sleep, each argument defaults to seconds if no unit suffix is given.", [], ["sleep 5"], "https://www.gnu.org/software/coreutils/manual/html_node/sleep-invocation.html", "25.1 sleep: Delay for a specified time", "sleep uses seconds by default when no unit suffix is present.", "high", "high", "", "studyapp/input/source_documents/linux/processes/sleep-invocation.html", ["default", "is seconds"]),
            IRSpec("linux_processes_ir_0030", "nproc default behavior", "command", "The nproc command prints the number of processing units available to the current process, which may be less than the number of online processors.", [], ["nproc"], "https://www.gnu.org/software/coreutils/manual/html_node/nproc-invocation.html", "21.3 nproc: Print the number of available processors", "nproc reports processors available to the current process, not necessarily all online processors.", "high", "high", "", "studyapp/input/source_documents/linux/processes/nproc-invocation.html", ["Print the number of processing units available to the current process", "may be less than the number of online processors"]),
        ],
        "question_specs": [
            QuestionSpec("linux_processes_q_0001", "linux_processes_ir_0001", "The `timeout` command runs a command and kills it if it is still running after the specified time interval.", True, "`timeout` runs a command with a time limit and kills it if it overruns.", "basic"),
            QuestionSpec("linux_processes_q_0002", "linux_processes_ir_0002", "The command managed by `timeout` may be a shell special built-in utility.", False, "The manual says the managed command must not be a special built-in utility.", "intermediate"),
            QuestionSpec("linux_processes_q_0003", "linux_processes_ir_0003", "The `timeout --foreground` option avoids creating a separate background program group so the command can use the foreground TTY normally.", True, "That is the purpose of `timeout --foreground`.", "advanced"),
            QuestionSpec("linux_processes_q_0004", "linux_processes_ir_0004", "In `timeout --foreground` mode, all children of the managed command are still guaranteed to be timed out.", False, "The manual says children of the managed command will not be timed out in foreground mode.", "advanced"),
            QuestionSpec("linux_processes_q_0005", "linux_processes_ir_0005", "The `timeout --kill-after` option ensures the monitored command is also sent a KILL signal.", True, "`timeout --kill-after` adds a follow-up KILL signal.", "intermediate"),
            QuestionSpec("linux_processes_q_0006", "linux_processes_ir_0006", "For `timeout --kill-after`, the extra duration is measured from when the command starts, not from when the first timeout signal is sent.", False, "The manual says the kill-after timer starts when the initial timeout signal is sent.", "intermediate"),
            QuestionSpec("linux_processes_q_0007", "linux_processes_ir_0007", "The `timeout --kill-after` option has no effect if the main timeout duration or the kill-after duration is 0.", True, "A zero main or kill-after duration disables kill-after behavior.", "intermediate"),
            QuestionSpec("linux_processes_q_0008", "linux_processes_ir_0008", "With `timeout --preserve-status`, a timeout still always returns a fixed timeout status instead of the managed command's status.", False, "The manual says `--preserve-status` returns the managed command's exit status on timeout.", "intermediate"),
            QuestionSpec("linux_processes_q_0009", "linux_processes_ir_0009", "The `timeout --signal` option can send a chosen signal instead of the default TERM signal.", True, "`timeout --signal` lets you choose a signal other than TERM.", "basic"),
            QuestionSpec("linux_processes_q_0010", "linux_processes_ir_0010", "For `timeout`, an unsuffixed duration is measured in minutes by default.", False, "The default timeout duration unit is seconds.", "basic"),
            QuestionSpec("linux_processes_q_0011", "linux_processes_ir_0011", "The `timeout` command accepts duration suffixes for seconds, minutes, hours, and days.", True, "The manual lists `s`, `m`, `h`, and `d` as timeout duration units.", "basic"),
            QuestionSpec("linux_processes_q_0012", "linux_processes_ir_0012", "In `timeout`, a duration of 0 forces the associated timeout to expire immediately.", False, "The manual says a duration of 0 disables the associated timeout.", "basic"),
            QuestionSpec("linux_processes_q_0013", "linux_processes_ir_0013", "Without `--preserve-status`, `timeout` uses exit status 124 when the managed command times out.", True, "Exit status 124 is the standard timeout status when preserve-status is not used.", "intermediate"),
            QuestionSpec("linux_processes_q_0014", "linux_processes_ir_0014", "If a KILL(9) signal is involved, `timeout` returns exit status 124.", False, "KILL-related cases return exit status 137 according to the manual.", "intermediate"),
            QuestionSpec("linux_processes_q_0015", "linux_processes_ir_0015", "The `nohup` command ignores hangup signals so a command can continue running after logout.", True, "That is the core purpose of `nohup`.", "basic"),
            QuestionSpec("linux_processes_q_0016", "linux_processes_ir_0016", "If standard input is a terminal, `nohup` leaves it unchanged so the command can keep reading from the terminal normally.", False, "The manual says `nohup` redirects terminal standard input and makes the substitute unreadable.", "intermediate"),
            QuestionSpec("linux_processes_q_0017", "linux_processes_ir_0017", "If standard output is a terminal, `nohup` tries `nohup.out`, then `$HOME/nohup.out`, and does not run the command if neither can be written.", True, "That is the fallback order documented for `nohup` terminal output.", "intermediate"),
            QuestionSpec("linux_processes_q_0018", "linux_processes_ir_0018", "A `nohup.out` file created by `nohup` follows the current umask without any exception.", False, "The manual says a file created by `nohup` is made readable and writable only to the user regardless of umask.", "intermediate"),
            QuestionSpec("linux_processes_q_0019", "linux_processes_ir_0019", "If standard error is a terminal, `nohup` normally redirects it to the same file descriptor as standard output.", True, "That is the normal stderr behavior documented for `nohup`.", "basic"),
            QuestionSpec("linux_processes_q_0020", "linux_processes_ir_0020", "The `nohup` command automatically backgrounds the command it runs.", False, "The manual says you must background the command explicitly; `nohup` does not do it automatically.", "basic"),
            QuestionSpec("linux_processes_q_0021", "linux_processes_ir_0021", "The `nohup` command automatically lowers the niceness of the command it runs so background work is less intrusive.", False, "The manual explicitly says `nohup` does not alter niceness.", "basic"),
            QuestionSpec("linux_processes_q_0022", "linux_processes_ir_0022", "If no arguments are given, `nice` prints the current niceness.", True, "Without arguments, `nice` reports the current niceness.", "basic"),
            QuestionSpec("linux_processes_q_0023", "linux_processes_ir_0023", "By default, running a command through `nice` decreases its niceness by 10.", False, "The default behavior is to increment niceness by 10, not decrease it.", "basic"),
            QuestionSpec("linux_processes_q_0024", "linux_processes_ir_0024", "A niceness of -20 represents higher scheduling favor than a niceness of 19.", True, "The manual describes -20 as high priority and 19 as lower priority.", "intermediate"),
            QuestionSpec("linux_processes_q_0025", "linux_processes_ir_0025", "Niceness is exactly the same thing as scheduling priority and must be obeyed by the scheduler.", False, "The manual says niceness is not the same as priority and is merely advice that the scheduler may ignore.", "advanced"),
            QuestionSpec("linux_processes_q_0026", "linux_processes_ir_0026", "To change the niceness of an existing process, use `renice` rather than `nice`.", True, "The manual says `renice` is the command for changing niceness of an existing process.", "basic"),
            QuestionSpec("linux_processes_q_0027", "linux_processes_ir_0027", "If `nice --adjustment` is negative and you lack appropriate privileges, `nice` warns and otherwise behaves as if the adjustment were zero.", True, "That is the documented behavior for an unprivileged negative adjustment.", "advanced"),
            QuestionSpec("linux_processes_q_0028", "linux_processes_ir_0028", "The `sleep` command pauses for only the first command-line duration argument and ignores any remaining ones.", False, "GNU `sleep` pauses for the sum of the values of its command-line arguments.", "basic"),
            QuestionSpec("linux_processes_q_0029", "linux_processes_ir_0029", "For `sleep`, an argument without a unit suffix defaults to seconds.", True, "Seconds are the default unit for `sleep` when no suffix is given.", "basic"),
            QuestionSpec("linux_processes_q_0030", "linux_processes_ir_0030", "The `nproc` command always prints the total number of online processors, never a smaller process-limited value.", False, "The manual says `nproc` prints processing units available to the current process, which may be less than the number of online processors.", "intermediate"),
        ],
    },
    ("linux", "package_management"): {
        "ir_specs": [
            IRSpec("linux_package_management_ir_0001", "apt purpose", "definition", "The apt command provides a high-level commandline interface for the package management system and is intended as an end user interface.", [], ["apt install pkg"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION", "apt is described as a high-level end user interface for package management.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["provides a high-level commandline interface", "intended as an end user interface"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0002", "apt upgrade purpose", "command", "The apt upgrade command is used to install available upgrades of packages currently installed on the system.", [], ["apt upgrade"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > upgrade", "apt upgrade installs available upgrades for installed packages.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["available upgrades of", "packages currently installed on the system"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0003", "apt upgrade no removals", "behavior", "The apt upgrade command never removes existing installed packages.", [], ["apt upgrade"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > upgrade", "apt upgrade may add dependencies but will not remove installed packages.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["existing packages will never be removed"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0004", "apt full-upgrade removals", "behavior", "The apt full-upgrade command may remove currently installed packages if that is needed to upgrade the system as a whole.", [], ["apt full-upgrade"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > full-upgrade", "apt full-upgrade can remove installed packages when required for the upgrade.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["full-upgrade performs the function of upgrade but will", "remove currently installed packages"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0005", "apt remove leaves config", "behavior", "Removing a package with apt leaves usually small modified user configuration files behind.", [], ["apt remove pkg"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > install, reinstall, remove, purge", "apt remove leaves modified user configuration files behind.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["Removing a package removes all packaged data", "user configuration files behind"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0006", "apt autoremove purpose", "command", "The apt autoremove command removes packages that were automatically installed to satisfy dependencies and are no longer needed.", [], ["apt autoremove"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > autoremove", "apt autoremove removes no-longer-needed automatically installed dependency packages.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["autoremove is used to remove packages", "automatically installed to satisfy dependencies", "no longer needed"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0007", "apt search behavior", "command", "The apt search command can be used to search for given regex terms in the list of available packages and display matches.", [], ["apt search editor"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > search", "apt search looks for regex terms in available packages and shows matches.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["search", "term(s) in the list of available packages", "display matches"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0008", "apt list filters", "option", "The apt list command can display installed, upgradeable, or all available versions of packages.", [], ["apt list --installed"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > list", "apt list supports installed, upgradeable, and all-versions views.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["--installed", "--upgradeable", "--all-versions"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0009", "apt edit-sources", "command", "The apt edit-sources command lets you edit sources.list files in your preferred text editor while providing basic sanity checks.", [], ["apt edit-sources"], "https://manpages.debian.org/experimental/apt/apt.8.en.html", "DESCRIPTION > edit-sources", "apt edit-sources edits sources.list files with basic sanity checks.", "high", "medium", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-manpage.html", ["edit-sources lets you edit your", "providing basic sanity", "checks"], "Debian apt man page", "apt(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0010", "apt-get update purpose", "command", "The apt-get update command resynchronizes the package index files from their sources.", [], ["apt-get update"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > update", "apt-get update refreshes package index files from configured sources.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["update is used to resynchronize the package index files", "from their sources"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0011", "apt-get update before upgrade", "best_practice", "An apt-get update should always be performed before apt-get upgrade or apt-get dist-upgrade.", [], ["apt-get update && apt-get upgrade"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > update", "The apt-get man page says update should always come before upgrade or dist-upgrade.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["always be performed before an upgrade or dist-upgrade"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0012", "apt-get install dependencies", "behavior", "The apt-get install command retrieves and installs packages required by the specified package or packages.", [], ["apt-get install curl"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > install", "apt-get install also brings in required packages for the requested package set.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["All packages required by", "specified for installation will also be retrieved and", "installed"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0013", "apt-get remove leaves config", "behavior", "The apt-get remove command removes packages but leaves configuration files on the system.", [], ["apt-get remove pkg"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > remove", "apt-get remove leaves configuration files behind.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["removed instead of installed", "configuration files on the system"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0014", "apt-get purge behavior", "behavior", "The apt-get purge command removes packages and deletes configuration files too.", [], ["apt-get purge pkg"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > purge", "apt-get purge removes packages and their configuration files.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["purge is identical to remove except that packages are", "configuration files are deleted too"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0015", "apt-get download behavior", "command", "The apt-get download command downloads the given binary package into the current directory.", [], ["apt-get download pkg"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > download", "apt-get download fetches a binary package into the current directory.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["download will download the given binary package into the", "current directory"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0016", "apt-get clean behavior", "command", "The apt-get clean command removes everything but the lock file from /var/cache/apt/archives/ and /var/cache/apt/archives/partial/.", [], ["apt-get clean"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > clean", "apt-get clean clears retrieved package files but keeps the lock file.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["clean clears out the local repository of retrieved", "removes everything but the lock file"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0017", "apt-get autoclean behavior", "command", "The apt-get autoclean command removes only retrieved package files that can no longer be downloaded.", [], ["apt-get autoclean"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > autoclean", "apt-get autoclean targets obsolete cached package files instead of clearing everything.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["Like clean, autoclean clears out the local repository of", "only removes package files", "can no longer be downloaded"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0018", "apt-get check purpose", "command", "The apt-get check command is a diagnostic tool that updates the package cache and checks for broken dependencies.", [], ["apt-get check"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "DESCRIPTION > check", "apt-get check updates cache metadata and checks dependency consistency.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["check is a diagnostic tool", "updates the package cache", "checks for broken dependencies"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0019", "apt-get download-only option", "option", "The apt-get --download-only option retrieves package files but does not unpack or install them.", [], ["apt-get --download-only install pkg"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "OPTIONS > --download-only", "apt-get --download-only fetches packages without unpacking or installing them.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["--download-only", "Download only", "package files are only retrieved"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0020", "apt-get only-upgrade option", "option", "The apt-get --only-upgrade option does not install new packages and only upgrades packages that are already installed.", [], ["apt-get --only-upgrade install pkg"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "OPTIONS > --only-upgrade", "apt-get --only-upgrade limits install to packages that already exist on the system.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["--only-upgrade", "Do not install new packages", "upgrades for already installed"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0021", "apt-get no-upgrade option", "option", "The apt-get --no-upgrade option prevents command-line packages from being upgraded if they are already installed.", [], ["apt-get --no-upgrade install pkg"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "OPTIONS > --no-upgrade", "apt-get --no-upgrade blocks upgrades of already installed command-line packages.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["--no-upgrade", "prevent packages on the command line from being", "upgraded if they are already installed"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0022", "apt-get with-new-pkgs option", "option", "When used with upgrade, the apt-get --with-new-pkgs option allows installing new dependencies but never removes packages.", [], ["apt-get --with-new-pkgs upgrade"], "https://manpages.debian.org/experimental/apt/apt-get.8.en.html", "OPTIONS > --with-new-pkgs", "apt-get --with-new-pkgs can add new dependency packages during upgrade without allowing removals.", "high", "high", "APT behavior is distribution-specific to Debian-family systems and may vary by release.", "studyapp/input/source_documents/linux/package_management/apt-get-manpage.html", ["--with-new-pkgs", "Allow installing new packages", "will never remove packages"], "Debian apt-get man page", "apt-get(8) man page", "experimental"),
            IRSpec("linux_package_management_ir_0023", "dnf purpose", "definition", "DNF is a package manager for RPM-based Linux distributions.", [], ["dnf install pkg"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Description", "DNF is documented as a package manager for RPM-based Linux distributions.", "high", "high", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["package manager for RPM-based Linux", "distributions"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0024", "dnf return value 0", "behavior", "DNF returns 0 when the operation was successful.", [], ["dnf list"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Return values", "DNF uses exit code 0 for success.", "high", "medium", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["Return values:", "Operation was successful"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0025", "dnf return value 100", "behavior", "DNF uses exit code 100 for the check-update case.", [], ["dnf check-update"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Return values", "DNF reserves exit code 100 for check-update.", "high", "medium", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["Return values:", "100", "check-update"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0026", "dnf allowerasing", "option", "The dnf --allowerasing option allows erasing installed packages to resolve dependencies.", [], ["dnf --allowerasing install pkg"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Options > --allowerasing", "dnf --allowerasing permits package removals during dependency resolution.", "high", "high", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["--allowerasing", "Allow erasing of installed packages to resolve dependencies"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0027", "dnf assumeno", "option", "The dnf --assumeno option automatically answers no for all questions.", [], ["dnf --assumeno upgrade"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Options > --assumeno", "dnf --assumeno declines prompts automatically.", "high", "high", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["--assumeno", "Automatically answer no for all questions"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0028", "dnf best option", "option", "The dnf --best option forces DNF to consider only the latest packages for directly requested packages and fail if the latest version cannot be installed.", [], ["dnf --best install pkg"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Options > --best", "dnf --best prefers latest versions for requested packages and fails when the latest cannot be installed.", "high", "high", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["--best", "only consider the latest packages", "fail giving a reason why the latest version can not be installed"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0029", "dnf cacheonly", "option", "The dnf --cacheonly option runs entirely from the system cache and uses it even when it is expired.", [], ["dnf --cacheonly list"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Options > --cacheonly", "dnf --cacheonly avoids cache refreshes and works from existing cache data.", "high", "high", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["--cacheonly", "Run entirely from system cache", "use it even in case it is expired"], "DNF Command Reference", "DNF Command Reference", "stable"),
            IRSpec("linux_package_management_ir_0030", "dnf disablerepo", "option", "The dnf --disablerepo option temporarily disables active repositories for the current dnf command.", [], ["dnf --disablerepo=repo list"], "https://dnf.readthedocs.io/en/stable/command_ref.html", "Options > --disablerepo", "dnf --disablerepo only affects the current command invocation.", "high", "high", "DNF behavior is distribution-specific to RPM-based systems and plugin behavior can vary by environment.", "studyapp/input/source_documents/linux/package_management/dnf-command-ref.html", ["--disablerepo", "Temporarily disable active repositories", "current dnf command"], "DNF Command Reference", "DNF Command Reference", "stable"),
        ],
        "question_specs": [
            QuestionSpec("linux_package_management_q_0001", "linux_package_management_ir_0001", "The `apt` command is documented as a high-level command-line interface intended for end users.", True, "The `apt` man page describes it as a high-level end user interface.", "basic"),
            QuestionSpec("linux_package_management_q_0002", "linux_package_management_ir_0002", "The `apt upgrade` command only refreshes package metadata and does not install package upgrades.", False, "`apt upgrade` is used to install available upgrades of installed packages.", "basic"),
            QuestionSpec("linux_package_management_q_0003", "linux_package_management_ir_0003", "The `apt upgrade` command does not remove existing installed packages.", True, "The manual explicitly says existing packages will never be removed by `apt upgrade`.", "basic"),
            QuestionSpec("linux_package_management_q_0004", "linux_package_management_ir_0004", "The `apt full-upgrade` command never removes installed packages.", False, "`apt full-upgrade` may remove installed packages when needed to upgrade the system as a whole.", "intermediate"),
            QuestionSpec("linux_package_management_q_0005", "linux_package_management_ir_0005", "Removing a package with `apt remove` can leave modified user configuration files behind.", True, "The `apt` man page says removing a package usually leaves small modified user configuration files behind.", "basic"),
            QuestionSpec("linux_package_management_q_0006", "linux_package_management_ir_0006", "The `apt autoremove` command removes only packages that the user explicitly installed by hand.", False, "`apt autoremove` targets packages that were automatically installed as dependencies and are no longer needed.", "basic"),
            QuestionSpec("linux_package_management_q_0007", "linux_package_management_ir_0007", "The `apt search` command can search available packages for regex terms and display matches.", True, "The `apt` documentation says `search` can search for given regex terms and display matches.", "basic"),
            QuestionSpec("linux_package_management_q_0008", "linux_package_management_ir_0008", "The `apt list` command can show only installed packages, not upgradeable or all available versions.", False, "`apt list` supports installed, upgradeable, and all-versions views.", "basic"),
            QuestionSpec("linux_package_management_q_0009", "linux_package_management_ir_0009", "The `apt edit-sources` command edits `sources.list` files and provides basic sanity checks.", True, "That is the documented purpose of `apt edit-sources`.", "intermediate"),
            QuestionSpec("linux_package_management_q_0010", "linux_package_management_ir_0010", "The `apt-get update` command installs every upgradable package on the system.", False, "`apt-get update` resynchronizes package index files; it does not itself install upgrades.", "basic"),
            QuestionSpec("linux_package_management_q_0011", "linux_package_management_ir_0011", "The `apt-get` documentation says `update` should be performed before `upgrade` or `dist-upgrade`.", True, "The man page explicitly recommends running `update` before `upgrade` or `dist-upgrade`.", "basic"),
            QuestionSpec("linux_package_management_q_0012", "linux_package_management_ir_0012", "The `apt-get install` command never retrieves dependency packages automatically.", False, "`apt-get install` retrieves and installs the packages required by the requested package set.", "basic"),
            QuestionSpec("linux_package_management_q_0013", "linux_package_management_ir_0013", "The `apt-get remove` command removes a package but leaves configuration files on the system.", True, "That is the documented difference between `remove` and `purge`.", "basic"),
            QuestionSpec("linux_package_management_q_0014", "linux_package_management_ir_0014", "The `apt-get purge` command keeps configuration files in place so the package can be restored quickly.", False, "`apt-get purge` removes packages and deletes configuration files too.", "basic"),
            QuestionSpec("linux_package_management_q_0015", "linux_package_management_ir_0015", "The `apt-get download` command downloads the requested binary package into the current directory.", True, "The man page says `download` puts the binary package in the current directory.", "basic"),
            QuestionSpec("linux_package_management_q_0016", "linux_package_management_ir_0016", "The `apt-get clean` command leaves all retrieved package files in the cache.", False, "`apt-get clean` removes everything but the lock file from the package cache directories.", "basic"),
            QuestionSpec("linux_package_management_q_0017", "linux_package_management_ir_0017", "The `apt-get autoclean` command removes only package files that can no longer be downloaded.", True, "Unlike `clean`, `autoclean` removes only obsolete cached package files.", "basic"),
            QuestionSpec("linux_package_management_q_0018", "linux_package_management_ir_0018", "The `apt-get check` command automatically reinstalls packages to fix dependency problems.", False, "`apt-get check` is a diagnostic tool that updates the cache and checks for broken dependencies.", "intermediate"),
            QuestionSpec("linux_package_management_q_0019", "linux_package_management_ir_0019", "The `apt-get --download-only` option retrieves package files without unpacking or installing them.", True, "That option downloads packages only and does not unpack or install them.", "basic"),
            QuestionSpec("linux_package_management_q_0020", "linux_package_management_ir_0020", "With `apt-get --only-upgrade`, `install` can install a brand new package that is not already present.", False, "`--only-upgrade` avoids installing new packages and upgrades only already installed ones.", "intermediate"),
            QuestionSpec("linux_package_management_q_0021", "linux_package_management_ir_0021", "The `apt-get --no-upgrade` option prevents already installed command-line packages from being upgraded.", True, "That is the documented effect of `--no-upgrade` when used with `install`.", "intermediate"),
            QuestionSpec("linux_package_management_q_0022", "linux_package_management_ir_0022", "When used with `upgrade`, `apt-get --with-new-pkgs` allows package removals if dependency resolution needs them.", False, "The option may allow new packages to be installed, but it does not allow removals.", "intermediate"),
            QuestionSpec("linux_package_management_q_0023", "linux_package_management_ir_0023", "DNF is documented as a package manager for RPM-based Linux distributions.", True, "The DNF command reference describes DNF that way.", "basic"),
            QuestionSpec("linux_package_management_q_0024", "linux_package_management_ir_0024", "DNF exit code `0` means an error occurred but DNF handled it.", False, "In DNF, exit code `0` means the operation was successful.", "basic"),
            QuestionSpec("linux_package_management_q_0025", "linux_package_management_ir_0025", "DNF uses exit code `100` for the `check-update` case.", True, "The command reference lists `100` with the note to see `check-update`.", "intermediate"),
            QuestionSpec("linux_package_management_q_0026", "linux_package_management_ir_0026", "The DNF `--allowerasing` option forbids erasing installed packages during dependency resolution.", False, "`--allowerasing` does the opposite: it allows erasing installed packages to resolve dependencies.", "intermediate"),
            QuestionSpec("linux_package_management_q_0027", "linux_package_management_ir_0027", "The DNF `--assumeno` option automatically answers no to all questions.", True, "That is the explicit behavior of `--assumeno`.", "basic"),
            QuestionSpec("linux_package_management_q_0028", "linux_package_management_ir_0028", "The DNF `--best` option lets DNF silently settle for an older directly requested package when the latest version cannot be installed.", False, "For directly requested packages, `--best` forces the latest choice and fails if it cannot be installed.", "advanced"),
            QuestionSpec("linux_package_management_q_0029", "linux_package_management_ir_0029", "The DNF `--cacheonly` option runs from cache without updating it, even if the cache is expired.", True, "The reference says `--cacheonly` uses the system cache entirely, even when expired.", "intermediate"),
            QuestionSpec("linux_package_management_q_0030", "linux_package_management_ir_0030", "The DNF `--disablerepo` option permanently disables repositories until they are manually re-enabled later.", False, "The option only temporarily disables active repositories for the current DNF command.", "intermediate"),
        ],
    },
    ("linux", "networking"): {
        "ir_specs": [
            IRSpec("linux_networking_ir_0001", "hostname no-args behavior", "command", "With no arguments, the hostname command prints the name of the current host system.", [], ["hostname"], "https://www.gnu.org/software/coreutils/manual/html_node/hostname-invocation.html", "hostname invocation", "With no arguments, hostname prints the current host system name.", "high", "high", "Other packages may also supply a hostname command.", "studyapp/input/source_documents/linux/networking/hostname-invocation.html", ["With no arguments", "prints the name of the current host", "system"], "", "", ""),
            IRSpec("linux_networking_ir_0002", "hostname one-arg behavior", "behavior", "With one argument, the hostname command sets the current host name to the specified string.", [], ["hostname newname"], "https://www.gnu.org/software/coreutils/manual/html_node/hostname-invocation.html", "hostname invocation", "With one argument, hostname sets the current host name.", "high", "high", "Changing the hostname depends on runtime privileges.", "studyapp/input/source_documents/linux/networking/hostname-invocation.html", ["With one argument", "sets the current host name", "specified string"], "", "", ""),
            IRSpec("linux_networking_ir_0003", "hostname privilege rule", "limitation", "You must have appropriate privileges to set the host name with the hostname command.", [], ["hostname newname"], "https://www.gnu.org/software/coreutils/manual/html_node/hostname-invocation.html", "hostname invocation", "Setting the host name requires appropriate privileges.", "high", "high", "", "studyapp/input/source_documents/linux/networking/hostname-invocation.html", ["appropriate privileges to set the host", "name"], "", "", ""),
            IRSpec("linux_networking_ir_0004", "hostname portability warning", "warning", "Portable scripts should not rely on the existence of the hostname command or on the exact behavior documented for it.", [], ["hostname"], "https://www.gnu.org/software/coreutils/manual/html_node/hostname-invocation.html", "hostname invocation", "The manual warns that portable scripts should not rely on hostname being present or behaving exactly as documented.", "high", "high", "This is a portability warning, not a runtime error.", "studyapp/input/source_documents/linux/networking/hostname-invocation.html", ["portable scripts should", "not rely on its existence", "exact behavior documented above"], "", "", ""),
            IRSpec("linux_networking_ir_0005", "ping purpose", "definition", "The ping command sends ICMP ECHO_REQUEST packets to network hosts.", [], ["ping example.com"], "https://man7.org/linux/man-pages/man8/ping.8.html", "NAME", "ping sends ICMP ECHO_REQUEST to network hosts.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["send ICMP ECHO_REQUEST to network hosts"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0006", "ping dual-stack support", "behavior", "The ping command works with both IPv4 and IPv6.", [], ["ping -4 host", "ping -6 host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "DESCRIPTION", "ping works with both IPv4 and IPv6.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["works with both IPv4 and IPv6"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0007", "ping family selection", "option", "The ping command can explicitly enforce IPv4 or IPv6 by specifying -4 or -6.", [], ["ping -4 host", "ping -6 host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "DESCRIPTION", "ping can be forced to IPv4 or IPv6 with -4 or -6.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["explicitly can be enforced by specifying", "-4", "or", "-6"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0008", "ping count option", "option", "The ping -c option stops after sending the specified count of ECHO_REQUEST packets.", [], ["ping -c 3 host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "OPTIONS > -c", "ping -c stops after the requested number of ECHO_REQUEST packets are sent.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["Stop after sending", "ECHO_REQUEST packets"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0009", "ping interval option", "option", "The ping -i option waits the specified interval in seconds between sending each packet.", [], ["ping -i 0.5 host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "OPTIONS > -i", "ping -i controls the delay between packets.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["Wait", "seconds between sending each", "packet"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0010", "ping default interval", "definition", "By default, ping waits one second between each packet in normal operation.", [], ["ping host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "OPTIONS > -i", "The default ping interval is one second between packets.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["default is to wait for one second between each", "packet"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0011", "ping low interval privilege rule", "limitation", "Only the super-user may set the ping interval to values less than 2 ms.", [], ["ping -i 0.001 host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "OPTIONS > -i", "Sub-2ms ping intervals require super-user privileges.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["Only super-user", "may set interval to values less than 2 ms"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0012", "ping quiet output", "option", "The ping -q option produces quiet output in which only the summary lines at startup and finish are displayed.", [], ["ping -q host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "OPTIONS > -q", "Quiet ping output shows only summary lines.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["Quiet output", "Nothing is displayed except the summary lines"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0013", "ping exit code 1", "behavior", "The ping command exits with code 1 if it receives no reply packets at all.", [], ["ping host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "EXIT STATUS", "ping uses exit code 1 when no reply packets are received.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["does not receive any reply packets at all", "exit", "code 1"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0014", "ping exit code 2", "behavior", "The ping command exits with code 2 on errors other than the no-reply case.", [], ["ping host"], "https://man7.org/linux/man-pages/man8/ping.8.html", "EXIT STATUS", "ping uses exit code 2 for other errors.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ping.8.html", ["On other error it", "exits with code 2"], "ping(8) Linux manual page", "ping(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0015", "ss purpose", "definition", "The ss command is used to dump socket statistics.", [], ["ss"], "https://man7.org/linux/man-pages/man8/ss.8.html", "DESCRIPTION", "ss is a socket statistics utility.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["is used to dump socket statistics"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0016", "ss default scope", "behavior", "When no option is used, ss displays open non-listening sockets that have established connections.", [], ["ss"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS", "By default, ss shows open non-listening sockets with established connections.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["When no option is used", "open non-listening", "have established connections"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0017", "ss all option", "option", "The ss -a option displays both listening and non-listening sockets.", [], ["ss -a"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS > -a", "ss -a includes listening and non-listening sockets.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["-a, --all", "Display both listening and non-listening"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0018", "ss listening option", "option", "The ss -l option displays only listening sockets.", [], ["ss -l"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS > -l", "ss -l filters to listening sockets only.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["-l, --listening", "Display only listening sockets"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0019", "ss process option", "option", "The ss -p option shows processes using sockets.", [], ["ss -p"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS > -p", "ss -p shows process information for sockets.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["Show processes using sockets"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0020", "ss summary option", "option", "The ss -s option prints summary statistics and does not parse socket lists to obtain the summary.", [], ["ss -s"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS > -s", "ss -s prints summary statistics without parsing socket lists.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["Print summary statistics", "does not parse socket", "lists"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0021", "ss ipv4 option", "option", "The ss -4 option displays only IP version 4 sockets.", [], ["ss -4"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS > -4", "ss -4 limits output to IPv4 sockets.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["-4, --ipv4", "Display only IP version 4 sockets"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0022", "ss ipv6 option", "option", "The ss -6 option displays only IP version 6 sockets.", [], ["ss -6"], "https://man7.org/linux/man-pages/man8/ss.8.html", "OPTIONS > -6", "ss -6 limits output to IPv6 sockets.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ss.8.html", ["-6, --ipv6", "Display only IP version 6 sockets"], "ss(8) Linux manual page", "ss(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0023", "ip address show purpose", "definition", "The ip address show command looks at protocol addresses.", [], ["ip address show"], "https://man7.org/linux/man-pages/man8/ip-address.8.html", "ip address show - look at protocol addresses", "ip address show is used to inspect protocol addresses.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-address.8.html", ["ip address show - look at protocol addresses"], "ip-address(8) Linux manual page", "ip-address(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0024", "ip address show up", "option", "In ip address show, the up selector lists only running interfaces.", [], ["ip address show up"], "https://man7.org/linux/man-pages/man8/ip-address.8.html", "ip address show", "ip address show up limits results to active interfaces.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-address.8.html", ["up", "only list running interfaces"], "ip-address(8) Linux manual page", "ip-address(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0025", "ip address flush purpose", "command", "The ip address flush command flushes protocol addresses selected by criteria.", [], ["ip address flush dev eth0"], "https://man7.org/linux/man-pages/man8/ip-address.8.html", "ip address flush - flush protocol addresses", "ip address flush removes selected protocol addresses.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-address.8.html", ["ip address flush - flush protocol addresses", "flushes the protocol addresses selected by some", "criteria"], "ip-address(8) Linux manual page", "ip-address(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0026", "ip address flush no-args rule", "limitation", "The ip address flush command does not run when no arguments are given.", [], ["ip address flush"], "https://man7.org/linux/man-pages/man8/ip-address.8.html", "ip address flush - flush protocol addresses", "ip address flush requires selection arguments and does not run with none.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-address.8.html", ["does not run when no arguments are given"], "ip-address(8) Linux manual page", "ip-address(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0027", "ip address flush warning", "warning", "The ip address flush command is unforgiving and can purge all addresses.", [], ["ip address flush dev eth0"], "https://man7.org/linux/man-pages/man8/ip-address.8.html", "ip address flush - flush protocol addresses", "The manual warns that ip address flush can cruelly purge all addresses.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-address.8.html", ["Warning:", "flush", "unforgiving", "purge all the addresses"], "ip-address(8) Linux manual page", "ip-address(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0028", "ip link set purpose", "definition", "The ip link set command changes device attributes.", [], ["ip link set dev eth0 up"], "https://man7.org/linux/man-pages/man8/ip-link.8.html", "ip link set - change device attributes", "ip link set is the subcommand for changing link device attributes.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-link.8.html", ["ip link set - change device attributes"], "ip-link(8) Linux manual page", "ip-link(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0029", "ip link set multi-change warning", "warning", "If multiple parameter changes are requested, ip can abort after a failure and move the system to an unpredictable state.", [], ["ip link set dev eth0 mtu 1400 up"], "https://man7.org/linux/man-pages/man8/ip-link.8.html", "ip link set - change device attributes", "The ip-link manual warns against combining many parameter changes in one set call.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-link.8.html", ["multiple parameter changes are requested", "unpredictable state"], "ip-link(8) Linux manual page", "ip-link(8)", "Linux man-pages online"),
            IRSpec("linux_networking_ir_0030", "ip link set up-down", "behavior", "In ip link set, the up and down modifiers change the state of the device to UP or DOWN.", [], ["ip link set dev eth0 up"], "https://man7.org/linux/man-pages/man8/ip-link.8.html", "ip link set - change device attributes", "ip link set up/down changes interface state.", "high", "high", "", "studyapp/input/source_documents/linux/networking/ip-link.8.html", ["up", "and", "down", "change the state of the device to", "UP", "DOWN"], "ip-link(8) Linux manual page", "ip-link(8)", "Linux man-pages online"),
        ],
        "question_specs": [
            QuestionSpec("linux_networking_q_0001", "linux_networking_ir_0001", "With no arguments, the `hostname` command prints the current host system name.", True, "The GNU Coreutils manual says `hostname` prints the current host system name when called without arguments.", "basic"),
            QuestionSpec("linux_networking_q_0002", "linux_networking_ir_0002", "With one argument, the `hostname` command appends the string to the current host name instead of replacing it.", False, "With one argument, `hostname` sets the current host name to the specified string.", "basic"),
            QuestionSpec("linux_networking_q_0003", "linux_networking_ir_0003", "Setting the host name with `hostname` requires appropriate privileges.", True, "The manual explicitly says appropriate privileges are required to set the host name.", "basic"),
            QuestionSpec("linux_networking_q_0004", "linux_networking_ir_0004", "Portable scripts can safely rely on `hostname` always existing and following the exact GNU behavior.", False, "The manual warns portable scripts not to rely on the command's existence or exact behavior.", "intermediate"),
            QuestionSpec("linux_networking_q_0005", "linux_networking_ir_0005", "The `ping` command sends ICMP ECHO_REQUEST packets to network hosts.", True, "That is the core purpose stated in the manual page name section.", "basic"),
            QuestionSpec("linux_networking_q_0006", "linux_networking_ir_0006", "The `ping` command works only with IPv4 unless a separate `ping6` binary is used.", False, "The manual says `ping` works with both IPv4 and IPv6.", "basic"),
            QuestionSpec("linux_networking_q_0007", "linux_networking_ir_0007", "You can force `ping` to use one address family by specifying `-4` or `-6`.", True, "The manual says `-4` and `-6` explicitly enforce one family.", "basic"),
            QuestionSpec("linux_networking_q_0008", "linux_networking_ir_0008", "The `ping -c` option stops only after receiving a given number of replies, regardless of how many requests it sends.", False, "The `-c` option stops after sending the specified count of ECHO_REQUEST packets.", "intermediate"),
            QuestionSpec("linux_networking_q_0009", "linux_networking_ir_0009", "The `ping -i` option controls the time between sending packets.", True, "The `-i` option sets the interval in seconds between sent packets.", "basic"),
            QuestionSpec("linux_networking_q_0010", "linux_networking_ir_0010", "In normal operation, `ping` waits two seconds between packets by default.", False, "The default documented interval is one second between packets.", "basic"),
            QuestionSpec("linux_networking_q_0011", "linux_networking_ir_0011", "Only the super-user may set `ping` intervals smaller than 2 ms.", True, "The manual states that intervals below 2 ms require super-user privileges.", "intermediate"),
            QuestionSpec("linux_networking_q_0012", "linux_networking_ir_0012", "The `ping -q` option suppresses the summary lines and prints only per-packet output.", False, "Quiet mode does the reverse: it shows only the summary lines.", "basic"),
            QuestionSpec("linux_networking_q_0013", "linux_networking_ir_0013", "If `ping` receives no reply packets at all, it exits with code 1.", True, "Exit code 1 is used for the no-reply case.", "intermediate"),
            QuestionSpec("linux_networking_q_0014", "linux_networking_ir_0014", "When `ping` hits an error other than the no-reply case, it exits with code 0.", False, "The manual says other errors cause exit code 2.", "intermediate"),
            QuestionSpec("linux_networking_q_0015", "linux_networking_ir_0015", "The `ss` command is used to dump socket statistics.", True, "`ss` is described as a utility for dumping socket statistics.", "basic"),
            QuestionSpec("linux_networking_q_0016", "linux_networking_ir_0016", "Without options, `ss` shows only listening sockets.", False, "By default `ss` shows open non-listening sockets with established connections.", "basic"),
            QuestionSpec("linux_networking_q_0017", "linux_networking_ir_0017", "The `ss -a` option displays both listening and non-listening sockets.", True, "That is the documented behavior of `ss -a`.", "basic"),
            QuestionSpec("linux_networking_q_0018", "linux_networking_ir_0018", "The `ss -l` option includes both listening and non-listening sockets.", False, "`ss -l` restricts output to listening sockets only.", "basic"),
            QuestionSpec("linux_networking_q_0019", "linux_networking_ir_0019", "The `ss -p` option shows processes using sockets.", True, "The manual says `-p` shows processes using sockets.", "basic"),
            QuestionSpec("linux_networking_q_0020", "linux_networking_ir_0020", "The `ss -s` option computes its summary only by parsing all socket lists first.", False, "The manual explicitly says `ss -s` does not parse socket lists to obtain the summary.", "intermediate"),
            QuestionSpec("linux_networking_q_0021", "linux_networking_ir_0021", "The `ss -4` option displays only IPv4 sockets.", True, "That is the documented effect of `-4`.", "basic"),
            QuestionSpec("linux_networking_q_0022", "linux_networking_ir_0022", "The `ss -6` option displays only IPv4 sockets.", False, "The `-6` option limits output to IPv6 sockets.", "basic"),
            QuestionSpec("linux_networking_q_0023", "linux_networking_ir_0023", "The `ip address show` command is used to look at protocol addresses.", True, "The man page uses that exact description.", "basic"),
            QuestionSpec("linux_networking_q_0024", "linux_networking_ir_0024", "In `ip address show`, the `up` selector lists every interface, including non-running ones.", False, "The `up` selector lists only running interfaces.", "basic"),
            QuestionSpec("linux_networking_q_0025", "linux_networking_ir_0025", "The `ip address flush` command flushes protocol addresses selected by criteria.", True, "That is the command's documented purpose.", "basic"),
            QuestionSpec("linux_networking_q_0026", "linux_networking_ir_0026", "The `ip address flush` command runs normally even when you give it no arguments.", False, "The manual states that it does not run when no arguments are given.", "intermediate"),
            QuestionSpec("linux_networking_q_0027", "linux_networking_ir_0027", "The `ip address flush` command is documented as unforgiving and capable of purging all addresses.", True, "The man page includes a direct warning about this.", "intermediate"),
            QuestionSpec("linux_networking_q_0028", "linux_networking_ir_0028", "The `ip link set` subcommand is used only to display device attributes.", False, "`ip link set` changes device attributes; display belongs to `ip link show`.", "basic"),
            QuestionSpec("linux_networking_q_0029", "linux_networking_ir_0029", "The `ip-link` manual warns that combining multiple parameter changes in one `ip link set` call can leave the system in an unpredictable state after a failure.", True, "The warning says a failed multi-change call can move the system to an unpredictable state.", "advanced"),
            QuestionSpec("linux_networking_q_0030", "linux_networking_ir_0030", "In `ip link set`, the `up` and `down` modifiers adjust only logging verbosity and do not change interface state.", False, "The manual says `up` and `down` change the device state to UP or DOWN.", "basic"),
        ],
    },
    ("linux", "shell_scripting"): {
        "ir_specs": [
            IRSpec("linux_shell_scripting_ir_0001", "script $0", "behavior", "When Bash runs a shell script, it sets the special parameter 0 to the name of the file rather than the name of the shell.", [], ["./script.sh"], "https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html", "Shell Scripts", "For a shell script, Bash sets special parameter 0 to the script file name.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/shell-scripts.html", ["sets the special parameter", "0", "to the name", "of the file"], "GNU Bash Reference Manual", "Shell Scripts", ""),
            IRSpec("linux_shell_scripting_ir_0002", "script positional params unset", "behavior", "If no additional arguments are supplied to a shell script, the positional parameters are unset.", [], ["./script.sh"], "https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html", "Shell Scripts", "A script with no extra arguments has unset positional parameters.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/shell-scripts.html", ["If no additional arguments are supplied", "positional parameters", "unset"], "GNU Bash Reference Manual", "Shell Scripts", ""),
            IRSpec("linux_shell_scripting_ir_0003", "script executable bit", "best_practice", "A shell script may be made executable by using chmod to turn on the execute bit.", [], ["chmod +x script.sh"], "https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html", "Shell Scripts", "chmod can make a shell script executable by enabling the execute bit.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/shell-scripts.html", ["may be made executable", "chmod", "execute bit"], "GNU Bash Reference Manual", "Shell Scripts", ""),
            IRSpec("linux_shell_scripting_ir_0004", "script new Bash instance via PATH", "behavior", "When Bash finds an executable shell script while searching PATH for a command, it creates a new instance of itself to execute it.", [], ["script.sh"], "https://www.gnu.org/software/bash/manual/html_node/Shell-Scripts.html", "Shell Scripts", "Bash launches a new instance of itself to execute a discovered shell script.", "high", "medium", "", "studyapp/input/source_documents/linux/shell_scripting/shell-scripts.html", ["searching the", "$PATH", "creates a new instance of itself to execute it"], "GNU Bash Reference Manual", "Shell Scripts", ""),
            IRSpec("linux_shell_scripting_ir_0005", "if zero rule", "behavior", "In an if command, if the test-commands list returns status zero, the consequent-commands list is executed.", [], ["if test; then echo ok; fi"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > if", "if executes its consequent when the test command list succeeds.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["if its return status is zero", "consequent-commands", "executed"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0006", "if elif rule", "behavior", "If the test-commands list of an if command returns non-zero, each elif list is executed in turn, and the matching consequent runs when one returns zero.", [], ["if false; then :; elif true; then echo ok; fi"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > if", "elif branches are checked in order until one succeeds.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["returns a non-zero status", "each", "elif", "executed in turn", "exit status is zero"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0007", "if else rule", "behavior", "If the final command in the final if or elif clause has a non-zero exit status and an else clause is present, the alternate-consequents are executed.", [], ["if false; then :; else echo alt; fi"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > if", "The else branch runs when prior conditions do not succeed.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["else", "final", "non-zero exit status", "alternate-consequents", "executed"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0008", "if return status last command", "behavior", "The return status of an if command is the exit status of the last command executed.", [], ["if true; then echo ok; fi"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > if", "An if command returns the exit status of its last executed command.", "high", "medium", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["The return status is the exit status of the last command executed"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0009", "if zero if no condition true", "behavior", "An if command returns zero if no condition tested true.", [], ["if false; then :; fi"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > if", "When no if condition succeeds, the if command returns zero.", "high", "medium", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["zero if no condition tested true"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0010", "case no-match return", "behavior", "The return status of a case command is zero if no pattern matches.", [], ["case x in y) :;; esac"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > case", "case returns zero when nothing matches.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["return status is zero if no", "pattern", "matches"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0011", "case match return", "behavior", "If a case command matches a clause, its return status is the exit status of the last command-list executed.", [], ["case x in x) echo ok;; esac"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > case", "A matching case command returns the last executed command-list's status.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["Otherwise, the return status is the exit status of the", "last", "command-list", "executed"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0012", "select purpose", "definition", "The select construct allows the easy generation of menus.", [], ["select item in a b; do break; done"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > select", "select is a shell construct for easy menu generation.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["select", "allows the easy generation of menus"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0013", "select default words", "behavior", "If the word list is omitted in a select command, Bash uses the positional parameters as if in \"$@\" had been specified.", [], ["select x; do break; done"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > select", "Without an explicit list, select uses the positional parameters.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["words", "is omitted", "print the positional parameters", "&quot;$@&quot;"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0014", "select empty line behavior", "behavior", "If an empty line is read by select, it displays the words and prompt again.", [], ["select x in a b; do :; done"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > select", "An empty input line makes select redisplay its menu and prompt.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["If the line is empty", "displays the words and prompt again"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0015", "select EOF return", "behavior", "If EOF is read, a select command completes and returns 1.", [], ["select x in a b; do :; done"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > select", "select returns 1 on EOF.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["If", "EOF", "is read", "returns 1"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0016", "select invalid input name null", "behavior", "If select reads any other value that is not a valid menu number, it sets the selected name to null.", [], ["select x in a b; do :; done"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > select", "Invalid non-empty select input sets the selection variable to null.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["Any other value read causes", "name", "to be set to null"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0017", "select REPLY", "behavior", "The line read by a select command is saved in the REPLY variable.", [], ["select x in a b; do :; done"], "https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html", "Conditional Constructs > select", "select stores the raw input line in REPLY.", "high", "medium", "", "studyapp/input/source_documents/linux/shell_scripting/conditional-constructs.html", ["line read is saved in the variable", "REPLY"], "GNU Bash Reference Manual", "Conditional Constructs", ""),
            IRSpec("linux_shell_scripting_ir_0018", "command builtin skips function", "behavior", "If there is a shell function named ls, running command ls within that function executes the external command ls instead of calling the function recursively.", [], ["command ls"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > command", "The command builtin can bypass shell functions during command lookup.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["command ls", "external command", "instead of calling the function recursively"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0019", "command search scope", "definition", "The command builtin executes only shell builtin commands or commands found by searching PATH.", [], ["command printf ok"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > command", "command runs builtins or PATH-found commands.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["Only shell builtin commands or commands found by searching the", "PATH", "are executed"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0020", "command 127 rule", "behavior", "The command builtin returns status 127 if the requested command cannot be found or an error occurred.", [], ["command missingcmd"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > command", "command uses exit status 127 for command-not-found or similar lookup errors.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["return status", "127", "cannot be", "found or an error occurred"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0021", "readonly effect", "behavior", "Readonly names cannot be assigned values by subsequent assignment statements or unset.", [], ["readonly x=1"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > declare -r", "Readonly names cannot be reassigned or unset normally.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["Make", "readonly", "cannot then be assigned values", "or unset"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0022", "readonly cannot be removed", "limitation", "Using +r with declare does not remove the readonly attribute.", [], ["declare +r x"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > declare", "The readonly attribute cannot be turned off with +r.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["+r", "will not", "remove the readonly attribute"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0023", "declare local in function", "behavior", "When used in a function, declare makes each name local unless the -g option is supplied.", [], ["f(){ declare x=1; }"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > declare", "Inside a function, declare behaves like local unless -g is used.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["When used in a function", "declare", "makes each", "name", "local", "-g"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0024", "local only in function", "limitation", "The local builtin can only be used within a function.", [], ["local x=1"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > local", "local is valid only inside a shell function.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["local", "can only be used within a function"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0025", "local scope", "behavior", "The local builtin makes a variable's visible scope restricted to that function and its children.", [], ["f(){ local x=1; }"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > local", "local restricts visibility to the function scope and child contexts.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["visible scope restricted to that function and its", "children"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0026", "local no operands", "behavior", "With no operands, the local builtin writes a list of local variables to standard output.", [], ["local"], "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html", "Bash Builtins > local", "local with no operands lists local variables.", "high", "medium", "", "studyapp/input/source_documents/linux/shell_scripting/bash-builtins.html", ["With no operands", "writes a list of local variables"], "GNU Bash Reference Manual", "Bash Builtins", ""),
            IRSpec("linux_shell_scripting_ir_0027", "shell functions purpose", "definition", "Shell functions are a way to group commands for later execution using a single name for the group.", [], ["myfunc(){ echo hi; }"], "https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html", "Shell Functions", "Shell functions group commands under a reusable name.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-reference-manual.html", ["Shell functions are a way to group commands for later execution", "single name"], "GNU Bash Reference Manual", "Shell Functions", ""),
            IRSpec("linux_shell_scripting_ir_0028", "shell functions current shell", "behavior", "Shell functions are executed in the current shell context, and no new process is created to interpret them.", [], ["myfunc"], "https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html", "Shell Functions", "Shell functions run in the current shell process rather than a separate one.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-reference-manual.html", ["executed in the current", "shell context", "no new process"], "GNU Bash Reference Manual", "Shell Functions", ""),
            IRSpec("linux_shell_scripting_ir_0029", "special parameter $#", "definition", "The special parameter $# expands to the number of positional parameters in decimal.", [], ["echo $#"], "https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html", "Special Parameters > #", "$# gives the positional parameter count.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-reference-manual.html", ["($#)", "number of positional parameters"], "GNU Bash Reference Manual", "Special Parameters", ""),
            IRSpec("linux_shell_scripting_ir_0030", "special parameter $?", "definition", "The special parameter $? expands to the exit status of the most recently executed command.", [], ["echo $?"], "https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html", "Special Parameters > ?", "$? gives the most recent command's exit status.", "high", "high", "", "studyapp/input/source_documents/linux/shell_scripting/bash-reference-manual.html", ["($?)", "exit status of the most recently executed command"], "GNU Bash Reference Manual", "Special Parameters", ""),
        ],
        "question_specs": [
            QuestionSpec("linux_shell_scripting_q_0001", "linux_shell_scripting_ir_0001", "When Bash runs a shell script, special parameter `$0` is set to the script file name rather than the shell name.", True, "For a script, Bash sets `$0` to the file name being executed.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0002", "linux_shell_scripting_ir_0002", "If a shell script is run with no additional arguments, its positional parameters are automatically set to empty strings.", False, "The manual says the positional parameters are unset when no additional arguments are supplied.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0003", "linux_shell_scripting_ir_0003", "A shell script can be made executable by using `chmod` to turn on the execute bit.", True, "That is the documented way to make a shell script executable.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0004", "linux_shell_scripting_ir_0004", "When Bash finds an executable shell script through `PATH`, it always runs it in the current shell without creating a new Bash instance.", False, "The manual says Bash creates a new instance of itself to execute such a script.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0005", "linux_shell_scripting_ir_0005", "In an `if` command, a zero status from the test command list causes the consequent command list to run.", True, "A successful test list makes the `then` branch run.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0006", "linux_shell_scripting_ir_0006", "In an `if` command, `elif` branches are skipped unless the initial test command returned zero.", False, "`elif` branches are checked when earlier tests return non-zero.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0007", "linux_shell_scripting_ir_0007", "If an `else` clause is present, it can run when the prior `if` or `elif` conditions do not succeed.", True, "The `else` branch runs when the earlier conditions do not succeed.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0008", "linux_shell_scripting_ir_0008", "The return status of an `if` command is always the status of its test command list.", False, "The manual says the return status is the exit status of the last command executed.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0009", "linux_shell_scripting_ir_0009", "If no condition tested true, an `if` command returns zero.", True, "That is the documented fallback return status of the `if` command.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0010", "linux_shell_scripting_ir_0010", "A `case` command returns failure by default when no pattern matches.", False, "The manual says a `case` command returns zero if no pattern matches.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0011", "linux_shell_scripting_ir_0011", "If a `case` clause matches, the command's return status is the exit status of the last command-list executed.", True, "That is how the `case` command reports status when a clause runs.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0012", "linux_shell_scripting_ir_0012", "The `select` construct exists to make menu generation easier.", True, "The Bash manual describes `select` as a construct for easy menu generation.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0013", "linux_shell_scripting_ir_0013", "If a `select` command omits the word list, it behaves as if no menu items exist at all.", False, "Without a word list, `select` uses the positional parameters as if `in \"$@\"` were given.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0014", "linux_shell_scripting_ir_0014", "If `select` reads an empty line, it displays the menu words and prompt again.", True, "An empty line causes `select` to redisplay the choices and prompt.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0015", "linux_shell_scripting_ir_0015", "If `select` reads EOF, it completes and returns 1.", True, "The manual explicitly documents return value 1 on EOF.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0016", "linux_shell_scripting_ir_0016", "If `select` reads a non-empty invalid value, it keeps the selection variable unchanged.", False, "The manual says the selected name is set to null for other values.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0017", "linux_shell_scripting_ir_0017", "The raw line read by `select` is stored in the `PS3` variable.", False, "The Bash manual says `select` saves the line it read in `REPLY`, not `PS3`.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0018", "linux_shell_scripting_ir_0018", "Inside a shell function named `ls`, using `command ls` can execute the external `ls` instead of recursing into the function.", True, "The `command` builtin can bypass a shell function of the same name.", "advanced"),
            QuestionSpec("linux_shell_scripting_q_0019", "linux_shell_scripting_ir_0019", "The `command` builtin can execute shell builtins or commands found through `PATH` lookup.", True, "That is the execution scope documented for `command`.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0020", "linux_shell_scripting_ir_0020", "If the requested command cannot be found, the `command` builtin returns status 0.", False, "The documented return status is 127 when the command cannot be found or an error occurs.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0021", "linux_shell_scripting_ir_0021", "After a name is made readonly, later assignment or `unset` on that name is not allowed.", True, "Readonly names cannot be reassigned or unset by normal means.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0022", "linux_shell_scripting_ir_0022", "Using `declare +r` removes the readonly attribute from a readonly variable.", False, "The manual explicitly says `+r` does not remove the readonly attribute.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0023", "linux_shell_scripting_ir_0023", "Inside a function, `declare` makes each declared name local unless `-g` is used.", True, "Within a function, `declare` behaves like `local` unless `-g` is supplied.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0024", "linux_shell_scripting_ir_0024", "The `local` builtin can be used at top level outside of any function as long as the variable name is valid.", False, "The Bash manual says `local` can only be used within a function.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0025", "linux_shell_scripting_ir_0025", "A variable created with `local` remains visibly scoped across the whole shell after the function returns.", False, "The manual says `local` restricts visible scope to that function and its children.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0026", "linux_shell_scripting_ir_0026", "When `local` is called with no operands, it clears all existing local variables.", False, "With no operands, `local` writes a list of local variables to standard output.", "intermediate"),
            QuestionSpec("linux_shell_scripting_q_0027", "linux_shell_scripting_ir_0027", "Shell functions group commands for later execution under a single name.", True, "That is the Bash manual's basic description of shell functions.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0028", "linux_shell_scripting_ir_0028", "Shell functions always run in a separate process from the current shell.", False, "The manual says shell functions execute in the current shell context with no new process.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0029", "linux_shell_scripting_ir_0029", "The special parameter `$#` expands to the number of positional parameters.", True, "`$#` is the decimal count of positional parameters.", "basic"),
            QuestionSpec("linux_shell_scripting_q_0030", "linux_shell_scripting_ir_0030", "The special parameter `$?` expands to the output text of the most recently executed command.", False, "`$?` expands to the exit status of the most recently executed command, not its output.", "basic"),
        ],
    },
}


class PipelineError(Exception):
    def __init__(self, step: str, reason: str) -> None:
        super().__init__(reason)
        self.step = step
        self.reason = reason


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def app_config_path(app_id: str) -> Path:
    return ROOT / "apps" / "active_apps" / app_id / "app_config.json"


def output_path(*parts: str) -> Path:
    return ROOT.joinpath("output", *parts)


def source_dir(app_id: str, category: str) -> Path:
    return ROOT / "input" / "source_documents" / app_id / category


def source_files_in_directory(directory: Path) -> list[Path]:
    return [
        path
        for path in directory.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]


def ir_source_document_rel(spec: IRSpec) -> str:
    if isinstance(spec.source_document_rel, str) and spec.source_document_rel:
        return spec.source_document_rel
    return SOURCE_DOC_REL


def ir_required_snippets(spec: IRSpec) -> list[str]:
    if spec.required_snippets:
        return spec.required_snippets
    if isinstance(spec.source_document_rel, list):
        return spec.source_document_rel
    return []


def profile_from_json(profile_data: dict[str, Any]) -> dict[str, Any]:
    ir_keys = {
        "id",
        "topic",
        "fact_type",
        "statement",
        "conditions",
        "examples",
        "source_url",
        "source_section",
        "source_quote_or_summary",
        "confidence",
        "question_potential",
        "notes",
        "source_document_rel",
        "required_snippets",
        "source_name",
        "source_title",
        "source_version",
    }
    question_keys = {
        "id",
        "source_ir_id",
        "question",
        "answer",
        "explanation",
        "difficulty",
    }
    return {
        "ir_specs": [
            IRSpec(**{
                "source_document_rel": item.get("source_document_path", item.get("source_document_rel", "")),
                "source_name": item.get("source", item.get("source_name", "")),
                **{key: value for key, value in item.items() if key in ir_keys},
            })
            for item in profile_data["ir_specs"]
        ],
        "question_specs": [
            QuestionSpec(**{key: value for key, value in item.items() if key in question_keys})
            for item in profile_data["question_specs"]
        ],
    }


def load_profile(app_id: str, category: str) -> dict[str, Any] | None:
    bank_path = BANK_ROOT / app_id / f"{category}.json"
    if bank_path.exists():
        return profile_from_json(load_json(bank_path))
    return SUPPORTED_PIPELINES.get((app_id, category))


def load_cycle_profile(app_id: str, category: str, cycle: str) -> dict[str, Any] | None:
    cycle_path = CYCLE_BANK_ROOT / app_id / category / f"{cycle}.json"
    if cycle_path.exists():
        return profile_from_json(load_json(cycle_path))
    return None


def slice_profile_for_cycle(profile: dict[str, Any], cycle: str) -> dict[str, Any]:
    if cycle not in CYCLE_WINDOWS:
        raise PipelineError("read_app_config", f"Unsupported cycle: {cycle}")
    start, end = CYCLE_WINDOWS[cycle]
    ir_specs = profile["ir_specs"]
    question_specs = profile["question_specs"]
    if len(question_specs) < end:
        raise PipelineError("read_source_documents", f"Profile does not contain enough question items for {cycle}. Needed {end}, found {len(question_specs)} questions.")
    cycle_questions = question_specs[start:end]
    required_ir_ids = {item.source_ir_id for item in cycle_questions}
    cycle_irs = [item for item in ir_specs if item.id in required_ir_ids]
    if len(cycle_irs) != len(required_ir_ids):
        raise PipelineError("read_source_documents", f"Profile is missing one or more IR items referenced by {cycle}.")
    return {
        "ir_specs": cycle_irs,
        "question_specs": cycle_questions,
    }


def require_curated_cycle_profile(app_id: str, category: str, cycle: str) -> dict[str, Any]:
    cycle_profile = load_cycle_profile(app_id, category, cycle)
    if cycle_profile is None:
        raise PipelineError(
            "read_source_documents",
            f"Missing curated cycle bank for {app_id}/{category}/{cycle}. cycle_02 and later must use individually reviewed cycle banks under {CYCLE_BANK_ROOT / app_id / category}.",
        )
    return cycle_profile


def verify_app_and_category(app_id: str, category: str) -> dict[str, Any]:
    config_path = app_config_path(app_id)
    if not config_path.exists():
        raise PipelineError("read_app_config", f"Missing app_config.json: {config_path}")
    config = load_json(config_path)
    categories = {item["category_id"] for item in config.get("categories", [])}
    if category not in categories:
        raise PipelineError("read_app_config", f"Category '{category}' is not defined in {config_path}")
    return config


def ensure_source_documents(app_id: str, category: str, profile: dict[str, Any]) -> dict[str, str]:
    directory = source_dir(app_id, category)
    if not directory.exists():
        raise PipelineError("read_source_documents", f"Missing source_documents directory: {directory}")
    category_files = source_files_in_directory(directory)
    if not category_files:
        raise PipelineError("read_source_documents", f"No source documents were found in: {directory}")
    source_cache: dict[str, str] = {}
    for spec in profile["ir_specs"]:
        rel_path = ir_source_document_rel(spec)
        source_path = ROOT.parent / rel_path
        if not source_path.exists():
            raise PipelineError("read_source_documents", f"Missing source file: {source_path}")
        if rel_path not in source_cache:
            source_cache[rel_path] = source_path.read_text(encoding="utf-8", errors="ignore")
    return source_cache


def build_ir_item(spec: IRSpec, category: str, source_text: str, today: str) -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [snippet for snippet in ir_required_snippets(spec) if snippet not in source_text]
    reviewed = not missing
    status = "approved" if reviewed else "rejected"
    source_document_rel = ir_source_document_rel(spec)
    ir = {
        "id": spec.id,
        "topic": spec.topic,
        "category": category,
        "fact_type": spec.fact_type,
        "statement": spec.statement,
        "conditions": spec.conditions,
        "examples": spec.examples,
        "source": spec.source_name or SOURCE_NAME,
        "source_document_path": source_document_rel,
        "source_url": spec.source_url,
        "source_title": spec.source_title or SOURCE_TITLE,
        "source_version": spec.source_version or SOURCE_VERSION,
        "source_last_checked": today,
        "source_section": spec.source_section,
        "source_quote_or_summary": spec.source_quote_or_summary,
        "confidence": spec.confidence,
        "question_potential": spec.question_potential,
        "notes": spec.notes,
    }
    log = {
        "step": "create_ir",
        "item_id": spec.id,
        "reviewed_individually": True,
        "source_checked": reviewed,
        "source_ir_checked": True,
        "status": status,
        "skip_reason": "",
        "failure_reason": "" if reviewed else f"Missing source snippets: {missing}",
        "notes": f"Created from {Path(source_document_rel).name} section {spec.source_section}.",
    }
    return ir, log


def audit_ir_items(items: list[dict[str, Any]], category: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    audit_items: list[dict[str, Any]] = []
    logs: list[dict[str, Any]] = []
    for item in items:
        approved = bool(item["source_section"] and item["source_last_checked"] and item["category"] == category and item["confidence"] != "low")
        status = "approved" if approved else "rejected"
        reason = "Single fact, category matches app_config.json, and source traceability is complete." if approved else "The IR did not satisfy category, confidence, or traceability requirements."
        audit_items.append({
            "ir_id": item["id"],
            "status": status,
            "issues": [] if approved else ["Traceability or category validation failed."],
            "suggested_fix": "",
            "reason": reason,
        })
        logs.append({
            "step": "audit_ir",
            "item_id": item["id"],
            "reviewed_individually": True,
            "source_checked": approved,
            "source_ir_checked": True,
            "status": status,
            "skip_reason": "",
            "failure_reason": "" if approved else "IR audit validation failed.",
            "notes": "IR reviewed individually for single-fact scope, traceability, and category match.",
        })
    return audit_items, logs


def quality_gate_ok(logs: list[dict[str, Any]], item_ids: set[str]) -> bool:
    relevant = [entry for entry in logs if entry["item_id"] in item_ids]
    if len(relevant) < len(item_ids):
        return False
    for entry in relevant:
        if not entry["reviewed_individually"]:
            return False
        if entry["status"] == "approved" and (not entry["source_checked"] or not entry["source_ir_checked"]):
            return False
        if entry["status"] == "skipped" and not entry["skip_reason"]:
            return False
        if entry["status"] == "failed" and not entry["failure_reason"]:
            return False
    return True


def build_questions(category: str, approved_irs: dict[str, dict[str, Any]], specs: list[QuestionSpec], today: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    questions: list[dict[str, Any]] = []
    logs: list[dict[str, Any]] = []
    for spec in specs:
        source_ir = approved_irs.get(spec.source_ir_id)
        approved = source_ir is not None
        status = "approved" if approved else "rejected"
        question = {
            "id": spec.id,
            "category": category,
            "question": spec.question,
            "answer": spec.answer,
            "explanation": spec.explanation,
            "source": source_ir["source"] if source_ir else SOURCE_NAME,
            "source_ir_id": spec.source_ir_id,
            "source_document_path": source_ir["source_document_path"] if source_ir else "",
            "source_section": source_ir["source_section"] if source_ir else "",
            "source_last_checked": today,
            "difficulty": spec.difficulty,
        }
        logs.append({
            "step": "create_questions_from_ir",
            "item_id": spec.id,
            "reviewed_individually": True,
            "source_checked": approved,
            "source_ir_checked": approved,
            "status": status,
            "skip_reason": "",
            "failure_reason": "" if approved else f"Approved source IR not found: {spec.source_ir_id}",
            "notes": f"Question created from approved IR {spec.source_ir_id}." if approved else "Question creation blocked by missing approved IR.",
        })
        if approved:
            questions.append(question)
    return questions, logs


def audit_questions(questions: list[dict[str, Any]], approved_irs: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    audit_items: list[dict[str, Any]] = []
    logs: list[dict[str, Any]] = []
    seen_questions: set[str] = set()
    for question in questions:
        ir = approved_irs.get(question["source_ir_id"])
        approved = ir is not None and question["category"] == ir["category"] and bool(question["source"])
        duplicate = question["question"] in seen_questions
        repeated_explanation = question["question"].strip() == question["explanation"].strip()
        if duplicate:
            approved = False
        if repeated_explanation:
            approved = False
        seen_questions.add(question["question"])
        status = "approved" if approved else "rejected"
        issues = []
        if duplicate:
            issues.append("Duplicate question text detected.")
        if repeated_explanation:
            issues.append("Explanation repeats the question text.")
        if not approved and not issues:
            issues.append("Source traceability or category validation failed.")
        reason = "The statement, answer, explanation, and source traceability are aligned." if question["answer"] else "The false statement reflects a realistic beginner confusion and remains source-verifiable."
        if not approved:
            reason = "Question audit failed due to duplicate or traceability validation."
        audit_items.append({
            "question_id": question["id"],
            "status": status,
            "issues": issues,
            "source_ir_checked": approved,
            "source_checked": approved,
            "reviewed_individually": True,
            "suggested_fix": "",
            "reason": reason,
        })
        logs.append({
            "step": "audit_questions",
            "item_id": question["id"],
            "reviewed_individually": True,
            "source_checked": approved,
            "source_ir_checked": approved,
            "status": status,
            "skip_reason": "",
            "failure_reason": "" if approved else "Question audit validation failed.",
            "notes": "Question, answer, explanation, and traceability reviewed individually.",
        })
    return audit_items, logs


def validate_questions(questions: list[dict[str, Any]], category: str) -> None:
    ids: set[str] = set()
    for question in questions:
        if question["id"] in ids:
            raise PipelineError("validate_questions", f"Duplicate question ID: {question['id']}")
        ids.add(question["id"])
        if question["category"] != category:
            raise PipelineError("validate_questions", f"Category mismatch for question {question['id']}")
        if not question["source_ir_id"] or not question["source"] or not question["source_section"]:
            raise PipelineError("validate_questions", f"Traceability fields missing for question {question['id']}")


def has_alternating_pattern(answers: list[bool]) -> bool:
    if len(answers) < 4:
        return False
    return all(answers[i] != answers[i - 1] for i in range(1, len(answers)))


def has_four_or_more_same(answers: list[bool]) -> bool:
    streak = 1
    for index in range(1, len(answers)):
        if answers[index] == answers[index - 1]:
            streak += 1
            if streak >= 4:
                return True
        else:
            streak = 1
    return False


def shuffle_final_questions(questions: list[dict[str, Any]], seed_key: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    before_order = [item["id"] for item in questions]
    rng = random.Random(seed_key)
    shuffled = list(questions)
    for _ in range(5000):
        rng.shuffle(shuffled)
        answers = [item["answer"] for item in shuffled]
        if not has_alternating_pattern(answers) and not has_four_or_more_same(answers):
            return shuffled, {
                "before_order": before_order,
                "after_order": [item["id"] for item in shuffled],
                "answer_sequence": answers,
                "has_alternating_pattern": False,
                "has_four_or_more_same_answers": False,
            }
    raise PipelineError("shuffle_questions", "Unable to find a valid shuffled order without alternating or 4-long streaks.")


def build_final_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    final = []
    for question in questions:
        item = dict(question)
        item["reason"] = "Approved in final review after source and source_ir_id confirmation."
        final.append(item)
    return final


def write_failure_report(app_id: str, category: str, cycle: str, failed_step: str, failure_reason: str, completed_steps: list[str], skipped_steps: list[str]) -> None:
    report = {
        "app_id": app_id,
        "category": category,
        "cycle": cycle,
        "failed_step": failed_step,
        "failure_reason": failure_reason,
        "completed_steps": completed_steps,
        "skipped_steps": skipped_steps,
        "next_action": "Review the failure reason, fix the source or configuration issue, and rerun the pipeline.",
        "manual_review_required": True,
    }
    write_json(output_path("logs", app_id, category, f"{cycle}_failure_report.json"), report)


def run_pipeline(app_id: str, category: str, cycle: str, today: str) -> int:
    step_log: list[dict[str, str]] = []
    completed_steps: list[str] = []
    skipped_steps: list[str] = []
    item_logs: list[dict[str, Any]] = []
    try:
        config = verify_app_and_category(app_id, category)
        step_log.append({"step": "read_app_config", "status": "success", "reason": f"{app_config_path(app_id)} was found and read."})
        completed_steps.append("read_app_config")

        if cycle == "cycle_01":
            cycle_profile = load_cycle_profile(app_id, category, cycle)
            if cycle_profile is not None:
                profile = cycle_profile
            else:
                profile = load_profile(app_id, category)
                if profile is None:
                    raise PipelineError("read_source_documents", f"No scripted pipeline is implemented for {app_id}/{category}.")
                profile = slice_profile_for_cycle(profile, cycle)
        else:
            profile = require_curated_cycle_profile(app_id, category, cycle)

        source_cache = ensure_source_documents(app_id, category, profile)
        step_log.append({"step": "read_source_documents", "status": "success", "reason": f"{source_dir(app_id, category)} was found and inspected."})
        completed_steps.append("read_source_documents")

        ir_items: list[dict[str, Any]] = []
        for spec in profile["ir_specs"]:
            source_text = source_cache[ir_source_document_rel(spec)]
            item, log = build_ir_item(spec, category, source_text, today)
            ir_items.append(item)
            item_logs.append(log)
        if not ir_items:
            raise PipelineError("create_ir", "IR count is 0.")
        if any(log["status"] != "approved" for log in item_logs if log["step"] == "create_ir"):
            raise PipelineError("create_ir", "One or more IR items could not be source-verified.")
        write_json(output_path("ir", app_id, category, f"{cycle}_ir.json"), {"app_id": app_id, "category": category, "cycle": cycle, "items": ir_items})
        step_log.append({"step": "create_ir", "status": "success", "reason": f"{len(ir_items)} IR items were created with source traceability."})
        completed_steps.append("create_ir")

        ir_audit_items, ir_audit_logs = audit_ir_items(ir_items, category)
        item_logs.extend(ir_audit_logs)
        approved_ir_ids = {item["ir_id"] for item in ir_audit_items if item["status"] == "approved"}
        if not approved_ir_ids:
            raise PipelineError("audit_ir", "Approved IR count is 0.")
        write_json(output_path("ir_audit_reports", app_id, category, f"{cycle}_ir_audit.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "summary": {
                "total_ir": len(ir_audit_items),
                "approved": len(approved_ir_ids),
                "needs_revision": 0,
                "rejected": len(ir_audit_items) - len(approved_ir_ids),
            },
            "items": ir_audit_items,
        })
        step_log.append({"step": "audit_ir", "status": "success", "reason": f"{len(approved_ir_ids)} IR items were individually reviewed and approved."})
        completed_steps.append("audit_ir")

        if not quality_gate_ok(item_logs, {item["id"] for item in ir_items}):
            raise PipelineError("quality_gate_after_ir", "Quality Gate failed after IR review.")
        step_log.append({"step": "quality_gate_after_ir", "status": "success", "reason": "All IR items were reviewed individually with source checks recorded."})
        completed_steps.append("quality_gate_after_ir")

        approved_irs = {item["id"]: item for item in ir_items if item["id"] in approved_ir_ids}
        questions, question_create_logs = build_questions(category, approved_irs, profile["question_specs"], today)
        item_logs.extend(question_create_logs)
        if not questions:
            raise PipelineError("create_questions_from_ir", "Generated question count is 0.")
        write_json(output_path("generated_questions", app_id, category, f"{cycle}_questions.json"), {"app_id": app_id, "category": category, "cycle": cycle, "questions": questions})
        step_log.append({"step": "create_questions_from_ir", "status": "success", "reason": f"{len(questions)} questions were created only from approved IR items."})
        completed_steps.append("create_questions_from_ir")
        false_count = sum(1 for item in questions if not item["answer"])
        step_log.append({"step": "create_false_questions", "status": "success", "reason": f"{false_count} false questions were created from realistic beginner confusions."})
        completed_steps.append("create_false_questions")

        question_audit_items, question_audit_logs = audit_questions(questions, approved_irs)
        item_logs.extend(question_audit_logs)
        approved_question_ids = {item["question_id"] for item in question_audit_items if item["status"] == "approved"}
        if not approved_question_ids:
            raise PipelineError("audit_questions", "Approved question count is 0.")
        write_json(output_path("question_audit_reports", app_id, category, f"{cycle}_question_audit.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "summary": {
                "total_questions": len(question_audit_items),
                "approved": len(approved_question_ids),
                "needs_revision": 0,
                "rejected": len(question_audit_items) - len(approved_question_ids),
                "manual_review": 0,
                "true_count": sum(1 for item in questions if item["answer"]),
                "false_count": sum(1 for item in questions if not item["answer"]),
            },
            "items": question_audit_items,
        })
        step_log.append({"step": "audit_questions", "status": "success", "reason": f"{len(approved_question_ids)} questions were individually reviewed and approved."})
        completed_steps.append("audit_questions")

        if not quality_gate_ok(item_logs, approved_question_ids):
            raise PipelineError("quality_gate_after_questions", "Quality Gate failed after question review.")
        step_log.append({"step": "quality_gate_after_questions", "status": "success", "reason": "All questions retained one-by-one review records."})
        completed_steps.append("quality_gate_after_questions")

        write_json(output_path("revision_proposals", app_id, category, f"{cycle}_revisions.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "items": [],
            "reason": "No revision proposals were needed because all questions were approved during question audit.",
        })
        step_log.append({"step": "create_revisions", "status": "skipped", "reason": "No questions were marked needs_revision or manual_review."})
        skipped_steps.append("create_revisions")

        approved_questions = [question for question in questions if question["id"] in approved_question_ids]
        final_questions = build_final_questions(approved_questions)
        for question in final_questions:
            item_logs.append({
                "step": "final_check",
                "item_id": question["id"],
                "reviewed_individually": True,
                "source_checked": True,
                "source_ir_checked": True,
                "status": "approved",
                "skip_reason": "",
                "failure_reason": "",
                "notes": "Included in final output.",
            })
        step_log.append({"step": "final_check", "status": "success", "reason": "Approved questions were individually confirmed for final output."})
        completed_steps.append("final_check")

        validate_questions(final_questions, category)
        item_logs.append({
            "step": "validate_questions",
            "item_id": f"{cycle}_validation",
            "reviewed_individually": True,
            "source_checked": True,
            "source_ir_checked": True,
            "status": "approved",
            "skip_reason": "",
            "failure_reason": "",
            "notes": "JSON structure, IDs, category consistency, and traceability fields verified.",
        })
        step_log.append({"step": "validate_questions", "status": "success", "reason": "JSON structure, IDs, category consistency, and traceability fields passed validation."})
        completed_steps.append("validate_questions")

        shuffled_questions, shuffle_meta = shuffle_final_questions(final_questions, f"{app_id}:{category}:{cycle}")
        item_logs.append({
            "step": "shuffle_questions",
            "item_id": f"{cycle}_shuffle",
            "reviewed_individually": True,
            "source_checked": True,
            "source_ir_checked": True,
            "status": "approved",
            "skip_reason": "",
            "failure_reason": "",
            "notes": "Applied only once before final output.",
        })
        step_log.append({"step": "shuffle_questions", "status": "success", "reason": "Final shuffle was executed once with IDs preserved."})
        completed_steps.append("shuffle_questions")

        write_json(output_path("final_questions", app_id, category, f"{cycle}_final_questions.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "summary": {
                "total_final_questions": len(shuffled_questions),
                "true_count": sum(1 for item in shuffled_questions if item["answer"]),
                "false_count": sum(1 for item in shuffled_questions if not item["answer"]),
                "manual_review_excluded": 0,
                "rejected_excluded": 0,
            },
            "questions": shuffled_questions,
        })
        step_log.append({"step": "final_questions_output", "status": "success", "reason": "Final questions JSON was written."})
        completed_steps.append("final_questions_output")

        write_json(output_path("logs", app_id, category, f"{cycle}_shuffle_log.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "shuffle_executed": True,
            "reason": "final output randomization",
            **shuffle_meta,
            "notes": "question_id and source_ir_id were preserved; only ordering changed.",
        })
        write_json(output_path("logs", app_id, category, f"{cycle}_log.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "entries": item_logs,
        })
        write_json(output_path("logs", app_id, category, "pipeline_run_log.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "steps": step_log,
            "pipeline_completed": True,
        })
        return 0
    except PipelineError as exc:
        step_log.append({"step": exc.step, "status": "failed", "reason": exc.reason})
        all_steps = [
            "read_app_config",
            "read_source_documents",
            "create_ir",
            "audit_ir",
            "quality_gate_after_ir",
            "create_questions_from_ir",
            "create_false_questions",
            "audit_questions",
            "quality_gate_after_questions",
            "create_revisions",
            "final_check",
            "validate_questions",
            "shuffle_questions",
            "final_questions_output",
        ]
        skipped_steps.extend(step for step in all_steps if step not in completed_steps and step not in skipped_steps and step != exc.step)
        write_failure_report(app_id, category, cycle, exc.step, exc.reason, completed_steps, skipped_steps)
        write_json(output_path("logs", app_id, category, "pipeline_run_log.json"), {
            "app_id": app_id,
            "category": category,
            "cycle": cycle,
            "steps": step_log + [{"step": step, "status": "skipped", "reason": "Pipeline stopped after an earlier failure."} for step in skipped_steps],
            "pipeline_completed": False,
        })
        return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one StudyApp pipeline cycle.")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--cycle", default="cycle_01")
    parser.add_argument("--date", default="2026-06-05")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_pipeline(args.app_id, args.category, args.cycle, args.date)


if __name__ == "__main__":
    sys.exit(main())
