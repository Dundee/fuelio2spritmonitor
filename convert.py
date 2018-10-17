import argparse
import csv
import io


def convert(file_name):
    output = io.StringIO()

    with open(file_name, 'r') as rfp:
        reader = csv.reader(rfp)

        use_miles = False
        in_log = False
        log = []

        for line in reader:
            if line[0] == '## Log':
                in_log = True
                continue
            # header
            if line[0] == 'Data':
                if line[1] == 'Odo (mi)':
                    use_miles = True
                continue
            if in_log and line[0].startswith('##'):
                break
            if in_log:
                log.append(line)

    writer = csv.writer(output)
    writer.writerow((
        'fuelup_date',
        'odometer',
        'litres',
        'partial_fuelup',
        'price',
    ))

    for item in log:
        writer.writerow((
            item[0],  # date
            item[1],  # ODO
            item[2],  # litres
            0 if item[3] == '1' else 1,  # full
            item[13],  # price/l
        ))

    print(output.getvalue().strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Fuelio CSV into Fuelly CSV')
    parser.add_argument('file', help='CSV file to parse')
    args = parser.parse_args()

    convert(args.file)
