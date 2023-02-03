import csv
import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

FIELDS_NAME = ('Статус', 'Количество')
DIR_OUTPUT = 'results'
DT_FORMAT = '%Y-%m-%dT%H-%M-%S'
FILE_NAME = 'status_summary_{time}.csv'
TIME_NOW = dt.datetime.now().strftime(DT_FORMAT)


class PepParsePipeline:
    def open_spider(self, spider):
        """
        Формирование пути до директории results.
        """
        self.results = {}

    def process_item(self, item, spider):
        """
        Подсчет количества pep-статусов.
        """
        status = item['status']
        self.results[status] = self.results.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        """
        Запись данных в файл.
        """
        self.results_dir = BASE_DIR / DIR_OUTPUT
        self.results_dir.mkdir(exist_ok=True)
        file_dir = self.results_dir / FILE_NAME.format(time=TIME_NOW)
        with open(file_dir, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow((FIELDS_NAME))
            writer.writerows(self.results.items())
            writer.writerow(['Total', sum(self.results.values())])
