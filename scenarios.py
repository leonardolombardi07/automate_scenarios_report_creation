# External imports
from typing import List, Literal, Union, TypedDict
import pathlib


ScenarioCaseProcessing = Literal["FirstRun", "With PFP"]
ScenarioCaseSoftware = Literal["FAHTS", "USFOS"]


class ScenarioCase():
    def __init__(self, scenario_number: int, processing: ScenarioCaseProcessing,
                 software: ScenarioCaseSoftware, path: pathlib.Path):
        self.scenario_number = scenario_number
        self.processing = processing
        self.software = software
        self.path = path


class GetCasesFilterByKey(TypedDict):
    processing: Literal["Todos", "FirstRun", "With PFP"]
    software: Literal["Todos", "FAHTS", "USFOS"]


GetCasesFilter = Union[Literal("Todos"), GetCasesFilterByKey]


def get_cases(scenarios_folder_path: pathlib.Path,
              filter: GetCasesFilter = "Todos") -> List[ScenarioCase]:
    cases: List[ScenarioCase] = []

    for scenario_dir_path in scenarios_folder_path.iterdir():
        if scenario_dir_path.is_dir() == False:
            continue

        scenario_number = _get_scenario_number(scenario_dir_path)

        sorted_case_paths = sorted(
            scenario_dir_path.iterdir(), key=_sort_by_last_modified)

        for case_path in sorted_case_paths:
            if "firstrun" in case_path.name.lower():
                if case_path.is_dir() == False:
                    continue

                # TODO: Leo: I couldn't understand why we need to get the paths of the .raf files
                # Add a comment explanation here
                [FAHTS_PATH, USFOS_PATH] = list(case_path.glob(".raf"))

                fahts_case = ScenarioCase(scenario_number=scenario_number,
                                          processing="FirstRun",
                                          software="FAHTS",
                                          path=FAHTS_PATH)
                usfos_case = ScenarioCase(scenario_number=scenario_number,
                                          processing="FirstRun",
                                          software="USFOS",
                                          path=USFOS_PATH)
                cases.append(fahts_case)
                cases.append(usfos_case)

            elif case_path.suffix == ".raf":
                case = ScenarioCase(scenario_number=scenario_number,
                                    processing="With PFP",
                                    software="FAHTS" if case_path.name.lower() in ["faths", "output"]
                                    else "USFOS",
                                    path=case_path)
                cases.append(case)

    if type(filter) == dict:
        return [case for case in cases
                if (filter["processing"] in ["Todos", case.processing]) and
                (filter["software"] in ["Todos", case.software])]

    return cases


def _get_scenario_number(scenario_dir_path: pathlib.Path) -> int:
    # TODO: Leo: maybe we should add some error handling and check
    # if the file name is in the expected format and gives a valid scenario_number
    return int(scenario_dir_path.name[:scenario_dir_path.name.find("_")])


def _sort_by_last_modified(path: pathlib.Path) -> float:
    # TODO: Leo: use a solution that does not depend on the OS (WindowsPath)
    return pathlib.WindowsPath.stat(path).st_mtime


def get_fringe(scenario_case: ScenarioCase):
    '''Create different fringe based on report requirements'''

    # TODO: Leo: not so clear what "fringe cases" are.
    # The name "case" here gets confused with a scenario case, so I don't think we should use it.
    # Also, couldn't understand the conceptual difference between the key of a fringe case dictionary (for example "temperature")
    # and its corresponding value 'global, element, temperature').
    # This is important to give proper names on variables (I called the key "fringe"
    # and the value "variables", but probably there's something more appropriate )

    # TODO: if this should not be configurable but the user and depends only on information
    # like the file case and the PFP case, maybe we should not have this function and just
    # add the fringe as a property of the ScenarioCase class

    if scenario_case.processing == "FirstRun":
        if scenario_case.software == "USFOS":
            return {"temperature": 'global, element, temperature'}

    if scenario_case.processing == "With PFP":
        if scenario_case.software == "USFOS":
            return {"temperature": 'global, element, temperature',
                    "plastic_utilization": 'global, element, plastic utilization',
                    "z_displacement": 'global, node, displacement, z'}
        else:
            return {"PFP_cond": 'shell, node, pfp cond'}

    # Leo: is this intentional? How should we deal with FirstRun and FAHTS?
    raise TypeError(
        f"Scenario processed as '${scenario_case.processing}' and with software '{scenario_case.software}' not supported")
