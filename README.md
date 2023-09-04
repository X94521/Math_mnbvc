# MathQA-mnbvc

## 项目描述
- 本项目主要目的是搜集不同的 math 数据集，清洗并对齐到统一的数据格式
- 各个数据集原始的数据格式见 dataset
- 处理结果为 jsonl，每行对应一条数据

## 环境
```python
pip install -r requirements.txt
```

## 数据源
1. [ape210k](https://github.com/Chenny0808/ape210k)
2. [dolphin_number_word_std](https://www.microsoft.com/en-us/research/project/sigmadolphin/)
3. [dolphin18k](https://www.microsoft.com/en-us/research/project/sigmadolphin/)
4. [goat](https://huggingface.co/datasets/tiedong/goat)
5. [grade_school_math](https://github.com/openai/grade-school-math)
6. [MATH](https://github.com/hendrycks/math)
7. [math23k](https://github.com/SCNU203/Math23k)
8. [mathematics](https://github.com/deepmind/mathematics_dataset)
9. [prm800k](https://github.com/openai/prm800k)

## 用法
1. 下载数据到 dataset 目录下(各个数据源下载后的数据格式参考dataset目录下的sample文件)
2. 运行
```
python format_data.py
```

## 代码说明
- ```data_types.py``` 数据格式定义
- ```format_data.py``` 数据格式对齐

## 结果示例
1. math_qa.json

```json
{
    "id": 0,
    "问": "五年级同学参加义务捐书活动，五1班捐了500本，五2班捐的本数是五1班80%，五3班捐的本数是五2班120%，五1班和五3班比谁捐书多？(请用两种方法比较一下)．",
    "答": "equation:x=1\n1",
    "来源": "ape210k",
    "元数据": {
        "create_time": "20230904 22:18:59",
        "问题明细": "{\"from\": \"original_text\"}",
        "回答明细": "{\"from\": [\"equation\", \"ans\"]}",
        "扩展字段": "{\"from_id\": \"1099539\"}"
    }
}
```

2. math_cot.json
```
{
    "ID": 0,
    "主题": "Three pencils and a jumbo eraser cost $\\$1.24$. Five pencils and a jumbo eraser cost $\\$1.82$. No prices include tax. In cents, what is the cost of a pencil?",
    "来源": "prm800k",
    "回复": [
        {
            "楼ID": "0",
            "回复": "Let's call the price of a pencil p and the price of a jumbo eraser e. Then we can write two equations.",
            "扩展字段": "{\"\\u5f15\\u7528ID\": 0, \"from\": \"completions.text\", \"rating\": 1, \"is_answer\": false, \"is_solution\": false, \"is_preferred_response\": true, \"is_human_response\": false}"
        }
    ],
    "元数据": {
        "扩展字段": "{\"会话\": \"bb8e8fdd1ff5c331d300cb9fd13ca180\", \"多轮序号\": 1, \"标注人\": \"e90a38f3-3135-4465-87af-3e6322e3d772\", \"原文\": {\"labeler\": \"e90a38f3-3135-4465-87af-3e6322e3d772\", \"timestamp\": \"2022-07-30T23:23:32.118856\", \"generation\": null, \"is_quality_control_question\": false, \"is_initial_screening_question\": false, \"question\": {\"problem\": \"Three pencils and a jumbo eraser cost $\\\\$1.24$. Five pencils and a jumbo eraser cost $\\\\$1.82$. No prices include tax. In cents, what is the cost of a pencil?\", \"ground_truth_answer\": \"29\"}, \"label\": {\"steps\": [{\"completions\": [{\"text\": \"Let's call the price of a pencil p and the price of a jumbo eraser e. Then we can write two equations.\", \"rating\": 1, \"flagged\": false}], \"human_completion\": null, \"chosen_completion\": 0}, {\"completions\": [{\"text\": \"The first equation is 3p + e = 124, and the second equation is 5p + e = 182.\", \"rating\": -1, \"flagged\": false}, {\"text\": \"The first equation is 3p+e=124, and the second is 5p+e=182.\", \"rating\": -1, \"flagged\": false}, {\"text\": \"The first equation is 3p + e = 124.\", \"rating\": -1, \"flagged\": false}, {\"text\": \"The first equation is $3p+e=124$. The second equation is $5p+e=182$.\", \"rating\": -1, \"flagged\": false}, {\"text\": \"The first equation is $3p+e=124$.\", \"rating\": -1, \"flagged\": false}], \"human_completion\": {\"text\": \"We have $3p+e=1.24$ and $5p+e=1.82$.\", \"rating\": null, \"source\": \"human\", \"flagged\": false}, \"chosen_completion\": null}, {\"completions\": [{\"text\": \"To solve this system, let's subtract the first equation from the second equation. This will eliminate e.\", \"rating\": 1, \"flagged\": false}], \"human_completion\": null, \"chosen_completion\": 0}, {\"completions\": [{\"text\": \"$5p+e-3p-e=1.82-1.24$.\", \"rating\": 1, \"flagged\": false}], \"human_completion\": null, \"chosen_completion\": 0}, {\"completions\": [{\"text\": \"This simplifies to $2p=0.58$. So $p=0.29$.\", \"rating\": 1, \"flagged\": false}], \"human_completion\": null, \"chosen_completion\": 0}, {\"completions\": [{\"text\": \"We could also solve this system by substitution.\", \"rating\": 0, \"flagged\": false}, {\"text\": \"So a pencil costs $0.29.\", \"rating\": 1, \"flagged\": false}, {\"text\": \"Right. One pencil costs $\\\\$0.29$.\", \"rating\": 1, \"flagged\": false}, {\"text\": \"So the price of a pencil is 29 cents.\\n\\n# Answer\\n\\n29\", \"rating\": 1, \"flagged\": false}, {\"text\": \"That means a pencil costs 29 cents.\\n\\n# Answer\\n\\n29\", \"rating\": 1, \"flagged\": false}], \"human_completion\": null, \"chosen_completion\": 4}], \"total_time\": 293250, \"finish_reason\": \"solution\"}}}"
    }
}
```

[QA数据格式定义说明参考](https://github.com/pany8125/ShareGPTQAExtractor-mnbvc)


[COT数据格式定义说明参考](https://github.com/aplmikex/forum_dialogue_mnbvc)