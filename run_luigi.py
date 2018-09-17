import luigi


class YearConcat(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("")

    def run(self):
        raise NotImplementedError


class SpatialSubset(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("")

    def run(self):
        raise NotImplementedError


class MonthSubset(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("")

    def run(self):
        raise NotImplementedError


class WindSpeedUnitConversion(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("")

    def run(self):
        raise NotImplementedError


class PrecipitationUnitConversion(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("")

    def run(self):
        raise NotImplementedError


class MonsoonIndex(luigi.Task):
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("")

    def run(self):
        raise NotImplementedError


if __name__ == 'main':
    luigi.run()
