import argparse
import csv
import datetime
import io
from operator import itemgetter


def convert(file_name):
    output = io.StringIO()

    with open(file_name, 'r') as rfp:
        reader = csv.reader(rfp)

        in_log = False
        log = []

        for line in reader:
            if line[0] == '## Log':
                in_log = True
                continue
            # header
            if line[0] == 'Data':
                continue
            if in_log and line[0].startswith('##'):
                break
            if in_log:
                line[1] = int(line[1])
                log.append(line)

    log = sorted(log, key=itemgetter(1))  # sort by ODO

    writer = csv.writer(output, delimiter=';')
    writer.writerow((
        'Date',
        'Odometer',
        'Trip',
        'Quantity',
        'Type',
        'Total price',
        'Currency',
    ))

    previous_odo = None

    for item in log:
        date = datetime.datetime.strptime(item[0], '%Y-%m-%d').date()
        odo = int(item[1])
        distance = odo - previous_odo if previous_odo else 0

        if not distance:
            type_ = '3'  # first
        elif item[3] == '1':
            type_ = '1'  # full
        else:
            type_ = '2'  # partial

        writer.writerow((
            date.strftime('%d.%m.%Y'),  # date
            item[1],  # ODO
            distance,
            item[2],  # quantity
            type_,  # fueling type
            item[4],  # total price
            'CZK',
        ))

        previous_odo = odo

    print(output.getvalue().strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Fuelio CSV into Fuelly CSV')
    parser.add_argument('file', help='CSV file to parse')
    args = parser.parse_args()

    convert(args.file)
