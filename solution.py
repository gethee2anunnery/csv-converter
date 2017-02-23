import json
import argparse
import pandas as pd


class CSVConversion(object):
    """ Class that outputs csv to formatted JSON.

    Format 1: Write the data grouped by identifier and
    sorted by datetime

    Format 2 (rollup): Write the data rolled
    up with gaps maintained
    """

    include_gaps = True

    def csv_to_dataframe(self):
        df = pd.read_csv('./%s' % self.csv_filename,
                         delimiter=',', index_col=None,
                         parse_dates=True)
        return df

    def match_column_headers(self):
        df_headers = [h.strip() for h in self.df.columns.values]
        for h in self.headers:
            if h not in df_headers:
                raise Exception("Unknown column heading %s. "
                                "Choices are: %s"
                                % (h, ', '.join(self.df.columns.values)))

    def set_json_filename(self):
        input_filename = self.csv_filename.rstrip('.csv')
        self.json_filename = '%s.json' % input_filename

    def write_to_json(self, data):
        self.set_json_filename()

        with open('./%s' % self.json_filename, 'w') as f:
            f.write(json.dumps(data))

    def group_by_identifier(self):
        grouped_data = []

        # to lowercase for output
        self.df.columns = [h.lower() for h in self.df.columns.values]
        df = self.df.round({self.value_column_key: 4})

        # sort datetime and group by identifier
        dataframes_list = [g for g in df.sort_values(by=[self.datetime_column_key])
                                          .groupby(by=[self.id_column_key])]

        # build the list
        for i, df in dataframes_list:
            grouped_data.append({self.id_column_key: i,
                                 'data': [[row[self.datetime_column_key],
                                          row[self.value_column_key]] for i, row in
                                          df.iterrows()]})

        self.write_to_json(grouped_data)

    def rollup_hours(self):
        frames_list = []

        self.df.columns = [h.lower() for h in self.df.columns.values]

        # get index of all datetimes for hour grouping
        times = pd.DatetimeIndex(self.df[self.datetime_column_key])
        grouped = [df for i, df in self.df.groupby([times.day, times.hour])]

        # get a set of identifier values to account for
        identifiers = self.df[self.id_column_key].unique()

        # loop through hour groups and add zero frames
        for df in grouped:

            # set all values to a 4-precision decimal
            df = df.round({self.value_column_key: 4})

            # replace datetime values with corresponding rollup hour
            datetimes = pd.DatetimeIndex(df[self.datetime_column_key])
            hour_formatted = datetimes[0].strftime('%-m/%-d/%Y %-I:00%p')
            df[self.datetime_column_key] = hour_formatted

            # compare dataset's identifiers to the global set
            # and add a zero value row for each missing one
            if self.include_gaps:
                id_diff = set(identifiers) - set(df[self.id_column_key].unique())
                if id_diff:
                    gaps = [{self.value_column_key.lower(): 0,
                            self.id_column_key.lower(): i,
                            self.datetime_column_key.lower(): hour_formatted}
                            for i in id_diff]
                    df = df.append(pd.DataFrame(gaps))

            frames_list.append(df)

        # concat the hour-grouped dataframes and drop the index
        data = pd.concat(frames_list, ignore_index=True)

        json_data = data.reset_index(drop=True).T.to_dict().values()
        self.write_to_json(json_data)

    def __init__(self, csv_filename, datetime_header, value_header, id_header):
        self.csv_filename = csv_filename
        self.id_column_key = id_header.lower()
        self.datetime_column_key = datetime_header.lower()
        self.value_column_key = value_header.lower()
        self.headers = [id_header, value_header, datetime_header]
        self.df = self.csv_to_dataframe()
        self.match_column_headers()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help='Input file name, ex: "data.csv" ', required=True)
    parser.add_argument('--rollup', default=False, help='Output formatting,'
                                                'default False, if True '
                                                'will output in rollup format')
    args = parser.parse_args()
    converter = CSVConversion(args.filename, 'Datetime', 'Value', 'Identifier')
    if args.rollup:
        converter.rollup_hours()
    else:
        converter.group_by_identifier()

if __name__ == '__main__':
    main()

