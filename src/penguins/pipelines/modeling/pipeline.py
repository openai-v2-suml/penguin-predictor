"""
This is a boilerplate pipeline 'modeling'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, node, pipeline

from penguins.pipelines.modeling.nodes import split_data, train_model


def create_pipeline() -> Pipeline:
    """Create the kedro modeling pipeline."""
    return pipeline([
        node(
            func=split_data,
            inputs=["model_input_table"],
            outputs=["train", "test"],
            name="split_data_node",
        ),
        node(
            func=train_model,
            inputs=["train", "test"],
            outputs="classificator",
            name="train_model_node",
        )
    ])
