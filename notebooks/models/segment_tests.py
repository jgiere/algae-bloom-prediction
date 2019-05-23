import unittest
import pandas as pd
import scripts.helper_functions as hf


class TestDataSegment(unittest.TestCase):

    def setUp(self):
        dates = pd.date_range(start='2018-01-01', periods=10, freq='d')
        data = range(0, 10)
        self.time_column = 'datetime'
        self.df = pd.DataFrame(data={self.time_column: dates,
                                     'data': data,
                                     'custom': data})
        index = self.time_column + 'Index'
        self.df[index] = self.df[self.time_column]
        self.df = self.df.set_index(index)

    def test_segment_even_windows(self):
        segments, targets = hf.extract_windows(self.df, self.time_column,
                                               x_win_size=pd.Timedelta(1, unit='d'),
                                               y_win_size=pd.Timedelta(1, unit='d'),
                                               shift=pd.Timedelta(1, unit='d'))
        self.assertEqual(len(segments), len(targets))
        self.assertEqual(len(segments), 8)

    def test_segment_odd_windows(self):
        segments, targets = hf.extract_windows(self.df, self.time_column,
                                               x_win_size=pd.Timedelta(2, unit='d'),
                                               y_win_size=pd.Timedelta(1, unit='d'),
                                               shift=pd.Timedelta(1, unit='d'))
        self.assertEqual(len(segments), len(targets))
        self.assertEqual(len(segments), 7)

    def test_segment_too_big_windows(self):
        segments, targets = hf.extract_windows(self.df, self.time_column,
                                               x_win_size=pd.Timedelta(8, unit='d'),
                                               y_win_size=pd.Timedelta(8, unit='d'),
                                               shift=pd.Timedelta(1, unit='d'))
        self.assertEqual(len(segments), len(targets))
        self.assertEqual(len(segments), 0)

    def test_extract_percentile(self):
        # Create a custom variables for the custom column
        parameters = {'custom': {'x_win_size': pd.Timedelta('1 day'),
                                 'separation': pd.Timedelta('1 day')}}
        percentile_array = [0.5, 0.7, 0.8, 0.9, 0.3]
        segments, targets = hf.extract_windows(self.df, self.time_column,
                                               x_win_size=pd.Timedelta(2, unit='d'),
                                               y_win_size=pd.Timedelta(2, unit='d'),
                                               shift=pd.Timedelta(1, unit='d'),
                                               custom_parameters=parameters)
        x_df = hf.extract_percentile(segments, self.time_column, percentile_array[0])
        y_df = hf.extract_percentile(targets, self.time_column, percentile_array[0])

        x_df_arr = hf.extract_percentile(segments, self.time_column, percentile_array)
        y_df_arr = hf.extract_percentile(targets, self.time_column,  percentile_array)

        # Check that the number of rows matches the number of windows in segments/targets
        self.assertEqual(x_df.shape[0], len(segments))
        self.assertEqual(y_df.shape[0], len(targets))

        # Check that the number of rows matches the number of windows in segments/targets
        self.assertEqual(x_df_arr.shape[0], len(segments))
        self.assertEqual(y_df_arr.shape[0], len(targets))
        # Checking to see if the size of the resulting array is the right shape along the column axis
        # this is done because we have to ensure that for every item in the percentile array that we pass in
        # the percentile will be appended to EACH of the column names in the returned array.
        self.assertEqual(x_df_arr.shape[1], segments[0].shape[0] * len(percentile_array) + 1)
        self.assertEqual(y_df_arr.shape[1], segments[0].shape[0] * len(percentile_array) + 1)

        # Calculate average values from segments/targets
        data_means = []
        custom_means = []
        for window in segments:
            data_means.append(window['data'].mean())
            custom_means.append(window['custom'].mean())
        y_averages = []
        for window in targets:
            y_averages.append(window['data'].mean())

        # Check that our calculated averages match each row in the extracted dataframes
        for i in range(0, len(data_means)):
            self.assertAlmostEqual(data_means[i], x_df['data'].values[i])
            self.assertAlmostEqual(custom_means[i], x_df['custom'].values[i])
        for i in range(0, len(y_averages)):
            self.assertAlmostEqual(y_averages[i], y_df['data'].values[i])


if __name__ == '__main__':
    unittest.main()
