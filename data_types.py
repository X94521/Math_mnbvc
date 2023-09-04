from pydantic import BaseModel
from typing import Union, List, Dict
import json
from datetime import datetime


class Session(BaseModel):
    会话: str
    多轮序号: int


class MetaData(BaseModel):
    create_time: str
    问题明细: str
    回答明细: str
    扩展字段: Union[str, Dict]


class QaData(BaseModel):
    id: int
    问: str
    答: str
    来源: str
    元数据: MetaData

    @classmethod
    def from_source(
        cls,
        uid: int,
        question: str,
        answer: str,
        source: str,
        question_from: Union[str, List[str]],
        answer_from: Union[str, List[str]],
        extension=""
    ):
        create_time = datetime.now().strftime("%Y%m%d %H:%M:%S")
        return cls(
            id=uid,
            问=question,
            答=answer,
            来源=source,
            元数据=MetaData(
                create_time=create_time,
                问题明细=json.dumps({"from": question_from}) if question_from else "",
                回答明细=json.dumps({"from": answer_from}) if answer_from else "",
                扩展字段=extension
            )
        )


class ForumExtraResponse(BaseModel):
    回复人: str
    回复时间: str
    回复ID: str
    点赞数: int = -1
    点踩数: int = -1


class ForumExtraQA(BaseModel):
    标签: str
    点赞数: str
    原文: str


class ForumResponse(BaseModel):
    楼ID: str
    回复: str
    扩展字段: str


class ForumMetaData(BaseModel):
    扩展字段: str


class ForumQaData(BaseModel):
    ID: int
    主题: str
    来源: str
    回复: List[ForumResponse]
    元数据: ForumMetaData
