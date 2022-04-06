import argparse
import logging
import os
import tarfile
import tempfile

import apache_beam as beam
from apache_beam.io import fileio
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from google.cloud import storage


def process_file(file):
    logging.info("- " + file.metadata.path)
    bucket_name = "mcclane-staging"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    with tempfile.TemporaryDirectory() as tmp_folder:
        file_path = file.metadata.path.replace("gs://" + bucket_name + "/druni/", "")
        print(file_path)
        logging.info("FILE PATH- " + file_path)
        #blob = bucket.get_blob(file_path)

        #with tempfile.NamedTemporaryFile() as f:
        #    blob.download_to_file(f)
        #    f.flush()
#
        #    tar = tarfile.open(f.name, "r")
        #    tar.extractall(tmp_folder)
        #    tar.close()
#
        #for screenshot_file in os.listdir(tmp_folder + "/data/screenshots/"):
        #    logging.info("[" + screenshot_file + " -> " + str(os.stat(tmp_folder + "/data/screenshots/" + screenshot_file).st_size) + " Kb]")

# access to bucket at gs://mapreuce-exercise-jplou/blobs/
# https://cloud.google.com/docs/authentication/production#passing_variable
"""
export GOOGLE_APPLICATION_CREDENTIALS="/home/mminguez/Desktop/ejercicios/petabyte_transformations/staging_global_service_account"


env/bin/python -m \
mcclane_bucket_dataflow \
--region europe-west1 \
--runner DataflowRunner \
--project staging-infra-240711 \
--temp_location gs://mapreuce-exercise-manuel/temp/ \
--requirements_file dataflow_requirements.txt



env/bin/python -m \
mcclane_bucket_dataflow \
--region europe-west1 \
--project staging-infra-240711 \
--temp_location gs://mapreuce-exercise-manuel/temp/ \
--requirements_file dataflow_requirements.txt

"""


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    bucket_name = "mcclane-staging"
    source_folder = "gs://" + bucket_name + "/druni/"
  
    with beam.Pipeline(options=pipeline_options) as pipeline:
        files = (
            pipeline
            | fileio.MatchFiles(source_folder + "**/*")
            | fileio.ReadMatches()
            | "show image files" >> beam.ParDo(process_file)
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
