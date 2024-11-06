
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from bot.parser.shedule.UniversityShedule import  UniversitySchedule



class Parser:
    def parse_file(self, xlsx_location: str) -> UniversitySchedule:
        wb: Workbook = openpyxl.load_workbook(filename=xlsx_location)
        us: UniversitySchedule = UniversitySchedule()
        for ws in wb.worksheets:
            us.merge_schedules(self.__parse_worksheet(ws))
        return us

    def __parse_worksheet(self, ws: Worksheet):
        #Идем вниз пока не найдем слово дни и запоминаем координату
        return UniversitySchedule()


if __name__ == '__main__':
    parser = Parser()
    grp_shedule:UniversitySchedule = parser.parse_file('./rasp.xlsx')
