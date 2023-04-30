# External imports
import pyautogui
import time
from PIL import ImageGrab
import pathlib
from typing import Tuple, List

# Internal imports
from scenarios import get_cases, get_fringe, GetCasesFilter
import UI


######################################################################
'''VARIÁVEIS DE CONFIGURAÇÃO
Adapte essas variáveis para o seu caso de uso.
'''

# Pasta onde estão os resultados dos cenários
SCENARIOS_PATH = pathlib.Path(
    r"C:\Users\LUIMAR\OneDrive - DNV\GeniE\Projects\TS091\Detailed\TS091_Detailed")

# Pasta onde serão salvas as imagens com resultados
SAVED_IMAGES_DIR_PATH = r'C:\Users\LUIMAR\Desktop\Plot Automation\figures'

# Lista de cenários que NÃO devem ser plotados
SCENARIOS_NUMBERS_TO_SKIP: List[int] = list(range(13, 19))

# Filtros para selecionar os cenários que devem ser plotados
CASES_FILTER: GetCasesFilter = {
    "processing": "With PFP",
    "software": "USFOS"
}
######################################################################


def automate_scenarios_report_creation():
    cases = get_cases(SCENARIOS_PATH, CASES_FILTER)
    adjusted_image_perspective = False

    for case in cases:
        # TODO: Leo: add numbers of scenarios to skip/not skip as part of the filters dictionary
        if case.scenario_number in SCENARIOS_NUMBERS_TO_SKIP:
            continue

        start_time = time.perf_counter()

        # TODO: Leo: why we are waiting time here? Remove if not necessary or explain why with a comment
        time.sleep(5)

        UI.write_on_command_window(f'open raf {case.path}')
        UI.drag_step_cursor_to_final_step()

        for [fringe, variables] in get_fringe(case).items():
            # TODO: Leo: why we are waiting time here? Remove if not necessary or explain why with a comment
            time.sleep(2)

            UI.write_on_command_window(f'results fringe {variables}')

            # Stop in the first iteration to adjust image perspective
            if adjusted_image_perspective == False:
                input("Pressione qualquer tecla para continuar...")
                # TODO: Leo: why we are waiting time here?
                # I assume it's to wait for the user to adjust the image an press a key,
                # but it's better to explain this with a comment (also 5 seconds seems too little time to do this)
                time.sleep(5)
                adjusted_image_perspective = True

            if fringe == "plastic_strain":
                pyautogui.write(f'results fringerange -0.02, 0.02')
                pyautogui.press('enter')

            UI.copy_current_image_to_clipboard()

            # TODO: Leo: why we are waiting time here?
            # I assume it's to wait for the image to be copied to the clipboard,
            # but it's better to explain this with a comment
            time.sleep(2)

            # Save copied image to disk
            img = ImageGrab.grabclipboard()
            img_filename = f'Scenario_{case.scenario_number}_{case.processing}_fringe.png'
            img_path = pathlib.Path(SAVED_IMAGES_DIR_PATH, img_filename)
            img.save(img_path)

            UI.wait_until_image_saved__EXPERIMENTAL(img_path)

    elapsed_time = time.perf_counter() - start_time
    print(
        f"Elapsed time to save images for scenario case: {elapsed_time:0.4f} seconds")
