# -*- coding: utf-8 -*--
import os
import io
import logging
import datetime
import time
import json
import atexit
import pytz
import click
import urllib
from typing import Dict

from src.feature_eng.feature_eng import process as fe_process
from src.preparation.preparation import process as prep_process
from src.scoring.scoring import process as score_process
from src.training.training import process as train_process

from src.common import path_helper
from src.common.common_helper import (
    get_last_month,
    timer,
    set_environment_variables,
    get_month,
    log_name_s3_cw,
    log,
    write_logs,
    get_date,
    build_session,
    set_spark_context,
)
from src.common.Lineage import Lineage


def run_job_prep(start_period: str, end_period: str, period: str, aws_job_id) -> Dict:
    """
    Run the preparation job
    :param aws_job_id: the AWS Batch job ID
    """
    try:
        LOGGER = log(os.environ["cw_s3_logger_name"])
        LOGGER.info("Lineage Status Running")
        LOGGER.info("Initializing Preparation Process...")
        input_paths = path_helper.get_paths(start_period, end_period, period, "Estand")
        output_paths = path_helper.get_paths(
            start_period, end_period, period, "Refined"
        )
        if not input_paths:
            LOGGER.info("Failed - Missing File input...")
        elif not output_paths:
            LOGGER.info("Failed - Missing File output...")
        else:
            df_pre_mdt, finals_paths_in, finals_paths_pre_mdt = prep_process(
                input_paths, output_paths, start_period, end_period
            )
        LOGGER.info("Preparation Process Finished")
        LOGGER.info("Loading Data of Preparation Job in Integration Table...")
        LOGGER.info("Loading Data of Preparation Job in Integration Table Finished")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table...")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table Finished")
        LOGGER.info("Loading Data of Preparation Job in Process Table...")
        LOGGER.info("Loading Data of Preparation Job in Process Table Finished")
        LOGGER.info("Lineage Status Suceeded")
        LOGGER.info("Preparation Job Status Suceeded")

    except Exception as e:
        LOGGER.info("Lineage status Failed")
        LOGGER.info(f"{e}")


def run_job_fe(start_period: str, end_period: str, period: str, aws_job_id) -> Dict:
    """
    Run the feature engineering job
    :param date_period: the start time of the data source for a execution
    :param aws_job_id: the AWS Batch job ID
    """
    try:
        LOGGER = log(os.environ["cw_s3_logger_name"])
        LOGGER.info("Lineage Status Running")
        LOGGER.info("Initializing Feature Eng Process...")
        input_paths = path_helper.get_paths_dynamo_parquet(
            start_period, end_period, "Refined"
        )
        output_paths = path_helper.get_paths_dynamo_parquet(
            start_period, end_period, "Resources"
        )
        if not input_paths:
            LOGGER.info("Failed - Missing File input...")
        elif not output_paths:
            LOGGER.info("Failed - Missing File output...")
        else:
            mdts = fe_process(input_paths, start_period, end_period)
            LOGGER.info(mdts)
        LOGGER.info("Feature_Engineering Process Finished")
        LOGGER.info("Loading Data of Feature_Engineering Job in Integration Table...")
        LOGGER.info(
            "Loading Data of Feature_Engineering Job in Integration Table Finished"
        )
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table...")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table Finished")
        LOGGER.info("Loading Data of Feature_Engineering Job in Process Table...")
        LOGGER.info("Loading Data of Feature_Engineering Job in Process Table Finished")
        LOGGER.info("Lineage Status Suceeded")
        LOGGER.info("Feature_Engineering Job Status Suceeded")
    except Exception as e:
        LOGGER.info("Lineage status Failed")
        LOGGER.info(f"{e}")


def run_job_training(
    start_period: str, end_period: str, period: str, aws_job_id
) -> None:
    """
    Run the training engineering job
    :param date_period: the start time of the data source for a execution
    :param aws_job_id: the AWS Batch job ID
    """
    try:
        LOGGER = log(os.environ["cw_s3_logger_name"])
        LOGGER.info("Lineage Status Running")
        LOGGER.info("Initializing training Process...")
        input_paths = path_helper.get_paths_dynamo_parquet(
            start_period, end_period, "Refined"
        )
        output_paths = path_helper.get_paths_dynamo_parquet(
            start_period, end_period, "Resources"
        )
        if not input_paths:
            LOGGER.info("Failed - Missing File input...")
        elif not output_paths:
            LOGGER.info("Failed - Missing File output...")
        else:
            models = train_process(input_paths, start_period, end_period)
            LOGGER.info(models)
        LOGGER.info("Training Process Finished")
        LOGGER.info("Loading Data of Training Job in Integration Table...")
        LOGGER.info("Loading Data of Training Job in Integration Table Finished")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table...")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table Finished")
        LOGGER.info("Loading Data of Training Job in Process Table...")
        LOGGER.info("Loading Data of Training Job in Process Table Finished")
        LOGGER.info("Lineage Status Suceeded")
        LOGGER.info("Training Job Status Suceeded")

    except Exception as e:
        LOGGER.info("Lineage status Failed")
        LOGGER.info(f"{e}")


def run_job_scoring(
    start_period: str, end_period: str, period: str, aws_job_id
) -> None:
    """
    Run the scoring job
    :param aws_job_id: the AWS Batch job ID
    """
    try:
        LOGGER = log(os.environ["cw_s3_logger_name"])
        LOGGER.info("Lineage Status Running")
        LOGGER.info("Initializing Scoring Eng Process...")
        input_paths = path_helper.get_paths_dynamo_parquet(
            start_period, end_period, "Refined"
        )
        output_paths = path_helper.get_paths_dynamo_parquet(
            start_period, end_period, "Resources"
        )
        if not input_paths:
            LOGGER.info("Failed - Missing File input...")
        elif not output_paths:
            LOGGER.info("Failed - Missing File output...")
        else:
            scores = score_process(input_paths, start_period, end_period)
            LOGGER.info(scores)

        LOGGER.info("Scoring Process Finished")
        LOGGER.info("Loading Data of Scoring Job in Integration Table...")
        LOGGER.info("Loading Data of Scoring Job in Integration Table Finished")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table...")
        LOGGER.info("Loading Data of EndToEnd Job in Integration Table Finished")
        LOGGER.info("Loading Data of Scoring Job in Process Table...")
        LOGGER.info("Loading Data of Scoring Job in Process Table Finished")
        LOGGER.info("Lineage Status Suceeded")
        LOGGER.info("Scoring Job Status Suceeded")

    except Exception as e:
        LOGGER.info("Lineage status Failed")
        LOGGER.info(f"{e}")


@click.command()
@click.option(
    "--job", default="prep", help="prep, fe, scoring, training", required=True
)
@click.option("--overwrite", help="True, False", required=False)
@click.option("--start_period", help="YYYY/MM/DD", required=False)
@click.option("--end_period", help="YYYY/MM/DD", required=False)
@click.option(
    "--period",
    default="2022-02-16T14:55:15Z",
    help="yyyy-mm-ddThh:mm:ssZ",
    required=True,
)
@click.option(
    "--aws_job_id", default="10", help="The current AWS Batch Job ID", required=True
)
@click.option(
    "--env",
    default="ds",
    help="'dev' for development, 'prod' for production environment, 'ds' for Data Sciences",
    required=True,
)
def main(job, overwrite, start_period, end_period, period, aws_job_id, env):
    start = time.time()
    set_environment_variables(env)
    os.environ["OVERWRITE_DATA"] = overwrite or "False"
    start_period = start_period or get_date(period)
    end_period = end_period or get_date(period)

    log_period = start_period.replace("/", "-")

    path_s3_log, cw_s3_logger_name, stream_log = log_name_s3_cw(
        job, env, log_period, aws_job_id
    )
    os.environ["cw_s3_logger_name"] = cw_s3_logger_name

    LOGGER = log(os.environ["cw_s3_logger_name"])
    log_stringio = io.StringIO()
    log_txt = logging.StreamHandler(log_stringio)
    format_txt = logging.Formatter(
        "%(asctime)s -> %(name)s -> %(levelname)s: %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    log_txt.setFormatter(fmt=format_txt)
    LOGGER.addHandler(log_txt)

    LOGGER.info("Creating New Spark Context ...")
    # spark_session = build_session("name_use_case", "16g")["spark"]
    # spark_context = set_spark_context("name_use_case")
    LOGGER.info("Spark session Created")

    LOGGER.info(f"Job: {job} {aws_job_id}")
    LOGGER.info(f"Overwrite files: {overwrite}")
    LOGGER.info("Execution Period: {0} - {1}".format(start_period, end_period))
    LOGGER.info("Execution Day: {0}".format(period))

    os.environ["AWS_BATCH_JOB_ID"] = aws_job_id

    LOGGER.info(f"Starting a job: {aws_job_id}")

    # Start a job
    function_dict = {
        "prep": run_job_prep,
        "fe": run_job_fe,
        "scoring": run_job_scoring,
        "training": run_job_training,
    }
    job_function = function_dict.get(job)
    job_function(start_period, end_period, period, aws_job_id)
    timer(start, time.time(), LOGGER)
    atexit.register(
        write_logs,
        body=log_stringio.getvalue(),
        bucket=os.environ["LOGS"].split("/")[0],
        key="/".join(path_s3_log.split("/")[1:]),
    )


if __name__ == "__main__":
    # allows to set the aws access key
    main(auto_envvar_prefix="X")  # pylint: disable=E1123,E1120
