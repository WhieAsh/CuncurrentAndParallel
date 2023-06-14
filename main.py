import os
import time

from yaml_reader import YamlPiplineExecutor


def main():
    current_time = time.time()
    pipline_file = os.environ.get('PIPLINE_FILE') or 'Piplines\Wiki_yphoo_scraper_pipline.yaml'
    yamlPiplineExecutor = YamlPiplineExecutor(pipline_file)
    yamlPiplineExecutor.start()
    yamlPiplineExecutor.join()
    print("Execution_time: ", round((time.time() - current_time)/1, 2))


if __name__ == "__main__":
    main()
