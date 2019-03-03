import luigi


# TODO consider condensing tasks - must save output after each task could make lots of storage quickly
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


class TemporalSubset(luigi.Task):
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


class GettingUCData(luigi.Task):
    def output(self):
        return '/snfs1/users/nasa_develop/Fall2017/luigi/preprocessing_cmip5/preprocessing_cmip5/'


class PrecipitationUnitConversion(luigi.Task):

    def requires(self):
        return GettingUCData()

    def output(self):
        # return luigi.LocalTarget('/snfs1/users/nasa_develop/Fall2017/luigi/preprocessing_cmip5/unit_conversion/')
        return luigi.LocalTarget(r"C:\repos\luigi\preprocessing_cmip5\unit_conversion")

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
