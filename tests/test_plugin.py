import pytest_runtime_info
import os
import json


def test_tracebak(testdir):
    testdir.makepyfile("""
        def multiply():
            return 2 * 4 / 0

        def call_multiply():
            multiply()

        def test_multiply():
            call_multiply()
    """)
    result_file = pytest_runtime_info.getTempFilePath()
    try:
        file_modified = os.stat(result_file).st_mtime
    except Exception:
        file_modified = 0
    test_result = testdir.runpytest()
    # test if failed
    test_result.assert_outcomes(failed=1)
    # test if result file was modified
    assert file_modified != os.stat(result_file).st_mtime
    with open(result_file) as result_stream:
        result_json = result_stream.read()
        result = json.loads(result_json)
    tmpfile = os.path.join(testdir.tmpdir, "test_tracebak.py")
    assert len(result["exceptions"]) == 1
    assert result["exceptions"][0]["path"] == tmpfile
    assert len(result["fileMarkList"]) == 1
    assert result["fileMarkList"][0]["path"] == tmpfile
    assert len(result["fileMarkList"][0]["marks"]) == 10
