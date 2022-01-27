import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import fileio
import argparse
from apache_beam.options.pipeline_options import SetupOptions
import logging


        



def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    _, pipeline_args = parser.parse_known_args(argv)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
    with beam.Pipeline(options=pipeline_options) as pipeline:
        from google.cloud import storage
        import os
        from tempfile import NamedTemporaryFile, TemporaryDirectory
        import json
        import tarfile

        class GcloudClient():
            def __init__(self):
                self.storage_client = storage.Client("staging-infra-240711")
                # Create a bucket object for our bucket
                self.bucket = self.storage_client.get_bucket("mapreduce-exercise-manuel")
            
            def download_blob_from_bucket(self, blob_name):
                # Create a blob object from the filepath
                blob = self.bucket.blob(blob_name)

                with NamedTemporaryFile() as f:
                    # Download the file to a destination
                    blob.download_to_file(f)
                    f.flush()

                    temp_dir = TemporaryDirectory()
                    target_dir = temp_dir.name
                    with tarfile.open(f.name, "r:gz") as tf:
                        tf.extractall(path=target_dir)

                    return temp_dir
            def upload_blob_to_bucket(self, target_location, source_file_name):
                blob = self.bucket.blob(target_location)
                blob.upload_from_filename(source_file_name)

        def process_blobs_dataflow(blob, output_dir):
            blob_path = blob.metadata.path
            blob_name = 'blobs/' + blob_path.split('/blobs/')[1]
            check_name = blob_name.split('-')[0].split('/')[1]
            blob_file_name = blob_path.split('/blobs/')[1]

            gcloud_client = GcloudClient()
            temp_dir = gcloud_client.download_blob_from_bucket(blob_name)
            meta_path = os.path.join(temp_dir.name, "metadata.json")
            result_path = os.path.join(temp_dir.name, "result.json")
                
            with open(meta_path, "r") as f:
                meta = json.load(f)
            with open(result_path, "r") as f:
                result = json.load(f)

            source_file_name = os.path.join(output_dir, blob_name)
            #target_location = os.path.join("gs://mapreduce-exercise-manuel", source_file_name)
            
            meta['check_name'] = check_name

            with TemporaryDirectory() as tmp_folder:
                #We need to compress the blob and save it to the target directory
                with open('metadata.json', 'w') as outfile:
                    json.dump(meta, outfile)
                with open('result.json', 'w') as outfile:
                    json.dump(result, outfile)

                with tarfile.open(tmp_folder + "/" + blob_file_name, "w:gz") as tar:
                    tar.add(os.path.basename('metadata.json'))
                    tar.add(os.path.basename('result.json'))
                
                gcloud_client.upload_blob_to_bucket(source_file_name, tmp_folder + "/" + blob_file_name)



        readable_files = (
            pipeline
            | 'Read from Bucket' >> fileio.MatchFiles('gs://mapreduce-exercise-manuel/blobs/*.tar.gz')
            | fileio.ReadMatches(compression='auto')
            | 'Apply transformation' >> beam.Map(lambda x: (process_blobs_dataflow(x, 'clean_blobs_3')))
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()


"""
export GOOGLE_APPLICATION_CREDENTIALS="/home/mminguez/Desktop/ejercicios/petabyte_transformations/staging_global_service_account"
python -m dataflow \
    --region europe-west1 \
    --runner DataflowRunner \
    --project staging-infra-240711 \
    --temp_location gs://mapreduce-exercise-manuel/tmp/ \
    --requirements_file dataflow_requirements.txt

"""




