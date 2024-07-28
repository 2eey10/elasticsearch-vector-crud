import json
from pathlib import Path
from typing import Union

import yaml


def load_yaml(fp: Union[str, Path]) -> dict:
    """yaml파일을 load하여 dict로 반환한다.

    Args:
        fp (Union[str, Path]): yaml file path

    Raises:
        FileNotFoundError: 파일이 os상 존재하지 않을 때

    Returns:
        dict: yaml 내부 내용
    """
    fp = Path(fp)

    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")

    with open(fp) as f:
        yam = yaml.safe_load(f)

    return yam


def save_yaml(
    obj,
    fp: Union[str, Path],
):
    """obj내용을 fp(path)에 yaml 형식으로 저장.

    Args:
        obj (_type_): dict 등 자료형
        fp (Union[str, Path]): 저장할 file path
    """
    fp = Path(fp)

    with open(fp, "w") as f:
        yaml.safe_dump(obj, f, indent=4, sort_keys=False)


def save_json(obj, fp: Union[str, Path]):
    """obj내용을 fp(path)에 json 형식으로 저장.
    Args:
        obj (Any): dict 등 자료형
        fp (Union[str, Path]): 저장할 file path
    """
    fp = Path(fp)
    with open(fp, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def save_txt(obj: Union[str, dict], fp: Union[str, Path]):
    """obj 내용을 fp(path)에 txt 형식으로 저장.

    Args:
        obj (Union[str, dict]): 저장할 텍스트 또는 사전
        fp (Union[str, Path]): 저장할 파일 경로
    """
    if isinstance(fp, str):
        fp = Path(fp)

    if isinstance(obj, dict):
        obj = str(obj)

    with open(fp, "w") as f:
        f.write(obj)


def load_json(fp: Union[str, Path]) -> dict:
    """json파일을 load하여 dict로 반환한다.
    Args:
        fp (Union[str, Path]): json file path
    Returns:
        dict: json 내부 내용
    """
    fp = Path(fp)
    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")
    with open(fp) as f:
        jso = json.load(f)
    return jso