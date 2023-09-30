from io import BytesIO

import xlsxwriter


def export_robot_report_to_xlsx(robot_data: list[dict]) -> BytesIO:
    buffer = BytesIO()
    
    file_headers = ('Модель', 'Версия', 'Количество за неделю')
    with xlsxwriter.Workbook(buffer) as workbook:
        current_model = ""
        for robot in robot_data:
            col = 0
            
            if current_model != robot['model']:
                current_model = robot['model']
                worksheet = workbook.add_worksheet(current_model)
                [worksheet.write(0, i, value) for i, value in enumerate(file_headers)]
                row = 1
                
            for value in robot.values():
                worksheet.write(row, col, value)
                col += 1
            row += 1
    
    return buffer        
    