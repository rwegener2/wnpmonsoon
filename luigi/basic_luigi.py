from wnpmonsoon.ncdata import NCdata
import netCDF4 as nc
import luigi


class WindDirectionUC(luigi.Task):
    uas_filepath = luigi.parameter.Parameter()
    vas_filepath = luigi.parameter.Parameter()

    def output(self):
        return luigi.LocalTarget("/home/rwegener/repos/wnpmonsoon/luigi/testing/wdir.nc")

    def run(self):
        with nc.Dataset(self.uas_filepath, 'r') as uas_reader, \
             nc.Dataset(self.vas_filepath, 'r') as vas_reader:
            wdir = NCdata.wind_dir_from_components(uas_reader, vas_reader)
        wdir.write(self.output())
        # with self.output().open('w') as f:
        #     f.write('it is working')


class PrecipitationUC(luigi.Task):
    pr_filepath = luigi.parameter.Parameter()

    def output(self):
        return luigi.LocalTarget("/home/rwegener/repos/wnpmonsoon/luigi/testing/pr.nc")

    def run(self):
        with nc.Dataset(self.pr_filepath, 'r') as flux_reader:
            p_rate = NCdata.pr_rate_from_flux(flux_reader)
        p_rate.write(self.output())


# class MonsoonMonthClip(luigi.Task):
#     # TODO do I define multiple of these or can I assign just one and change inputs
#     uas_filepath = luigi.parameter.Parameter()
#     vas_filepath = luigi.parameter.Parameter()
#     pr_filepath = luigi.parameter.Parameter()
#
#     def requires(self):
#         return [PrecipitationUC(self.pr_filepath),
#                 WindDirectionUC(self.uas_filepath, self.vas_filepath)]
#
#     def output(self):
#         return luigi.LocalTarget("/home/rwegener/repos/wnpmonsoon/luigi/testing/jjaso.nc")
#
#     def run(self):
#         with nc.Dataset('') as reader:
#             pass
#
#
# class MonsoonIndex(luigi.Task):
#     def requires(self):
#         return [MonsoonMonthClip()]
#
#     def output(self):
#         return luigi.LocalTarget("/home/rwegener/repos/wnpmonsoon/luigi/testing/monsoon.nc")
#
#     def run(self):
#         with nc.Dataset('') as reader:
#             pass


if __name__ == 'main':
    luigi.run()
