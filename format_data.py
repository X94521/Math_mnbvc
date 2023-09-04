import json
from glob import glob
from pathlib import Path

from functional import seq

from data_types import QaData, MetaData, Session, ForumQaData, ForumResponse, ForumMetaData
from typing import List
from hashlib import md5
import logging


logging.basicConfig(level=logging.INFO)


class MathProcess:
    def __init__(self) -> None:
        self.idx = 0

    @staticmethod
    def read_file(file_path, file_type):
        if 'MATH' in file_path:
            return [json.load(open(file_path))]
        elif "math23k" in file_path:
            f = open(file_path, encoding="utf-8")
            js = ""
            data = []
            for i, s in enumerate(f):
                js += s
                i += 1
                if i % 7 == 0:  # every 7 line is a json
                    data_d = json.loads(js)
                    if "千米/小时" in data_d["equation"]:
                        data_d["equation"] = data_d["equation"][:-5]
                    data.append(data_d)
                    js = ""
            return data
        elif "mathematics" in file_path:
            if 'train-readme' in file_path:
                return []
            f = open(file_path, encoding="utf-8")
            data = []
            line = {}
            for i, s in enumerate(f):
                if i % 2 == 1:
                    line["answer"] = s.strip()
                    if "question" in line and "answer" in line:
                        data.append(line)
                    line = {}
                else:
                    line["question"] = s.strip()
            return data
        if file_type == 'jsonl':
            return seq.jsonl(file_path)
        elif file_type == 'json':
            return seq.json(file_path)
    
    def read_corpus(self, input_dir, file_type, end_name):
        if end_name is None:
            end_name = file_type
        for file_path in Path(input_dir).iterdir():
            if file_path.is_dir():
                yield from self.read_corpus(str(file_path), file_type, end_name)
            file_path = str(file_path)
            if not file_path.endswith(end_name):
                continue
            yield from self.read_file(file_path, file_type)

    def process(self, input_dir, file_type, end_name, process_engine, dataset):
        save_path = Path('processed') / f"{dataset}.json"
        seq(self.read_corpus(input_dir, file_type, end_name))\
            .map(process_engine)\
            .filter(lambda x: x is not None)\
            .map(lambda x: [x] if not isinstance(x, list) else x)\
            .flatten()\
            .map(lambda x: json.dumps(x.dict(), ensure_ascii=False))\
            .to_file(save_path, delimiter='\n', encoding='utf-8')
    
    def process2stream(self, input_dir, file_type, end_name, process_engine, dataset):
        stream = seq(self.read_corpus(input_dir, file_type, end_name))\
            .map(process_engine)\
            .filter(lambda x: x is not None)\
            .map(lambda x: [x] if not isinstance(x, list) else x)\
            .flatten()\
            .map(lambda x: json.dumps(x.dict(), ensure_ascii=False))
        return stream
    
    def ape210k_engine(self, line):
        uid = self.idx
        self.idx += 1
        question = line['original_text']
        answer = f"equation:{line['equation']}\n{line['ans']}".strip()
        data = QaData.from_source(
            uid, question, answer, source="ape210k",
            question_from="original_text", answer_from=["equation", "ans"],
            extension=json.dumps({
                'from_id': line['id']
            })
        )
        return data

    def dolphin_number_engine(self, line):
        def get_answer(equations, ans):
            equations = '\n'.join([x.replace('unkn', 'unknown values').replace('equ', 'equation') for x in equations])
            return equations + '\n' + 'answer: ' + ans
        uid = self.idx
        self.idx += 1
        question = line['text']
        answer = get_answer(line['equations'], line['ans'])
        data = QaData.from_source(
            uid, question, answer, source='dolphin_number_word_std',
            question_from='text', answer_from=["equations", "ans"],
            extension=json.dumps({
                'from_id': line['id']
            })
        )
        return data
    
    def dolphin18k_engine(self, line):
        if 'original_text' not in line or 'text' not in line:
            return None
        def get_answer(equations, ans):
            equations = '\n'.join([x.replace('unkn', 'unknown values').replace('equ', 'equation') for x in equations])
            return equations + '\n' + 'answer: ' + ans
        question = line['text']
        answer = get_answer(line['equations'], line['ans'])
        uid = self.idx
        self.idx += 1
        data = QaData.from_source(
            uid, question, answer, source='dolphin_number_word_std',
            question_from='text', answer_from=["equations", "ans"],
            extension=json.dumps({
                'id': line['id'],
            })
        )
        return data
        

    def goat_engine(self, line):
        uid = self.idx
        self.idx += 1
        question = line["instruction"]
        answer = line["answer"]
        source = "goat"
        data = QaData.from_source(
            uid, question, answer, source,
            question_from="instruction", answer_from="answer",
            extension=""
        )
        return data
    
    def grade_school_math_engine(self, line):
        uid = self.idx
        self.idx += 1
        question = line['question']
        if "answer" in line:
            answer_from = "answer"
        elif "ground_truth" in line:
            answer_from = "ground_truth"
        answer = line[answer_from]
        source = "grade_school_match"
        data = QaData.from_source(
            uid, question, answer, source,
            question_from="question", answer_from=answer_from,
            extension=""
        )
        return data
    
    def math_engine(self, line):
        uid = self.idx
        self.idx += 1
        question = line["problem"]
        answer = line["solution"]
        source = "math"
        data = QaData.from_source(
            uid, question, answer, source,
            question_from="problem", answer_from="solution",
            extension=""
        )
        return data
    
    def math23k_engine(self, line):
        uid = self.idx
        self.idx += 1
        question = line["original_text"]
        answer = f"equation:{line['equation']}\n{line['ans']}".strip()
        source = "math"
        data = QaData.from_source(
            uid, question, answer, source,
            question_from="original_text", answer_from="solution",
            extension=json.dumps({
                'id': line['id'],
            })
        )
        return data
    
    def mathematics_engine(self, line):
        uid = self.idx
        self.idx += 1
        question = line["question"]
        answer = line["answer"]
        source = "mathematics"
        data = QaData.from_source(
            uid, question, answer, source,
            question_from="", answer_from="",
            extension=""
        )
        return data
    
    def prm800k_engine(self, line):
        if 'question' not in line:
            return None

        md5_value = md5(json.dumps(line).encode('utf-8')).hexdigest()

        question = line['question']['problem']
        steps = line['label']['steps']
        qa_list: List[ForumQaData] = []
        for idx, step in enumerate(steps):
            responses: List[ForumResponse] = []

            completions = step['completions']
            if not isinstance(completions, list):
                completions = []

            if step["chosen_completion"] is None and step["human_completion"] is not None:
                human_text = step['human_completion'].get('text')
                if human_text is not None:
                    completions.append({'rating': 2, 'text': human_text})
            
            completions = sorted(completions, key=lambda x: x['rating'] if x['rating'] is not None else -1, reverse=True)

            uid = self.idx
            self.idx += 1

            for r_id, comp in enumerate(completions):
                responses.append(ForumResponse(
                    楼ID=r_id,
                    回复=comp['text'],
                    扩展字段=json.dumps({
                        '引用ID': uid,
                        'from': 'completions.text' if comp['rating'] != 2 else 'human_completion',
                        'rating': comp['rating'],
                        'is_answer': 'Answer' in comp['text'],
                        'is_solution': idx == len(steps) - 1 and line['label']['finish_reason'] == 'solution',
                        'is_preferred_response': step["chosen_completion"] == r_id,
                        'is_human_response': comp['rating'] == 2
                    })
                ))


            qa_list.append(ForumQaData(
                ID=uid,
                主题=question,
                来源='prm800k',
                回复=responses,
                元数据=ForumMetaData(扩展字段=json.dumps({
                    '会话': md5_value,
                    '多轮序号': len(qa_list) + 1,
                    '标注人': line['labeler'],
                    "原文": line
                }, ensure_ascii=False)),
            ))

            if idx == len(steps) - 1:
                continue

            next_question = step["human_completion"] if step["chosen_completion"] is None \
                else step["completions"][step["chosen_completion"]]["text"]
            
            if isinstance(next_question, dict):
                next_question = next_question['text']
            
            if next_question is None:
                next_question = completions[0]['text']

            question = question + '\n' + next_question
        return qa_list


    def run(self, engine_map, save_file):
        f_out = open(f'processed/{save_file}', 'w', encoding='utf-8')
        for dataset, info in engine_map.items():
            # if dataset in ["ape210k", "dolphin_number_word_std", "goat", "grade_school_math", "math", "math23k", "mathematics"]:
            #     continue
            process_engine = getattr(self, info["engine"])
            logging.info(f'processing {dataset}...')
            stream = self.process2stream(
                input_dir=info["input_dir"],
                file_type=info["file_type"],
                end_name=info["end_name"],
                process_engine=process_engine,
                dataset=dataset
            )
            for line in stream:
                f_out.write(line + '\n')
        f_out.close()


if __name__ == "__main__":
    engine_map_qa = {
        "ape210k": {
            "engine": "ape210k_engine",
            "input_dir": "dataset/ape210k",
            "file_type": "jsonl",
            "end_name": "json"
        }, "dolphin_number_word_std": {
            "engine": "dolphin_number_engine",
            "input_dir": "dataset/dolphin_number_word_std",
            "file_type": "json",
            "end_name": "json"
        }, "dolphin18k": {
            "engine": "dolphin18k_engine",
            "input_dir": "dataset/dolphin18k",
            "file_type": "json",
            "end_name": "json"
        }, "goat": {
            "engine": "goat_engine",
            "input_dir": "dataset/goat",
            "file_type": "json",
            "end_name": "json"
        }, "grade_school_math": {
            "engine": "grade_school_math_engine",
            "input_dir": "dataset/grade_school_math",
            "file_type": "jsonl",
            "end_name": "jsonl"
        }, "math": {
            "engine": "math_engine",
            "input_dir": "dataset/MATH",
            "file_type": "json",
            "end_name": "json"
        }, "math23k": {
            "engine": "math23k_engine",
            "input_dir": "dataset/math23k",
            "file_type": "jsonl",
            "end_name": "json"
        }, "mathematics": {
            "engine": "mathematics_engine",
            "input_dir": "dataset/mathematics",
            "file_type": "txt",
            "end_name": "txt"
        }
    }
    p = MathProcess()
    p.run(engine_map_qa, 'math_qa.json')

    engine_map_cot = {
        "prm800k": {
            "engine": "prm800k_engine",
            "input_dir": "dataset/prm800k",
            "file_type": "jsonl",
            "end_name": "jsonl"
        }
    }
    p.idx = 0
    p.run(engine_map_cot, 'math_cot.json')
