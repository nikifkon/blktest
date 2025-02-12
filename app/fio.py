from collections import defaultdict
import json
import logging
from itertools import product
from tempfile import NamedTemporaryFile
import subprocess

logger = logging.getLogger(__name__)


def get_global_config():
    return {
        "name": "global",
        "ioengine": "libaio",
        "direct": "1",
        "bs": "4k",
        "size": "1G",
        "numjobs": "1",
    }


def get_config_for_test(global_config, args, test_type, iodepth):
    config = global_config.copy()
    config["name"] = args.name
    config["filename"] = args.filename.name
    config["rw"] = test_type
    config["iodepth"] = iodepth
    return config


def write_section(file_obj, config):
    file_obj.write("[{}]\n".format(config["name"]))
    for k, v in config.items():
        if k == "name":
            continue
        file_obj.write("{}={}\n".format(k, v))
    file_obj.write("\n")


def generate_jobs_file(args, types, iodepths):
    job_file = NamedTemporaryFile(mode="w")
    global_config = get_global_config()
    jobs = (
        get_config_for_test(global_config, args, t, iodepth)
        for t, iodepth in product(types, iodepths)
    )
    for config in (global_config, *jobs):
        write_section(job_file.file, config)
    job_file.flush()
    return job_file


def measure(args):
    job_file = generate_jobs_file(args, ["randread", "randwrite"], args.iodepth)
    with open(job_file.name) as f:
        logger.info("Fio config: %s", f.read())

    p = subprocess.run(
        ["fio", job_file.name, "--output-format=json"], capture_output=True
    )
    fio_results = json.loads(p.stdout)

    results = defaultdict(lambda: [])

    for job_result in fio_results["jobs"]:
        test_type = job_result["job options"]["rw"]
        if "read" in test_type:
            clat = job_result["read"]["lat_ns"]["mean"]
        else:
            clat = job_result["write"]["lat_ns"]["mean"]
        iodpeth = job_result["job options"]["iodepth"]
        results[test_type].append((iodpeth, clat))

    return results
