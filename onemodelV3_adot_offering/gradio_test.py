import pandas as pd
import gradio as gr
from typing import List

# Setting the precision of numbers to 2 decimal places
# s = df.style.format("{:.2f}")

def greet(df):
    df = pd.DataFrame({
    "A" : [14.12345, 4.23456, 5.34567, 4.45678, 1.56789], 
    "B" : [5.67891, 2.78912, 54.89123, 3.91234, 2.12345], 
    # ... other columns
    }) 
    return df

def filter_records(records, name):
    return records.loc[records['name'] == name]

def call_feast(user_id: str, features:List): 
    """ implement Feast 호출"""
    mock_api = [
        {
        "values": ["aaefdfa50081f2020e7b27aa44086d1cf4999017179f2cd098d2b546279e50fc"],
        "statuses": ["PRESENT"],
        "event_timestamps": ["1970-01-01T00: 00: 00Z"]
        },
        {
            "values": [
                [
                    round(0.0030955201226635204, 4),
                    round(0.0008368274787716285, 4),
                    round(0.0003644698068292545, 4),
                    round(-0.001804624325378576, 4),
                    round(-0.010911989546514435, 4),
                    round(-0.012886816094245935, 4)
                ]
            ],
            "statuses": ["PRESENT"
            ],
            "event_timestamps": ["2024-06-12T10: 01: 02Z"]
        },
        {
            "values": [
            [
                "event_id4",
                "event_id2",
                "event_id5",
                "event_id1",
                "event_id6",
                "event_id3"
            ]
            ],
            "statuses": ["PRESENT"],
            "event_timestamps": ["2024-06-12T10: 01: 02Z"]
        },
        {
            "values": [
            [
                "음악을 좋아하는 유저",
                "캠핑을 좋아하는 유저",
                "노래를 좋아하는 유저",
                "날씨를 좋아하는 유저",
                "게임를 좋아하는 유저",
                "미용을 좋아하는 유저",
            ]
            ],
            "statuses": ["PRESENT"],
            "event_timestamps": ["2024-06-12T10: 01: 02Z"]
        }
    ]
    return mock_api

def post_processing(response:List):
    
    return response

def get_user_data(user_id, features):
    response = call_feast(user_id=user_id, features=features)
    response = post_processing(response=response)

    # First, create the dictionary as before
    data_dict = {feature: item["values"] for feature, item in zip(features, response[1:])}

    # Then, create the DataFrame and explode all columns
    df = pd.DataFrame(data_dict).apply(pd.Series.explode)

    # Reset the index if needed
    df = df.reset_index(drop=True)

    return df

import gradio as gr

def get_retrieved_data(user_id):
    features = ['event_ids_score', 'event_ids', 'event_description']
    df = get_user_data(user_id, features)
    return df

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# User Information Retrieval")
    
    with gr.Row():
        with gr.Column(scale=1):
            user_id_input = gr.Textbox(
                label="User ID",
                placeholder="Enter user ID...",
                value="APL000"
            )
            submit_btn = gr.Button("Retrieve Data", variant="primary")
    
    with gr.Row():
        with gr.Column(scale=3):
            output_df = gr.DataFrame(
                headers=["Event IDs Score", "Event IDs", "Event Description"],
                datatype=["str", "str", "str"],
                label="Retrieved Data"
            )
            
    
    submit_btn.click(
        fn=get_retrieved_data,
        inputs=user_id_input,
        outputs=output_df
    )


demo.launch()