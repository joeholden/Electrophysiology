import tools
import os
import pyabf


ROOT_DIR_RECORDING_DAY = r"C:\Users\Acer\Desktop\2023-07-26 great patch day".replace('\\', os.sep)


if __name__ == '__main__':
    tools.patch_log(abf_directory_path=os.path.join(ROOT_DIR_RECORDING_DAY, 'ABF'),
                    excel_save_path=ROOT_DIR_RECORDING_DAY)
    # Make directories if they don't exist
    PNG_SINGLE_TRACES_PATH= os.path.join(ROOT_DIR_RECORDING_DAY, 'PNG/Single Traces')
    PNG_ALL_TRACES_PATH = os.path.join(ROOT_DIR_RECORDING_DAY, 'PNG/ALL Traces')
    PNG_IV_CURVES = os.path.join(ROOT_DIR_RECORDING_DAY, 'PNG/IV Curves')
    EXCEL_IV_CURVES = os.path.join(ROOT_DIR_RECORDING_DAY, 'EXCEL/IV Curves')

    if not os.path.exists(PNG_SINGLE_TRACES_PATH):
        os.makedirs(PNG_SINGLE_TRACES_PATH)
    if not os.path.exists(PNG_ALL_TRACES_PATH):
        os.makedirs(PNG_ALL_TRACES_PATH)
    if not os.path.exists(PNG_IV_CURVES):
        os.makedirs(PNG_IV_CURVES)
    if not os.path.exists(EXCEL_IV_CURVES):
        os.makedirs(EXCEL_IV_CURVES)

    for root, dirs, files in os.walk(os.path.join(ROOT_DIR_RECORDING_DAY, 'ABF')):
        for file in files:
            abf = pyabf.ABF(os.path.join(root, file))
            if abf.protocol == 'AstroVoltClamp':
                try:
                    tools.iv_curve(plot_linear=False,
                                   excel_save_path=EXCEL_IV_CURVES,
                                   png_save_path=PNG_IV_CURVES,
                                   abf_path=os.path.join(root, file),
                                   display_fig=False,
                                   )
                except Exception as e:
                    print(e)
            try:
                tools.show_traces(abf_file_path=os.path.join(root, file),
                                  path_to_save_fig=PNG_ALL_TRACES_PATH,
                                  display_fig=False,
                                  save_fig=True,
                                  smooth=2)
            except Exception as e:
                print(e)

            try:
                for sweep in range(0, abf.sweepCount):
                    tools.show_trace(abf_file_path=os.path.join(root, file),
                                     path_to_save_fig=PNG_SINGLE_TRACES_PATH,
                                     display_fig=False,
                                     save_fig=True,
                                     trace_number=sweep)
            except Exception as e:
                print(e)
