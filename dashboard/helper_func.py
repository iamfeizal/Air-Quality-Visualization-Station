class MeanProcessing:
    def __init__(self, df):
        self.df=df

    def create_sorted_CO_mean_values_df(self):
        mean_CO_df = self.df
        CO_columns = [col for col in mean_CO_df.columns if col.startswith('CO_')]
        mean_CO_df=mean_CO_df[CO_columns].copy()
        mean_CO_df=mean_CO_df.describe().loc['mean']
        mean_CO_df=mean_CO_df.reset_index()
        mean_CO_df=mean_CO_df.rename(columns={'index': 'station', 'mean': 'CO mean'})
        mean_CO_df['station'] = mean_CO_df['station'].str.replace('CO_', '', regex=False)
        sorted_mean_CO_df = mean_CO_df.sort_values(by="CO mean", ascending=False)
        return sorted_mean_CO_df

    def create_sorted_PM10_mean_values_df(self):
        mean_PM10_df = self.df
        PM10_columns = [col for col in mean_PM10_df.columns if col.startswith('PM10_')]
        mean_PM10_df=mean_PM10_df[PM10_columns].copy()
        mean_PM10_df=mean_PM10_df.describe().loc['mean']
        mean_PM10_df=mean_PM10_df.reset_index()
        mean_PM10_df=mean_PM10_df.rename(columns={'index': 'station', 'mean': 'PM10 mean'})
        mean_PM10_df['station'] = mean_PM10_df['station'].str.replace('PM10_', '', regex=False)
        sorted_mean_PM10_df = mean_PM10_df.sort_values(by="PM10 mean", ascending=True)
        return sorted_mean_PM10_df

class MonthlyProcessing:
    def __init__(self, df):
        self.df=df

    def create_monthly_mean_df(self):
        wanliu_monthly_df = self.df
        wanliu_monthly_df = wanliu_monthly_df.resample(rule='M', on='datetime').agg({
            "PM2.5": "mean",
        })
        wanliu_monthly_df.index = wanliu_monthly_df.index.strftime('%Y %B')
        wanliu_monthly_df = wanliu_monthly_df.reset_index()
        return wanliu_monthly_df

class WanliuProcessing:
    def __init__(self, df):
        self.df=df

    def create_wanliu_df(self):
        wanliu_df = self.df
        wanliu_df = wanliu_df.resample(rule='D', on='datetime').agg({
            "PM2.5": "mean",
            "PM10": "mean",
            "CO": "mean"
        })
        return wanliu_df